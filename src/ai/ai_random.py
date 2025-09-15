# src/ai/ai_random.py
import random
from ..config import SCREEN_WIDTH, SPECIAL_ATTACK_COST

class AIRandom:
    def __init__(self, fighter, target):
        self.fighter = fighter
        self.target = target
        self.action_cooldown = 0

    def update(self):
        """Hàm update chính của AI, được gọi mỗi frame."""
        if not self.fighter.can_act():
            # Nếu AI đang bận (bị đánh, tấn công), reset lệnh di chuyển và không làm gì cả
            self.fighter.move_direction = 0
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

        # Nếu ở quá xa, lại gần
        if distance_to_target > 150:
            if self.fighter.rect.centerx < self.target.rect.centerx:
                self.fighter.move_direction = 1 # Ra lệnh đi sang phải
            else:
                self.fighter.move_direction = -1 # Ra lệnh đi sang trái
        # Nếu ở trong tầm, ngừng di chuyển để tấn công
        else:
            self.fighter.move_direction = 0 # Ra lệnh đứng yên
    
    def decide_attack(self):
        """AI quyết định hành động tấn công."""
        # AI chỉ tấn công khi ở đủ gần
        distance_to_target = abs(self.fighter.rect.centerx - self.target.rect.centerx)
        # Nếu ở rất gần đối thủ, AI sẽ nhảy lên đầu và di chuyển qua phía bên kia
        if distance_to_target < 60:
            # Xác định hướng nhảy qua đối thủ
            if self.fighter.rect.centerx < self.target.rect.centerx:
                # AI ở bên trái, nhảy sang phải
                self.fighter.move_direction = 1
            else:
                # AI ở bên phải, nhảy sang trái
                self.fighter.move_direction = -1
            # Thực hiện nhảy
            if hasattr(self.fighter, 'jump'):
                self.fighter.jump()
            # Đặt cooldown để tránh lặp lại liên tục
            self.action_cooldown = random.randint(40, 80)
            return

        # Nếu xa quá thì chỉ di chuyển
        if distance_to_target > 160:
            self.decide_movement()
            return

        # Nếu đã ở trong tầm đánh, quyết định tấn công như cũ
        self.fighter.move_direction = 0
        choices = ['attack', 'combo', 'special']
        weights = [50, 30, 20]
        can_use_special = self.fighter.sp >= SPECIAL_ATTACK_COST
        if not can_use_special:
            choices.pop()
            weights.pop()
        chosen_action = random.choices(choices, weights=weights, k=1)[0]
        if chosen_action == 'special':
            self.fighter.special_attack(self.target)
        else:
            self.fighter.attack(self.target)
        self.action_cooldown = random.randint(30, 90)