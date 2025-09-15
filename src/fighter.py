# src/fighter.py
import pygame
import os
from .config import *

class Fighter:
    def __init__(self, character_type, x, y, is_player_one):
        self.character_type = character_type
        self.is_player_one = is_player_one
        
        self.stats = CHAR_A_STATS if character_type == 'A' else CHAR_B_STATS
            
        self.name = self.stats['name']
        self.max_hp = self.stats['max_hp']
        self.hp = self.max_hp
        self.max_sp = self.stats['max_sp']
        self.sp = self.max_sp
        self.speed = self.stats['speed']
        self.damage_reduction = self.stats['damage_reduction']

        self.action = 'idle'
        self.moving = False
        self.attacking = False
        self.defending = False
        self.hit = False
        self.in_air = True
        self.dead = False
        self.flip = not is_player_one

        self.combo_step = 0
        self.last_attack_time = 0
        
        self.rolling = False
        self.roll_start_time = 0
        self.roll_cooldown_timer = 0

        self.hit_stun_timer = 0
        self.current_stun_duration = 0
        self.passive_sp_timer = pygame.time.get_ticks()
        
        self.vel_y = 0

        # ===> THÊM MỚI: Biến để AI điều khiển <===
        self.move_direction = 0 # -1: left, 1: right, 0: stop

        self.animation_speeds = self.stats.get('animation_speeds', {})
        self.animations = self.load_animations(self.stats['animations'])
        self.frame_index = 0
        self.image = self.animations[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()

        self.anchor_x = x
        self.anchor_y = y
        self.rect = pygame.Rect((x - 40, y - 90), (80, 180))

    # ... (các hàm load_animations, can_act, set_action, gain_sp, use_sp, take_hit, attack, etc. giữ nguyên) ...
    def load_animations(self, animation_paths):
        animation_dict = {}
        for action, path in animation_paths.items():
            if not os.path.exists(path):
                print(f"Cảnh báo: Không tìm thấy thư mục animation: {path}. Action '{action}' sẽ bị bỏ qua.")
                continue
            
            animation_frames = []
            files = sorted([f for f in os.listdir(path) if f.endswith('.png')])
            for filename in files:
                img_path = os.path.join(path, filename)
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                animation_frames.append(img)
            
            if not animation_frames:
                print(f"Cảnh báo: Không có file PNG nào trong {path}. Dùng placeholder.")
                animation_frames.append(pygame.Surface((150, 300)))
                
            animation_dict[action] = animation_frames
        return animation_dict

    def can_act(self):
        return not self.hit and not self.attacking and not self.dead and not self.rolling

    def set_action(self, new_action):
        if self.action != new_action and new_action in self.animations:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def gain_sp(self, amount):
        self.sp = min(self.sp + amount, self.max_sp)

    def use_sp(self, cost):
        if self.sp >= cost:
            self.sp -= cost
            return True
        return False
        
    def take_hit(self, damage, attacker, is_knockback=False, stun_duration=DEFAULT_STUN_DURATION):
        if self.rolling:
            return

        final_damage = damage * (1 - self.damage_reduction) if self.defending else damage
        self.hp = max(self.hp - final_damage, 0)
        
        if self.defending and 'sp_gain_on_defend' in self.stats:
            self.gain_sp(self.stats['sp_gain_on_defend'])

        if is_knockback and not self.defending:
            if attacker.rect.centerx < self.rect.centerx:
                self.anchor_x += KNOCKBACK_DISTANCE
            else:
                self.anchor_x -= KNOCKBACK_DISTANCE

        if self.hp == 0:
            self.dead = True
            self.set_action('death')
        else:
            self.hit = True
            self.hit_stun_timer = pygame.time.get_ticks()
            self.current_stun_duration = stun_duration
            self.set_action('take_hit')
        
        self.gain_sp(self.stats['sp_gain_on_get_hit'])

    def attack(self, target):
        if not self.can_act():
            return

        current_time = pygame.time.get_ticks()
        
        if self.in_air:
            self.attacking = True
            self.set_action('air_atk')
            damage = self.stats['damage_air']
            target.take_hit(damage, attacker=self)
            self.gain_sp(self.stats['sp_gain_on_hit'])
            return

        if current_time - self.last_attack_time > COMBO_WINDOW:
            self.combo_step = 1
        else:
            self.combo_step += 1

        if self.combo_step > 3: self.combo_step = 1
        
        self.attacking = True
        self.last_attack_time = current_time
        
        damage = 0; is_knockback = False; stun = DEFAULT_STUN_DURATION

        if self.combo_step == 1:
            self.set_action('1_atk'); damage = self.stats['damage_light']; stun = STUN_LIGHT
        elif self.combo_step == 2:
            self.set_action('2_atk'); damage = self.stats['damage_chain']; stun = STUN_CHAIN
        elif self.combo_step == 3:
            self.set_action('3_atk'); damage = self.stats['damage_ender']; is_knockback = True; stun = STUN_ENDER
            if 'sp_gain_on_combo_ender' in self.stats: self.gain_sp(self.stats['sp_gain_on_combo_ender'])

        target.take_hit(damage, attacker=self, is_knockback=is_knockback, stun_duration=stun)
        self.gain_sp(self.stats['sp_gain_on_hit'])

    def special_attack(self, target):
        if not self.can_act(): return
        if self.use_sp(SPECIAL_ATTACK_COST):
            self.attacking = True
            self.set_action('sp_atk')
            damage = self.stats['special_damage']
            is_knockback = self.character_type == 'A'
            target.take_hit(damage, attacker=self, is_knockback=is_knockback)

    def roll(self):
        current_time = pygame.time.get_ticks()
        if self.can_act() and current_time > self.roll_cooldown_timer:
            self.rolling = True; self.roll_start_time = current_time
            self.roll_cooldown_timer = current_time + ROLL_COOLDOWN
            self.set_action('roll')
            roll_distance = 150
            self.anchor_x += roll_distance if not self.flip else -roll_distance

    def jump(self):
        if not self.in_air and self.can_act():
            self.vel_y = JUMP_POWER
            self.in_air = True
    
    # ===> NÂNG CẤP HÀM MOVE <===
    def move(self, target):
        dx, dy = 0, 0
        self.moving = False
        self.defending = False

        if self.dead: return

        keys = pygame.key.get_pressed()

        # Xử lý input (Player hoặc AI)
        if not self.attacking and not self.hit:
            # Nếu là người chơi, đọc bàn phím
            if self.is_player_one:
                if keys[pygame.K_d] and not self.in_air:
                    self.defending = True
                
                if not self.defending:
                    if keys[pygame.K_LEFT]:
                        dx = -self.speed; self.flip = True; self.moving = True
                    if keys[pygame.K_RIGHT]:
                        dx = self.speed; self.flip = False; self.moving = True
            # Nếu là AI, đọc lệnh di chuyển
            else:
                if self.move_direction == -1:
                    dx = -self.speed; self.flip = True; self.moving = True
                elif self.move_direction == 1:
                    dx = self.speed; self.flip = False; self.moving = True
        
        # Áp dụng vật lý (chung cho cả hai)
        self.vel_y += GRAVITY
        dy += self.vel_y
        
        if self.anchor_y + dy > GROUND_Y:
            dy = GROUND_Y - self.anchor_y
            self.in_air = False
            self.vel_y = 0
        else:
            self.in_air = True # Nếu không chạm đất -> đang ở trên không
        
        # Xử lý va chạm (chung cho cả hai)
        if self.rect.left + dx < 0: dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH: dx = SCREEN_WIDTH - self.rect.right
        
        temp_rect = self.rect.copy()
        temp_rect.x += dx
        if temp_rect.colliderect(target.rect) and not self.in_air and not target.in_air:
            dx = 0

        # Cập nhật vị trí
        self.anchor_x += dx
        self.anchor_y += dy

    # ... (các hàm còn lại giữ nguyên) ...
    def update_timers(self):
        current_time = pygame.time.get_ticks()
        if self.hit and current_time - self.hit_stun_timer > self.current_stun_duration:
            self.hit = False; self.combo_step = 0
        
        if self.rolling and current_time - self.roll_start_time > ROLL_DURATION:
            self.rolling = False

        if not self.attacking and not self.hit and not self.dead:
            if current_time - self.passive_sp_timer > PASSIVE_SP_GAIN_RATE:
                self.gain_sp(PASSIVE_SP_GAIN_AMOUNT); self.passive_sp_timer = current_time
    
    def update_animation(self):
        current_cooldown = self.animation_speeds.get(self.action, ANIMATION_COOLDOWN)
        
        if self.action == 'death':
            # Khi chết, animation death sẽ chạy hết các frame và dừng ở frame cuối cùng
            if self.frame_index < len(self.animations.get('death', [])) - 1:
                if pygame.time.get_ticks() - self.update_time > current_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    self.frame_index += 1
            # Không reset frame_index về 0 khi chết
        elif self.frame_index >= len(self.animations.get(self.action, [])):
            if self.action in ['1_atk', '2_atk', '3_atk', 'sp_atk', 'air_atk', 'take_hit', 'roll']:
                if self.attacking: self.attacking = False
                self.set_action('idle')
                if self.action not in ['1_atk', '2_atk']: self.combo_step = 0
            else:
                self.frame_index = 0

        if self.action in self.animations and self.animations[self.action]:
            self.image = self.animations[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > current_cooldown:
                self.update_time = pygame.time.get_ticks(); self.frame_index += 1
        else:
             self.image = pygame.Surface((150, 300))

    def update(self):
        self.update_timers()
        # Nếu chết thì chỉ chạy animation death, không chuyển sang trạng thái khác
        if self.dead:
            if self.action != 'death':
                self.set_action('death')
            # Không chuyển sang trạng thái khác khi chết
            return
        elif self.hit:
            self.set_action('take_hit')
        elif self.rolling:
            self.set_action('roll')
        elif self.attacking: pass
        elif self.defending: self.set_action('defend')
        elif self.in_air: self.set_action('jump_up' if self.vel_y < 0 else 'jump_down')
        elif self.moving: self.set_action('run')
        else: self.set_action('idle')

        self.update_animation()
        self.rect.midbottom = (self.anchor_x, self.anchor_y)

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        img_rect = flipped_image.get_rect(center=self.rect.center)
        surface.blit(flipped_image, img_rect)