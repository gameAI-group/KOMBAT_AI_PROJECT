import random
# --- THAY ĐỔI DUY NHẤT Ở ĐÂY ---
from ..config import SP_COST_SPECIAL # Sửa tên biến cho đúng với file config của bạn

class AIRandom:
    def __init__(self, fighter, target, difficulty): # Thêm difficulty để tương thích
        self.fighter = fighter
        self.target = target
        self.action_cooldown = 0
        self.difficulty = difficulty # Lưu lại độ khó

    # Thêm hàm can_act để tương thích
    def can_act(self):
        return not self.fighter.attacking and not self.fighter.hit and not self.fighter.dead and not self.fighter.rolling

    def update(self):
        """Hàm update chính của AI, được gọi mỗi frame."""
        if not self.can_act():
            self.fighter.ai_move_direction = 0
            return
        
        if self.action_cooldown > 0:
            self.action_cooldown -= 1
            self.decide_movement()
            return
        
        self.decide_attack()

    def decide_movement(self):
        """AI quyết định hướng di chuyển."""
        distance_to_target = abs(self.fighter.rect.centerx - self.target.rect.centerx)

        if distance_to_target > 150:
            if self.fighter.rect.centerx < self.target.rect.centerx:
                self.fighter.ai_move_direction = 1
            else:
                self.fighter.ai_move_direction = -1
        else:
            self.fighter.ai_move_direction = 0
    
    def decide_attack(self):
        """AI quyết định hành động tấn công."""
        distance_to_target = abs(self.fighter.rect.centerx - self.target.rect.centerx)
        
        if distance_to_target < 60:
            if self.fighter.rect.centerx < self.target.rect.centerx:
                self.fighter.ai_move_direction = 1
            else:
                self.fighter.ai_move_direction = -1
            
            if hasattr(self.fighter, 'jump'): self.fighter.jump()
            self.action_cooldown = random.randint(40, 80)
            return

        if distance_to_target > 160:
            self.decide_movement()
            return

        self.fighter.ai_move_direction = 0
        choices = ['attack', 'combo', 'special']
        weights = [50, 30, 20]

        # --- VÀ THAY ĐỔI DUY NHẤT Ở ĐÂY ---
        can_use_special = self.fighter.sp >= SP_COST_SPECIAL # Sửa tên biến
        if not can_use_special:
            choices.pop()
            weights.pop()
            
        chosen_action = random.choices(choices, weights=weights, k=1)[0]
        
        if chosen_action == 'special':
            # Thay đổi cách gọi hàm cho phù hợp
            self.fighter.attack(self.target, 'special') 
        else:
            # Thay đổi cách gọi hàm cho phù hợp
            self.fighter.attack(self.target, 'light') 
        
        self.action_cooldown = random.randint(30, 90)