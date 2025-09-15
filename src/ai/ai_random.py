import random
from ..config import SP_COST_SPECIAL

class AIRandom:
    def __init__(self, fighter, target, difficulty):
        self.fighter = fighter
        self.target = target
        self.difficulty = difficulty
        self.action_cooldown = 0

        if self.difficulty == "EASY":
            self.reaction_time = 45; self.attack_chance = 40
        elif self.difficulty == "MEDIUM":
            self.reaction_time = 30; self.attack_chance = 60
        else: # HARD
            self.reaction_time = 15; self.attack_chance = 80

    def can_act_now(self):
        """Kiểm tra xem AI có thể hành động không (không bị khóa và hết cooldown)."""
        return self.fighter.action in ['idle', 'run'] and self.action_cooldown == 0

    def update(self):
        if self.fighter.dead:
            self.fighter.ai_move_direction = 0
            return

        if self.action_cooldown > 0:
            self.action_cooldown -= 1
        
        self.decide_movement()
        
        if self.can_act_now():
            self.decide_action()

    def decide_movement(self):
        distance = abs(self.fighter.anchor_x - self.target.anchor_x)
        
        if distance > 150: # Nếu xa, lại gần
            self.fighter.ai_move_direction = 1 if self.target.anchor_x > self.fighter.anchor_x else -1
        elif distance < 100: # Nếu quá gần, lùi ra
            self.fighter.ai_move_direction = -1 if self.target.anchor_x > self.fighter.anchor_x else 1
        else: # Giữ khoảng cách
            self.fighter.ai_move_direction = 0
    
    def decide_action(self):
        distance = abs(self.fighter.anchor_x - self.target.anchor_x)
        if distance < 120 and random.randint(1, 100) < self.attack_chance:
            self.fighter.ai_move_direction = 0
            
            can_use_special = self.fighter.sp >= SP_COST_SPECIAL
            if can_use_special and random.randint(1, 100) < 35:
                self.fighter.attack(self.target, 'special')
            else:
                self.fighter.attack(self.target, 'light')
            
            self.action_cooldown = self.reaction_time