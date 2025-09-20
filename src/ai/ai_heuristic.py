# src/ai/ai_heuristic.py
import random
from collections import deque
from ..fighter import Fighter
from ..config import SP_COST_SPECIAL, SP_COST_ROLL, SP_COST_TECH_ROLL, TECH_ROLL_WINDOW

class AIHeuristic:
    def __init__(self, ai_fighter: Fighter, player_fighter: Fighter, difficulty: str = 'Hard'):
        self.ai = ai_fighter
        self.player = player_fighter
        
        # === CÁC THAM SỐ CHIẾN THUẬT CƠ BẢN ===
        self.ATTACK_RANGE = 120
        self.REACTION_RANGE = 160 # Tăng nhẹ phạm vi phản ứng
        self.AERIAL_ENGAGE_RANGE = 200

        # === HỆ THỐNG GHI NHỚ (HEURISTIC CORE) ===
        self.HISTORY_LENGTH = 5  # Ghi nhớ 5 hành động gần nhất của player
        self.SPAM_THRESHOLD = 3  # Coi là spam nếu player lặp lại hành động 3 lần
        
        self.player_action_history = deque(maxlen=self.HISTORY_LENGTH)
        # Key: hành động của player (vd: 'light_attack'), Value: hành động của AI (vd: 'defend')
        self.last_responses = {}

        # === CÁC THAM SỐ ĐIỀU CHỈNH THEO ĐỘ KHÓ ===
        # Vì bạn yêu cầu chế độ Khó, các tham số này được đặt ở mức cao
        self.JUMP_REACTION_CHANCE = 0.75   # 75% cơ hội nhảy theo để không chiến
        self.DODGE_CHANCE = 0.60         # 60% ưu tiên lướt né thay vì đỡ đòn
        self.SPECIAL_ATTACK_CHANCE = 0.70  # 70% dùng chiêu đặc biệt khi có cơ hội
        self.COUNTER_ATTACK_CHANCE = 0.85  # 85% cơ hội kích hoạt logic chống spam
        self.TECH_ROLL_CHANCE = 0.80     # 80% cơ hội thực hiện Thoát Combo khi bị đánh

    def _get_player_current_action(self) -> str:
        """Phân tích và trả về hành động hiện tại của người chơi."""
        if self.player.attacking:
            # Dựa vào self.action của player để biết chính xác đòn tấn công
            if 'special' in self.player.action: return 'special_attack'
            if 'air' in self.player.action: return 'air_attack'
            return 'light_attack' # Bao gồm light1, light2, light3
        if self.player.in_air: return 'jump'
        if self.player.defending: return 'defend'
        if self.player.rolling: return 'roll'
        if self.player.moving: return 'moving'
        return 'idle'

    def update(self):
        # --- BƯỚC 0: RESET VÀ KIỂM TRA TRẠNG THÁI ---
        self.ai.ai_move_direction = 0
        if not self.ai.defending:
            self.ai.defend(False)

        # --- QUY TẮC ƯU TIÊN #1: PHẢN ỨNG SỐNG CÒN (THOÁT COMBO) ---
        # AI ở chế độ Khó phải biết dùng Tech Roll
        if self.ai.hit and not self.ai.rolling:
             if pygame.time.get_ticks() - self.ai.hit_stun_timer < TECH_ROLL_WINDOW:
                if self.ai.sp >= SP_COST_TECH_ROLL and random.random() < self.TECH_ROLL_CHANCE:
                    self.ai.roll() # Hàm roll trong fighter.py đã có logic xử lý tech roll
                    return # Thoát combo là ưu tiên cao nhất, không cần suy nghĩ thêm

        # Dừng mọi hành động khác nếu không thể hành động
        if not self.ai.can_act():
            return
            
        # Luôn cập nhật hướng mặt của AI
        if self.player.hurtbox.centerx < self.ai.hurtbox.centerx: self.ai.flip = True
        else: self.ai.flip = False
            
        distance = abs(self.ai.hurtbox.centerx - self.player.hurtbox.centerx)

        # --- BƯỚC 1: QUAN SÁT VÀ GHI NHỚ ---
        player_action = self._get_player_current_action()
        # Chỉ ghi lại hành động mới để tránh lấp đầy lịch sử bằng một hành động kéo dài (vd: 'moving')
        if not self.player_action_history or self.player_action_history[-1] != player_action:
            self.player_action_history.append(player_action)

        # --- BƯỚC 2: PHÂN TÍCH VÀ PHẢN CÔNG THÍCH ỨNG (LOGIC HEURISTIC) ---
        recent_actions = list(self.player_action_history)
        if len(recent_actions) >= self.SPAM_THRESHOLD:
            # Kiểm tra xem N hành động cuối cùng có giống nhau không
            if len(set(recent_actions[-self.SPAM_THRESHOLD:])) == 1 and player_action != 'idle':
                
                # Player đang spam, AI sẽ tìm cách phản công khác lần trước
                if random.random() < self.COUNTER_ATTACK_CHANCE:
                    last_response = self.last_responses.get(player_action)
                    
                    possible_counters = []
                    # Logic phản công dựa trên hành động của player
                    if player_action in ['light_attack', 'special_attack']:
                        possible_counters = ['defend', 'roll', 'trade_attack']
                    elif player_action == 'defend': # Nếu player spam thủ
                        possible_counters = ['wait', 'special_attack'] # Chờ hoặc dùng chiêu đặc biệt
                    
                    if last_response in possible_counters:
                        possible_counters.remove(last_response) # Không lặp lại hành động cũ

                    if possible_counters:
                        chosen_counter = random.choice(possible_counters)
                        self.last_responses[player_action] = chosen_counter # Ghi nhớ phản ứng mới
                        
                        # Thực hiện hành động phản công
                        if chosen_counter == 'defend': self.ai.defend(True)
                        elif chosen_counter == 'roll' and self.ai.sp >= SP_COST_ROLL: self.ai.roll()
                        elif chosen_counter == 'trade_attack': self.ai.attack(self.player, 'light')
                        elif chosen_counter == 'special_attack' and self.ai.sp >= SP_COST_SPECIAL: self.ai.attack(self.player, 'special')
                        # 'wait' không làm gì cả, chỉ đứng im chờ đợi
                        
                        return # Đã ra quyết định, kết thúc lượt

        # --- BƯỚC 3: HÀNH VI MẶC ĐỊNH (FALLBACK TO RULE-BASED NÂNG CAO) ---
        
        # Quy tắc #2: Tác chiến trên không
        if self.ai.in_air:
            if distance < self.ATTACK_RANGE + 30: self.ai.attack(self.player, 'air')
            return
        if self.player.in_air:
            if distance < self.AERIAL_ENGAGE_RANGE and random.random() < self.JUMP_REACTION_CHANCE:
                self.ai.jump()
            return

        # Quy tắc #3: Phản ứng phòng thủ trên mặt đất
        if self.player.attacking and distance < self.REACTION_RANGE:
            if self.ai.sp >= SP_COST_ROLL and random.random() < self.DODGE_CHANCE:
                self.ai.roll()
            else:
                self.ai.defend(True)
            return

        # Quy tắc #4: Tấn công chủ động
        if distance < self.ATTACK_RANGE:
            self.ai.ai_move_direction = 0
            # AI 'Khó' sẽ rất tích cực dùng chiêu cuối khi có đủ SP
            if self.ai.sp >= SP_COST_SPECIAL and random.random() < self.SPECIAL_ATTACK_CHANCE:
                self.ai.attack(self.player, 'special')
            else:
                self.ai.attack(self.player, 'light')
            return

        # Quy tắc #5: Áp sát (Mặc định)
        self.ai.ai_move_direction = -1 if self.ai.flip else 1