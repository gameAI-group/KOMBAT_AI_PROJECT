# src/ai/ai_rulebased.py
import random
from ..fighter import Fighter
from ..config import SP_COST_SPECIAL, SP_COST_ROLL

class AIRuleBased:
    def __init__(self, ai_fighter: Fighter, player_fighter: Fighter):
        self.ai = ai_fighter
        self.player = player_fighter
        
        self.ATTACK_RANGE = 120
        self.REACTION_RANGE = 150
        
        # === THÊM CÁC HẰNG SỐ MỚI CHO TÁC CHIẾN TRÊN KHÔNG ===
        self.AERIAL_ENGAGE_RANGE = 200 # Khoảng cách AI sẽ quyết định nhảy lên để tấn công
        self.JUMP_REACTION_CHANCE = 0.6 # 60% cơ hội nhảy theo khi người chơi nhảy
        
        self.DODGE_CHANCE = 0.5
        self.SPECIAL_ATTACK_CHANCE_WHEN_READY = 0.6

    def update(self):
        # Bước 0: Reset hành động & Kiểm tra trạng thái
        self.ai.ai_move_direction = 0
        self.ai.defend(False)

        if not self.ai.can_act():
            return

        # === QUY TẮC #0: LUÔN LUÔN BIẾT BẠN Ở ĐÂU ===
        if self.player.hurtbox.centerx < self.ai.hurtbox.centerx:
            self.ai.flip = True
        else:
            self.ai.flip = False
            
        distance = abs(self.ai.hurtbox.centerx - self.player.hurtbox.centerx)

        # === QUY TẮC #1: TÁC CHIẾN TRÊN KHÔNG (Ưu tiên cao nhất) ===
        
        # A) Nếu AI ĐÃ ở trên không...
        if self.ai.in_air:
            # ...mục tiêu chính của nó là tấn công người chơi nếu ở gần.
            if distance < self.ATTACK_RANGE + 20: # Tầm đánh trên không rộng hơn 1 chút
                self.ai.attack(self.player, 'air')
            # Khi đã ở trên không, AI sẽ không ra quyết định di chuyển hay phòng thủ nữa.
            return

        # B) Nếu NGƯỜI CHƠI ở trên không và AI ở dưới đất...
        if self.player.in_air:
            # ...AI sẽ quyết định có nên nhảy lên để "theo" hay không.
            if distance < self.AERIAL_ENGAGE_RANGE and random.random() < self.JUMP_REACTION_CHANCE:
                self.ai.jump()
                return # Ra quyết định nhảy, kết thúc lượt suy nghĩ

        # === NẾU ĐÃ VƯỢT QUA QUY TẮC 1, CÓ NGHĨA CẢ HAI ĐỀU ĐANG Ở DƯỚI ĐẤT ===

        # === QUY TẮC #2: PHẢN ỨNG PHÒNG THỦ (Mặt đất) ===
        if self.player.attacking and distance < self.REACTION_RANGE:
            if self.ai.sp >= SP_COST_ROLL and random.random() < self.DODGE_CHANCE:
                self.ai.roll()
            else:
                self.ai.defend(True)
            return

        # === QUY TẮC #3: TẤN CÔNG (Mặt đất) ===
        elif distance < self.ATTACK_RANGE:
            self.ai.ai_move_direction = 0
            if self.ai.sp >= SP_COST_SPECIAL and random.random() < self.SPECIAL_ATTACK_CHANCE_WHEN_READY:
                self.ai.attack(self.player, 'special')
            else:
                self.ai.attack(self.player, 'light')
            return

        # === QUY TẮC #4: ÁP SÁT (Mặt đất, mặc định) ===
        else:
            self.ai.ai_move_direction = -1 if self.ai.flip else 1