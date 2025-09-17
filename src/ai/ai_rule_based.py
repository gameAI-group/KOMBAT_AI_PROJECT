# src/ai/ai_rule_based.py
"""
AI điều khiển theo luật định sẵn (Lv2).

Hành vi được cài đặt:
- Tham số phụ thuộc độ khó (Dễ / Trung bình / Khó).
- Nhận thức vai trò: nhân vật A (phòng thủ/trừng phạt), nhân vật B (tấn công/kết hợp combo).
- Phản công khi vừa nhận sát thương.
- Tự động phòng thủ khi HP < 30% (có khác biệt nhỏ theo vai trò).

File này cố ý không sử dụng ngẫu nhiên cho quyết định cốt lõi; độ khó vẫn điều chỉnh ngưỡng và ưu tiên.
"""
from ..config import SP_COST_SPECIAL, SP_COST_ROLL


class AIRuleBased:
	def __init__(self, fighter, target, difficulty=None):
		self.fighter = fighter
		self.target = target
		self.action_cooldown = 0
		self.counterattack_ready = False
		# theo dõi trạng thái tấn công trước đó của đối thủ để phát hiện cơ hội phản đòn
		self.prev_target_attacking = False
		# bộ đếm giữ tư thế thủ cho B để không giữ thủ quá lâu
		self.defend_hold = 0
		self.last_hp = fighter.hp
		self.difficulty = (difficulty or "EASY").upper()
		# số frame khóa di chuyển (khi chuẩn bị tấn công)
		self.movement_block_frames = 0
		# cho phép A hung hãn ngay lúc đầu (chạy áp sát) trong một khoảng thời gian ngắn
		# điều này khiến hiệp sĩ lửa lao vào đối thủ ngay đầu round thay vì đứng yên
		self.initial_aggression_frames = 60 if getattr(self.fighter, 'character_type', None) == 'A' else 0
		# lưu lại anchor_x để phát hiện khi round được reset (bắt đầu round mới)
		self._last_anchor_x = getattr(self.fighter, 'anchor_x', None)

		# Điều chỉnh theo độ khó (ngưỡng và mức độ hung hãn)
		if self.difficulty == 'HARD':
			self.close_range = 140
			self.aggressiveness = 0.9
			self.evade_preference = 0.6
		elif self.difficulty == 'MEDIUM':
			self.close_range = 150
			self.aggressiveness = 0.6
			self.evade_preference = 0.4
		else:  # EASY
			self.close_range = 180
			self.aggressiveness = 0.35
			self.evade_preference = 0.2

	def ensure_face_target(self):
		"""Đảm bảo nhân vật AI luôn quay mặt về phía mục tiêu khi bắt đầu tấn công.
		Tránh đổi hướng trong những hành động khác ngoài tấn công.
		"""
		try:
			# anchor_x là vị trí hiện tại của nhân vật
			self.fighter.flip = False if self.fighter.anchor_x < self.target.anchor_x else True
			# khóa di chuyển tạm thời để move() không đổi hướng flip
			self.movement_block_frames = 2
		except Exception:
			pass

	def update(self):
		# Nếu HP quá thấp, ưu tiên phòng thủ/rút lui
		hp_ratio = self.fighter.hp / max(1, self.fighter.max_hp)
		# bỏ trạng thái phòng thủ nếu không còn ở mức nguy hiểm để tránh bị kẹt
		if hp_ratio >= 0.30:
			self.fighter.defending = False
		
		if hp_ratio < 0.30:
			# Cả 2 vai trò đều ưu tiên phòng thủ và giữ vị trí (không di chuyển khi phòng thủ)
			self.fighter.defending = True
			self.fighter.ai_move_direction = 0
			self.counterattack_ready = False
			self.last_hp = self.fighter.hp
			# đảm bảo quay mặt về phía đối thủ khi phòng thủ
			try:
				self.fighter.flip = False if self.fighter.anchor_x < self.target.anchor_x else True
			except Exception:
				pass
			return

		# Phát hiện vừa bị đánh trúng → chuẩn bị phản công
		if self.fighter.hp < self.last_hp:
			self.counterattack_ready = True
		self.last_hp = self.fighter.hp

		# Phát hiện cơ hội phản đòn: đối thủ vừa ngừng tấn công
		current_target_attacking = getattr(self.target, 'attacking', False)
		if self.prev_target_attacking and not current_target_attacking:
			distance = abs(self.fighter.rect.centerx - self.target.rect.centerx)
			if distance <= self.close_range + 20:
				# A ưu tiên dùng chiêu đặc biệt nếu có, B ưu tiên đánh nhanh (light)
				if self.fighter.character_type == 'A' and self.fighter.sp >= SP_COST_SPECIAL:
					self.ensure_face_target()
					self.fighter.attack(self.target, 'special')
					self.action_cooldown = 30
					self.prev_target_attacking = current_target_attacking
					return
				elif self.fighter.character_type == 'B':
					self.ensure_face_target()
					self.fighter.attack(self.target, 'light')
					self.action_cooldown = 10
					self.prev_target_attacking = current_target_attacking
					return
		self.prev_target_attacking = current_target_attacking

		# Nếu không thể hành động, không ra lệnh mới
		can_act = not self.fighter.attacking and not self.fighter.hit and not self.fighter.rolling and not self.fighter.dead
		if not can_act:
			self.fighter.ai_move_direction = 0
			return

		# Nếu đang bị khóa di chuyển, giảm bộ đếm
		if self.movement_block_frames > 0:
			self.movement_block_frames -= 1
			self.fighter.ai_move_direction = 0

		# Phát hiện round reset: nếu nhân vật được đưa về start_x, bật lại trạng thái hung hãn lúc đầu
		start_x = getattr(self.fighter, 'start_x', None)
		if start_x is not None and self.fighter.anchor_x == start_x and self._last_anchor_x != self.fighter.anchor_x:
			if getattr(self.fighter, 'character_type', None) == 'A':
				self.initial_aggression_frames = 60
				# quay mặt về phía đối thủ khi round bắt đầu và A sẽ lao vào
				try:
					self.fighter.flip = False if self.fighter.anchor_x < self.target.anchor_x else True
				except Exception:
					pass

		# Giảm dần bộ đếm hung hãn nếu còn hiệu lực
		if self.initial_aggression_frames > 0:
			self.initial_aggression_frames -= 1

		# Cập nhật anchor_x cuối cùng để phát hiện round mới
		try:
			self._last_anchor_x = self.fighter.anchor_x
		except Exception:
			pass

		# Nếu B đang thủ, giảm thời gian giữ thủ và bỏ khi đối thủ không tấn công
		if self.fighter.character_type == 'B' and self.fighter.defending:
			if not getattr(self.target, 'attacking', False):
				self.defend_hold = max(0, self.defend_hold - 1)
				if self.defend_hold == 0:
					self.fighter.defending = False
					self.fighter.ai_move_direction = 1 if self.fighter.rect.centerx < self.target.rect.centerx else -1
					self.action_cooldown = 6
					return

		# khoảng cách đến đối thủ
		distance = abs(self.fighter.rect.centerx - self.target.rect.centerx)

		# Phản công ngay nếu có cờ
		if self.counterattack_ready:
			self.counterattack()
			self.counterattack_ready = False
			return

		# Nếu đang cooldown, tập trung di chuyển/giữ vị trí
		if self.action_cooldown > 0:
			self.action_cooldown -= 1
			self.positioning()
			return

		# Nếu không thì quyết định hành động mới
		self.decide_action()

		# Cập nhật anchor_x cuối cùng để phát hiện round mới
		try:
			self._last_anchor_x = self.fighter.anchor_x
		except Exception:
			pass

	def positioning(self):
		# Căn chỉnh vị trí: tiếp cận hoặc giữ khoảng cách tùy vai trò
		distance = abs(self.fighter.rect.centerx - self.target.rect.centerx)
		if self.fighter.character_type == 'B':
			# B (hung hãn): tiến gần, trừ khi quá gần và đối thủ đang tấn công
			if distance > self.close_range:
				self.fighter.ai_move_direction = 1 if self.fighter.rect.centerx < self.target.rect.centerx else -1
			else:
				self.fighter.ai_move_direction = 0
		else:
			# A (phòng thủ): giữ khoảng cách an toàn
			# Nếu còn thời gian hung hãn lúc đầu, thì áp sát giống B trong thời gian ngắn
			if self.initial_aggression_frames > 0:
				# Lao vào gần hơn bình thường (so với tầm đánh thường)
				rush_target_distance = max(60, self.close_range - 40)  # vào gần hơn mức thường
				if distance > rush_target_distance:
					self.fighter.ai_move_direction = 1 if self.fighter.rect.centerx < self.target.rect.centerx else -1
				else:
					self.fighter.ai_move_direction = 0
			else:
				safe_distance = self.close_range + 30
				if distance < safe_distance:
					self.fighter.ai_move_direction = -1 if self.fighter.rect.centerx < self.target.rect.centerx else 1
				else:
					self.fighter.ai_move_direction = 0

	def decide_action(self):
		distance = abs(self.fighter.rect.centerx - self.target.rect.centerx)
		target_is_attacking = getattr(self.target, 'attacking', False)

		# Nếu đối thủ đang tấn công và mình ở gần
		if target_is_attacking and distance <= (self.close_range + 30):
			if self.fighter.character_type == 'A':
				# A ưu tiên chắn đòn
				if self.fighter.sp < SP_COST_SPECIAL:
					self.fighter.defending = True
					self.fighter.ai_move_direction = 0
					self.action_cooldown = 10
					return
				self.fighter.defending = True
				self.fighter.ai_move_direction = 0
				self.action_cooldown = 10
				return
			else:
				# B ưu tiên né (roll), nếu không thì nhảy, cuối cùng mới thủ
				can_try_roll = (not self.fighter.rolling and self.fighter.roll_cooldown_timer == 0 and self.fighter.sp >= SP_COST_ROLL)
				if can_try_roll:
					self.fighter.roll()
					if self.fighter.rolling:
						self.action_cooldown = 20
						return
				if self.fighter.jumps_left > 0 and not self.fighter.in_air:
					self.fighter.jump()
					self.action_cooldown = 12
					return
				self.fighter.defending = True
				self.defend_hold = 10
				self.fighter.ai_move_direction = 0
				self.action_cooldown = 8
				return

		# Hành vi thường khi đối thủ không tấn công
		if distance > self.close_range:
			if self.fighter.character_type == 'B':
				self.fighter.ai_move_direction = 1 if self.fighter.rect.centerx < self.target.rect.centerx else -1
			else:
				# A bình thường đứng yên, nhưng khi còn hung hãn thì sẽ áp sát hơn
				if self.initial_aggression_frames > 0:
					rush_target_distance = max(60, self.close_range - 40)
					if distance > rush_target_distance:
						self.fighter.ai_move_direction = 1 if self.fighter.rect.centerx < self.target.rect.centerx else -1
					else:
						self.fighter.ai_move_direction = 0
				else:
					self.fighter.ai_move_direction = 0
			return

		# Khi đã ở gần: chọn tấn công (light/special) tùy vai trò
		if self.fighter.character_type == 'B':
			if self.fighter.sp >= SP_COST_SPECIAL and self.difficulty in ('MEDIUM', 'HARD'):
				self.ensure_face_target()
				self.fighter.attack(self.target, 'special')
				self.action_cooldown = self.fighter.attacks.get('special', {}).get('cooldown', 30)
				return
			self.fighter.combo_input_timer = 0
			if 'light' in self.fighter.action and self.fighter.combo_step > 0:
				self.ensure_face_target()
				self.fighter.attack(self.target, 'light')
				self.action_cooldown = 8
				return
			self.ensure_face_target()
			self.fighter.attack(self.target, 'light')
			light_attack = self.fighter.attacks.get('light1', {})
			self.action_cooldown = max(6, int(light_attack.get('duration', 200) / 15))
			return
		else:
			if not target_is_attacking and not getattr(self.target, 'rolling', False) and self.fighter.sp >= SP_COST_SPECIAL:
				self.ensure_face_target()
				self.fighter.attack(self.target, 'special')
				self.action_cooldown = 28
				return
			self.ensure_face_target()
			self.fighter.attack(self.target, 'light')
			self.action_cooldown = 20

	def counterattack(self):
		# Phản công có quy tắc: ưu tiên chiêu đặc biệt nếu có và ở khoảng cách phù hợp
		distance = abs(self.fighter.rect.centerx - self.target.rect.centerx)
		in_range = distance <= (self.close_range + 20)
		if self.fighter.sp >= SP_COST_SPECIAL and self.difficulty in ('MEDIUM', 'HARD') and in_range:
			self.fighter.attack(self.target, 'special')
			self.action_cooldown = 30
			return

		# Nếu không thì dùng đòn light để phản công nhanh
		self.fighter.attack(self.target, 'light')
		self.action_cooldown = 20

	def on_round_start(self):
		"""Được gọi khi round mới bắt đầu để AI khởi tạo lại trạng thái cho mỗi round."""
		if getattr(self.fighter, 'character_type', None) == 'A':
			self.initial_aggression_frames = 60
			# quay mặt về phía đối thủ khi round bắt đầu và A sẽ lao vào
			try:
				self.fighter.flip = False if self.fighter.anchor_x < self.target.anchor_x else True
			except Exception:
				pass
		# reset các cờ mặc định
		self.movement_block_frames = 0
		self.counterattack_ready = False
		# cập nhật anchor_x hiện tại để phát hiện round tiếp theo
		try:
			self._last_anchor_x = self.fighter.anchor_x
		except Exception:
			pass
