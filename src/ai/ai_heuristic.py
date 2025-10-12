import random
from collections import deque, defaultdict, Counter
import pygame

# Import các lớp và hằng số cần thiết từ project của bạn
# Giả định cấu trúc thư mục của bạn là đúng
from ..fighter import Fighter
from ..config import SP_COST_SPECIAL, SP_COST_ROLL, SP_COST_TECH_ROLL, TECH_ROLL_WINDOW

class AIHeuristic:
    def __init__(self, ai_fighter: Fighter, player_fighter: Fighter, difficulty: str = 'Hard'):
        """
        Khởi tạo AI Heuristic.
        - ai_fighter: Đối tượng Fighter mà AI này sẽ điều khiển.
        - player_fighter: Đối tượng Fighter của người chơi để AI theo dõi.
        - difficulty: Độ khó (hiện tại chưa dùng để thay đổi nhiều tham số, nhưng có thể mở rộng).
        """
        self.ai = ai_fighter
        self.player = player_fighter

        # === CÁC THAM SỐ CHIẾN THUẬT CƠ BẢN ===
        self.ATTACK_RANGE = 120  # Khoảng cách tối ưu để tấn công thường
        self.REACTION_RANGE = 160 # Khoảng cách mà AI sẽ phản ứng (né, đỡ) với đòn đánh của người chơi
        self.AERIAL_ENGAGE_RANGE = 200 # Khoảng cách để AI nhảy lên không chiến

        # === HỆ THỐNG GHI NHỚ (HEURISTIC CORE) ===
        self.HISTORY_LENGTH = 10  # Ghi nhớ 10 hành động gần nhất của người chơi
        self.SPAM_THRESHOLD = 3   # Nếu 3 hành động cuối giống hệt nhau, coi là spam

        self.player_action_history = deque(maxlen=self.HISTORY_LENGTH)
        self.last_responses = {} # Lưu lại cách AI đã phản ứng với một hành động spam để lần sau chọn cách khác

        # === HỆ THỐNG NHẬN DIỆN PATTERN VÀ DỰ ĐOÁN ===
        # Key: một tuple các hành động (pattern), vd: ('jump', 'air_attack')
        # Value: một Counter đếm các hành động theo sau pattern đó, vd: Counter({'light_attack': 5, 'defend': 1})
        self.pattern_memory = defaultdict(Counter)
        self.PATTERN_MIN_OCCURRENCES = 3 # Pattern phải xuất hiện ít nhất 3 lần mới đáng tin cậy
        self.PATTERN_SIZES = [3, 2]      # Ưu tiên tìm pattern dài (3 hành động) trước, rồi đến pattern ngắn hơn

        # === CÁC THAM SỐ ĐIỀU CHỈNH HÀNH VI (CÓ THỂ THAY ĐỔI THEO ĐỘ KHÓ) ===
        self.JUMP_REACTION_CHANCE = 0.75   # 75% cơ hội nhảy theo khi người chơi nhảy
        self.DODGE_CHANCE = 0.60           # 60% cơ hội né đòn thay vì đỡ
        self.SPECIAL_ATTACK_CHANCE = 0.70  # 70% cơ hội dùng chiêu đặc biệt khi đủ SP và trong tầm
        self.COUNTER_ATTACK_CHANCE = 0.85  # 85% cơ hội phản công khi phát hiện spam
        self.TECH_ROLL_CHANCE = 0.80       # 80% cơ hội thực hiện "tech roll" để thoát combo
        self.PREDICTION_SUCCESS_CHANCE = 0.80 # 80% cơ hội tin vào dự đoán và hành động theo

    def _get_player_current_action(self) -> str:
        """Phân tích và trả về một chuỗi đại diện cho hành động hiện tại của người chơi."""
        if self.player.attacking:
            if 'special' in self.player.action: return 'special_attack'
            if 'air' in self.player.action: return 'air_attack'
            return 'light_attack'
        if self.player.in_air: return 'jump'
        if self.player.defending: return 'defend'
        if self.player.rolling: return 'roll'
        if self.player.moving: return 'moving'
        return 'idle'

    def _update_pattern_memory(self):
        """Cập nhật kho dữ liệu pattern dựa trên lịch sử hành động của người chơi."""
        history = list(self.player_action_history)
        if len(history) < 2:
            return

        # Cập nhật cho các pattern có độ dài khác nhau đã định nghĩa trong PATTERN_SIZES
        for size in self.PATTERN_SIZES:
            # Pattern phải có ít nhất `size` hành động cộng với hành động kết quả (tổng `size` + 1)
            if len(history) > size:
                # Lấy pattern từ lịch sử
                pattern = tuple(history[-(size + 1) : -1])
                # Lấy hành động diễn ra ngay sau pattern đó
                next_action = history[-1]
                # Ghi nhận rằng sau `pattern` này, `next_action` đã xảy ra
                self.pattern_memory[pattern].update([next_action])

    def _predict_and_counter(self) -> bool:
        """
        Cố gắng dự đoán hành động tiếp theo của người chơi và thực hiện phản công.
        Trả về True nếu một hành động phản công đã được thực hiện, ngược lại trả về False.
        """
        history = list(self.player_action_history)
        if len(history) < min(self.PATTERN_SIZES):
            return False

        # Duyệt qua các kích thước pattern, ưu tiên pattern dài hơn
        for size in self.PATTERN_SIZES:
            if len(history) >= size:
                current_pattern = tuple(history[-size:])

                if current_pattern in self.pattern_memory:
                    predictions = self.pattern_memory[current_pattern]
                    total_occurrences = sum(predictions.values())

                    # Chỉ tin vào dự đoán nếu pattern đã xảy ra đủ nhiều lần
                    if total_occurrences >= self.PATTERN_MIN_OCCURRENCES:
                        predicted_action, _ = predictions.most_common(1)[0]

                        # Thêm một lớp ngẫu nhiên để AI không phải lúc nào cũng hoàn hảo
                        if random.random() < self.PREDICTION_SUCCESS_CHANCE:
                            print(f"[AI LOG] Detected pattern {current_pattern}, predicting '{predicted_action}'. Choosing counter.")
                            # Logic phản công dựa trên hành động được dự đoán
                            if predicted_action in ['light_attack', 'special_attack']:
                                # Dự đoán người chơi sắp tấn công -> đỡ đòn trước
                                self.ai.defend(True)
                                return True
                            elif predicted_action == 'jump':
                                # Dự đoán người chơi sắp nhảy -> nhảy theo để không chiến
                                if abs(self.ai.hurtbox.centerx - self.player.hurtbox.centerx) < self.AERIAL_ENGAGE_RANGE:
                                    self.ai.jump()
                                    return True
        return False

    def update(self):
        """Hàm cập nhật chính, được gọi mỗi frame trong vòng lặp game."""
        # --- BƯỚC 0: RESET TRẠNG THÁI VÀ KIỂM TRA ĐIỀU KIỆN ---
        self.ai.ai_move_direction = 0
        self.ai.defend(False) # Ngừng đỡ đòn vào đầu mỗi lượt quyết định

        # --- QUY TẮC ƯU TIÊN #1: PHẢN ỨNG SỐNG CÒN (QUAN TRỌNG NHẤT) ---
        # Nếu AI đang bị trúng đòn và chưa lăn, hãy thử "tech roll"
        if self.ai.hit and not self.ai.rolling:
             # Kiểm tra xem có đang trong "cửa sổ" thời gian cho phép tech roll không
             if pygame.time.get_ticks() - self.ai.hit_stun_timer < TECH_ROLL_WINDOW:
                # Kiểm tra đủ SP và có cơ hội thành công
                if self.ai.sp >= SP_COST_TECH_ROLL and random.random() < self.TECH_ROLL_CHANCE:
                    self.ai.roll()
                    return # Thực hiện hành động và kết thúc lượt ngay lập tức

        # Nếu AI không thể hành động (đang tấn công, bị choáng, chết, v.v.), bỏ qua
        if not self.ai.can_act():
            return

        # Luôn xoay mặt về phía người chơi
        if self.player.hurtbox.centerx < self.ai.hurtbox.centerx:
            self.ai.flip = True
        else:
            self.ai.flip = False

        distance = abs(self.ai.hurtbox.centerx - self.player.hurtbox.centerx)

        # --- BƯỚC 1: QUAN SÁT, GHI NHỚ VÀ HỌC PATTERN ---
        player_action = self._get_player_current_action()
        # Chỉ ghi lại hành động mới và khác hành động cuối cùng
        if not self.player_action_history or self.player_action_history[-1] != player_action:
            if player_action != 'idle': # Không cần học từ trạng thái đứng yên
                self.player_action_history.append(player_action)
                self._update_pattern_memory() # Cập nhật kho pattern

        # --- BƯỚC 2: DỰ ĐOÁN VÀ PHẢN CÔNG DỰA TRÊN PATTERN ---
        if self._predict_and_counter():
            return # Nếu đã hành động dựa trên dự đoán, kết thúc lượt

        # --- BƯỚC 3: PHẢN CÔNG THÍCH ỨNG (CHỐNG SPAM) ---
        recent_actions = list(self.player_action_history)
        if len(recent_actions) >= self.SPAM_THRESHOLD:
            # Kiểm tra nếu các hành động gần nhất đều giống nhau
            if len(set(recent_actions[-self.SPAM_THRESHOLD:])) == 1:
                spammed_action = recent_actions[-1]
                if random.random() < self.COUNTER_ATTACK_CHANCE:
                    possible_counters = []
                    if spammed_action in ['light_attack', 'special_attack']:
                        possible_counters = ['defend', 'roll', 'trade_attack']
                    elif spammed_action == 'defend':
                        possible_counters = ['wait', 'special_attack']

                    # Tránh lặp lại cách phản công cũ
                    last_response = self.last_responses.get(spammed_action)
                    if last_response in possible_counters and len(possible_counters) > 1:
                        possible_counters.remove(last_response)

                    if possible_counters:
                        chosen_counter = random.choice(possible_counters)
                        self.last_responses[spammed_action] = chosen_counter
                        print(f"[AI LOG] Detected spam of '{spammed_action}', countering with '{chosen_counter}'.")

                        if chosen_counter == 'defend': self.ai.defend(True)
                        elif chosen_counter == 'roll' and self.ai.sp >= SP_COST_ROLL: self.ai.roll()
                        elif chosen_counter == 'trade_attack': self.ai.attack(self.player, 'light')
                        elif chosen_counter == 'special_attack' and self.ai.sp >= SP_COST_SPECIAL: self.ai.attack(self.player, 'special')
                        return

        # --- BƯỚC 4: HÀNH VI MẶC ĐỊNH (RULE-BASED) NẾU KHÔNG CÓ LOGIC NÂNG CAO NÀO ĐƯỢC KÍCH HOẠT ---
        # Xử lý khi AI đang ở trên không
        if self.ai.in_air:
            if distance < self.ATTACK_RANGE + 30: self.ai.attack(self.player, 'air')
            return

        # Phản ứng khi người chơi ở trên không
        if self.player.in_air:
            if distance < self.AERIAL_ENGAGE_RANGE and random.random() < self.JUMP_REACTION_CHANCE:
                self.ai.jump()
            return

        # Phản ứng khi người chơi đang tấn công gần
        if self.player.attacking and distance < self.REACTION_RANGE:
            if self.ai.sp >= SP_COST_ROLL and random.random() < self.DODGE_CHANCE:
                self.ai.roll()
            else:
                self.ai.defend(True)
            return

        # Tấn công khi ở trong tầm
        if distance < self.ATTACK_RANGE:
            self.ai.ai_move_direction = 0 # Đứng yên để tấn công
            if self.ai.sp >= SP_COST_SPECIAL and random.random() < self.SPECIAL_ATTACK_CHANCE:
                self.ai.attack(self.player, 'special')
            else:
                self.ai.attack(self.player, 'light')
            return

        # Nếu không có hành động nào khác, di chuyển về phía người chơi
        self.ai.ai_move_direction = -1 if self.ai.flip else 1