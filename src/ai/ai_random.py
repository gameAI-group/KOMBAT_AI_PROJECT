# src/ai/ai_random.py
import random
from ..config import SP_COST_SPECIAL # Sử dụng biến từ file config của bạn

class AIRandom:
    def __init__(self, fighter, target, difficulty=None): # Tham số difficulty không còn tác dụng
        self.fighter = fighter
        self.target = target
        self.action_cooldown = 0

    def update(self):
        """Hàm cập nhật chính của AI, được gọi mỗi frame."""
        # Kiểm tra xem AI có thể hành động không (tương đương hàm can_act() của bạn bạn)
        can_act = not self.fighter.attacking and not self.fighter.hit and not self.fighter.rolling and not self.fighter.dead
        if not can_act:
            self.fighter.ai_move_direction = 0 # Nếu AI bận, không di chuyển
            return
        
        if self.action_cooldown > 0:
            self.action_cooldown -= 1
            # Trong lúc chờ cooldown, AI vẫn có thể di chuyển
            self.decide_movement()
            return
        
        # Nếu không cooldown, AI có thể quyết định tấn công
        self.decide_attack()

    def decide_movement(self):
        """AI quyết định hướng di chuyển."""
        distance_to_target = abs(self.fighter.rect.centerx - self.target.rect.centerx)

        # Nếu ở quá xa (hơn 150px), lại gần
        if distance_to_target > 150:
            if self.fighter.rect.centerx < self.target.rect.centerx:
                self.fighter.ai_move_direction = 1 # Ra lệnh đi sang phải
            else:
                self.fighter.ai_move_direction = -1 # Ra lệnh đi sang trái
        # Nếu ở trong tầm, ngừng di chuyển
        else:
            self.fighter.ai_move_direction = 0 # Ra lệnh đứng yên
    
    def decide_attack(self):
        """AI quyết định hành động tấn công."""
        distance_to_target = abs(self.fighter.rect.centerx - self.target.rect.centerx)

        # 1. HÀNH VI ĐẶC BIỆT: NHẢY QUA ĐẦU NẾU QUÁ GẦN (< 60px)
        if distance_to_target < 60 and not self.fighter.in_air:
            # Xác định hướng để nhảy qua đối thủ
            if self.fighter.rect.centerx < self.target.rect.centerx:
                self.fighter.ai_move_direction = 1 # AI ở bên trái, tiếp tục di chuyển sang phải
            else:
                self.fighter.ai_move_direction = -1 # AI ở bên phải, tiếp tục di chuyển sang trái
            
            # Thực hiện nhảy
            self.fighter.jump()
            # Đặt cooldown để tránh lặp lại liên tục
            self.action_cooldown = random.randint(40, 80)
            return

        # 2. HÀNH VI DI CHUYỂN: NẾU QUÁ XA (> 160px), CHỈ DI CHUYỂN, KHÔNG TẤN CÔNG
        if distance_to_target > 160:
            self.decide_movement()
            return

        # 3. HÀNH VI TẤN CÔNG: NẾU Ở TRONG TẦM (60px - 160px)
        self.fighter.ai_move_direction = 0 # Dừng di chuyển để tấn công

        # Chọn loại tấn công: Tấn công thường hay Đặc biệt
        choices = ['light', 'special']
        # Tỷ lệ 80% đánh thường, 20% dùng chiêu đặc biệt (gộp 'attack' và 'combo')
        weights = [80, 20] 

        can_use_special = self.fighter.sp >= SP_COST_SPECIAL
        if not can_use_special:
            # Nếu không đủ SP, bỏ lựa chọn 'special'
            choices.pop()
            weights.pop()

        # Chọn một hành động ngẫu nhiên
        chosen_action = random.choices(choices, weights=weights, k=1)[0]
        
        if chosen_action == 'special':
            self.fighter.attack(self.target, 'special')
        else: 
            attack_type = 'air' if self.fighter.in_air else 'light'
            self.fighter.attack(self.target, attack_type)

        # Đặt cooldown sau khi tấn công
        self.action_cooldown = random.randint(30, 90)