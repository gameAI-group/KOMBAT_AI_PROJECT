import pygame, os, random
from .config import *

DEBUG_DRAW = True

class Fighter:
    def __init__(self, character_type, x, y, is_player_one):
        # ... (khởi tạo giữ nguyên) ...
        self.character_type = character_type; self.is_player_one = is_player_one
        if self.character_type == 'A': self.stats = CHAR_A_STATS
        else: self.stats = CHAR_B_STATS
        self.name = self.stats['name']; self.max_hp = self.stats['max_hp']
        self.max_sp = self.stats['max_sp']
        self.speed = self.stats['speed']; self.air_speed = self.stats['air_speed']
        self.attacks = self.stats['attacks']; self.defense_modifier = self.stats['defense_modifier']
        self.sp_gain_on_hit = self.stats['sp_gain_on_hit']; self.sp_gain_on_get_hit = self.stats['sp_gain_on_get_hit']
        self.start_x, self.start_y = x, y
        self.reset()
        self.animation_speeds = self.stats.get('animation_speeds', {})
        self.animations = self.load_animations()
        self.image = self.animations[self.action][self.frame_index]
        pushbox_width = 60; pushbox_height = 30
        self.pushbox_offset_x = 0; self.pushbox_offset_y = 200
        self.rect = pygame.Rect((0, 0), (pushbox_width, pushbox_height))
        hurtbox_width = 120; hurtbox_height = 140
        self.hurtbox_offset_x = 0; self.hurtbox_offset_y = 110
        self.hurtbox = pygame.Rect((0, 0), (hurtbox_width, hurtbox_height))
        self.hitbox = None
        self.attack_hitbox_width = 100; self.attack_hitbox_height = 170
        self.attack_hitbox_offset_x = 10; self.attack_hitbox_offset_y = -170

    def reset(self):
        self.hp = self.max_hp
        self.sp = self.max_sp
        self.anchor_x, self.anchor_y = self.start_x, self.start_y
        self.action = 'idle'; self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.moving = False; self.attacking = False; self.defending = False
        self.hit = False; self.in_air = True; self.dead = False; self.rolling = False
        self.flip = not self.is_player_one; self.attack_hit_this_frame = False
        self.vel_y = 0; self.knockback_vel_x = 0
        self.combo_step = 0; self.combo_input_timer = 0
        self.hits_landed_count = 0; self.jumps_left = 2; self.roll_velocity_x = 0
        self.air_attacks_left = 2; self.air_rolls_left = 1
        self.attack_timer = 0; self.attack_cooldown = 0; self.hit_stun_timer = 0
        self.roll_timer = 0; self.roll_cooldown_timer = 0
        self.passive_sp_timer = pygame.time.get_ticks()
        self.hit_stun_duration = 0
        self.ai_move_direction = 0
        self.invincible = False
        self.last_special_time = -SPECIAL_ATTACK_COOLDOWN
        # --- MỚI: Thêm trạng thái lướt xuyên thấu ---
        self.tech_rolling = False

    # ... (load_animations, can_act, load_frames, gain_sp, use_sp, attack... giữ nguyên) ...
    def load_animations(self):
        animation_dict = {}; all_anim_paths = self.stats['animations'].copy()
        for attack_name, attack_data in self.attacks.items():
            all_anim_paths[attack_name] = attack_data['animation']
        for action, path in all_anim_paths.items(): animation_dict[action] = self.load_frames(path)
        return animation_dict

    def can_act(self):
        return not self.hit and not self.attacking and not self.dead and not self.rolling

    def load_frames(self, path):
        frames = []
        try:
            files = sorted(os.listdir(path)); png_files = [f for f in files if f.endswith('.png')]
            for filename in png_files:
                img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                frames.append(pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)))
        except: print(f"Cảnh báo: Lỗi tải animation từ: {path}")
        return frames if frames else [pygame.Surface((150,300))]

    def gain_sp(self, amount): self.sp = min(self.sp + amount, self.max_sp)
    def use_sp(self, cost):
        if self.sp >= cost: self.sp -= cost; return True
        return False

    def attack(self, target, attack_type):
        if self.attacking and 'light' in self.action and 'light' in attack_type:
            self.combo_input_timer = pygame.time.get_ticks()
            return
        can_act = not self.attacking and not self.hit and not self.defending and not self.rolling and not self.dead
        if not can_act or self.attack_cooldown > 0: return
        if attack_type == 'special':
            if pygame.time.get_ticks() - self.last_special_time < SPECIAL_ATTACK_COOLDOWN:
                return 
            if self.in_air:
                if self.character_type == 'B':
                    if self.use_sp(SP_COST_SPECIAL):
                        self.last_special_time = pygame.time.get_ticks()
                        attack_data = self.attacks['special']; range_info = attack_data.get('range_box')
                        if not range_info: return
                        range_w, range_h = range_info['size']; offset_x, offset_y = range_info['offset']
                        if not self.flip: range_x = self.rect.right + offset_x
                        else: range_x = self.rect.left - range_w - offset_x
                        range_y = self.rect.y + offset_y
                        range_rect = pygame.Rect(range_x, range_y, range_w, range_h)
                        if range_rect.colliderect(target.hurtbox): self.perform_attack('special', target=target)
                        else:
                            rand_x = random.randint(range_rect.left, range_rect.right)
                            self.perform_attack('special', destination_pos=(rand_x, self.anchor_y))
                else:
                    if self.use_sp(SP_COST_SPECIAL):
                        self.last_special_time = pygame.time.get_ticks()
                        self.perform_attack('special', target)
                return
            else:
                if self.character_type == 'B':
                    if self.use_sp(SP_COST_SPECIAL):
                        self.last_special_time = pygame.time.get_ticks()
                        attack_data = self.attacks['special']; range_info = attack_data.get('range_box')
                        if not range_info: return
                        range_w, range_h = range_info['size']; offset_x, offset_y = range_info['offset']
                        if not self.flip: range_x = self.rect.right + offset_x
                        else: range_x = self.rect.left - range_w - offset_x
                        range_y = self.rect.y + offset_y
                        range_rect = pygame.Rect(range_x, range_y, range_w, range_h)
                        if range_rect.colliderect(target.hurtbox): self.perform_attack('special', target=target)
                        else:
                            rand_x = random.randint(range_rect.left, range_rect.right)
                            self.perform_attack('special', destination_pos=(rand_x, self.anchor_y))
                else:
                    if self.use_sp(SP_COST_SPECIAL):
                        self.last_special_time = pygame.time.get_ticks()
                        self.perform_attack('special', target)
            return
        if self.in_air:
            if attack_type == 'air' and 'air' in self.attacks and self.air_attacks_left > 0:
                self.perform_attack('air', target)
                self.air_attacks_left -= 1
        elif attack_type == 'light':
            self.combo_step = 1
            self.perform_attack('light1', target)
            self.combo_input_timer = 0
            
    # ... (perform_attack, check_attack_collision, create_and_check_hitbox, take_hit, defend giữ nguyên) ...
    def perform_attack(self, attack_type, target=None, destination_pos=None):
        if attack_type == 'special' and self.character_type == 'B':
            if destination_pos:
                self.flip = (destination_pos[0] < self.anchor_x)
                self.anchor_x, self.anchor_y = destination_pos[0], destination_pos[1]
            elif target is not None:
                if self.anchor_x < target.anchor_x: self.anchor_x = target.anchor_x - 80; self.flip = False
                else: self.anchor_x = target.anchor_x + 80; self.flip = True
        self.attacking = True; self.action = attack_type
        self.frame_index = 0; self.update_time = pygame.time.get_ticks()
        self.attack_timer = pygame.time.get_ticks()
        self.attack_hit_this_frame = False; self.hits_landed_count = 0
        attack_data = self.attacks.get(attack_type, {})
        self.attack_cooldown = attack_data.get('cooldown', 30)

    def check_attack_collision(self, target):
        if not self.attacking: self.hitbox = None; return
        attack_data = self.attacks.get(self.action)
        if not attack_data: return
        total_hits = attack_data.get('hits', 1)
        if total_hits > 1:
            hit_frames = attack_data.get('hit_frames', [])
            if self.hits_landed_count < total_hits and self.frame_index in hit_frames:
                expected_frame = hit_frames[self.hits_landed_count]
                if self.frame_index == expected_frame: self.create_and_check_hitbox(target, attack_data)
        else:
            if not self.attack_hit_this_frame:
                hit_on_frame = attack_data.get('hit_on_frame', 0)
                if self.frame_index >= hit_on_frame: self.create_and_check_hitbox(target, attack_data)

    def create_and_check_hitbox(self, target, attack_data):
        hitbox_w, hitbox_h = attack_data.get('hitbox_size', (self.attack_hitbox_width, self.attack_hitbox_height))
        offset_x, offset_y = attack_data.get('hitbox_offset', (self.attack_hitbox_offset_x, self.attack_hitbox_offset_y))
        if not self.flip: hitbox_x = self.rect.right + offset_x
        else: hitbox_x = self.rect.left - hitbox_w - offset_x
        hitbox_y = self.rect.y + offset_y
        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, hitbox_w, hitbox_h)
        if self.hitbox.colliderect(target.hurtbox):
            self.hits_landed_count += 1
            knockback = 0
            total_hits = attack_data.get('hits', 1)
            if self.hits_landed_count == total_hits and total_hits > 1: knockback = attack_data.get('knockback_on_last_hit', 0)
            elif total_hits == 1: knockback = attack_data.get('knockback', 0)
            stun = attack_data.get('stun', DEFAULT_HIT_STUN)
            target.take_hit(attack_data['damage'], knockback, stun, self.flip)
            if self.action != 'special': self.gain_sp(self.sp_gain_on_hit)
            if self.character_type == 'B' and self.action == 'light3': self.gain_sp(self.stats['sp_gain_on_combo_finish'])
            if total_hits == 1: self.attack_hit_this_frame = True
    
    def take_hit(self, damage, knockback, stun_duration, attacker_is_flipped):
        if self.dead or self.invincible:
            return
        self.attacking = False
        self.rolling = False 
        self.combo_step = 0
        self.hp -= damage * (self.defense_modifier if self.defending else 1)
        if self.hp <= 0: self.hp = 0; self.dead = True; self.hit = False
        else:
            self.hit = True; self.hit_stun_timer = pygame.time.get_ticks(); self.hit_stun_duration = stun_duration
        self.gain_sp(self.sp_gain_on_get_hit)
        if self.defending and 'sp_gain_on_block' in self.stats: self.gain_sp(self.stats['sp_gain_on_block'])
        direction = 1 if not attacker_is_flipped else -1
        self.knockback_vel_x = knockback * direction

    def defend(self, is_defending):
        if not self.attacking and not self.hit and not self.in_air and not self.rolling: self.defending = is_defending

    def roll(self):
        # --- SỬA ĐỔI: Tách logic lướt thường và lướt khi bị đánh (tech roll) ---
        
        # 1. Logic cho lướt né thông thường
        can_normal_roll = (not self.hit and not self.attacking and not self.defending)
        if can_normal_roll:
            base_condition = (self.roll_cooldown_timer == 0)
            can_roll_on_platform = base_condition and ((not self.in_air) or (self.in_air and self.air_rolls_left > 0))
            if can_roll_on_platform:
                if self.use_sp(SP_COST_ROLL):
                    if self.in_air:
                        self.air_rolls_left -= 1
                    self.rolling = True; self.roll_timer = pygame.time.get_ticks()
                    self.roll_velocity_x = ROLL_SPEED; self.vel_y = 0
                return # Dừng hàm sau khi xử lý xong

        # 2. Logic cho Tech Roll (lướt khi đang bị đánh)
        can_tech_roll = (self.hit and not self.rolling)
        if can_tech_roll:
            # Kiểm tra xem có trong cửa sổ thời gian cho phép không
            if pygame.time.get_ticks() - self.hit_stun_timer < TECH_ROLL_WINDOW:
                if self.use_sp(SP_COST_TECH_ROLL):
                    self.hit = False # Thoát khỏi trạng thái bị đánh
                    self.tech_rolling = True # Bật trạng thái lướt xuyên thấu
                    self.rolling = True # Dùng chung animation và timer của roll
                    self.roll_timer = pygame.time.get_ticks()
                    self.roll_velocity_x = ROLL_SPEED
                    self.roll_cooldown_timer = ROLL_COOLDOWN_DURATION # Vẫn áp dụng hồi chiêu

    def jump(self):
        can_jump = (self.jumps_left > 0 and not self.hit and not self.attacking and not self.defending and not self.rolling)
        if can_jump: self.vel_y = JUMP_POWER; self.in_air = True; self.jumps_left -= 1

    def update(self):
        prev_action = self.action
        if self.dead:
            self.action = 'death'
            self.invincible = False 
        else:
            if self.attack_cooldown > 0: self.attack_cooldown -= 1
            if self.roll_cooldown_timer > 0: self.roll_cooldown_timer -= 1
            if self.hit and pygame.time.get_ticks() - self.hit_stun_timer > self.hit_stun_duration: self.hit = False
            
            # --- SỬA ĐỔI: Cập nhật logic kết thúc roll ---
            if self.rolling:
                elapsed_roll_time = pygame.time.get_ticks() - self.roll_timer
                if ROLL_IFRAME_START <= elapsed_roll_time < (ROLL_IFRAME_START + ROLL_IFRAME_DURATION):
                    self.invincible = True
                else:
                    self.invincible = False
                if elapsed_roll_time > ROLL_DURATION:
                    self.rolling = False
                    self.invincible = False
                    self.tech_rolling = False # Quan trọng: Tắt trạng thái xuyên thấu khi roll kết thúc
                    self.roll_cooldown_timer = ROLL_COOLDOWN_DURATION
                    self.roll_velocity_x = 0
            else:
                self.invincible = False

            if not self.attacking and not self.hit:
                if pygame.time.get_ticks() - self.passive_sp_timer > PASSIVE_SP_GAIN_RATE:
                    self.gain_sp(PASSIVE_SP_GAIN_AMOUNT); self.passive_sp_timer = pygame.time.get_ticks()
            if self.attacking:
                attack_duration = self.attacks.get(self.action, {}).get('duration', 500)
                if pygame.time.get_ticks() - self.attack_timer > attack_duration:
                    is_next_combo_input_valid = (self.combo_input_timer > 0 and pygame.time.get_ticks() - self.combo_input_timer < COMBO_TIMEOUT)
                    if 'light' in self.action and is_next_combo_input_valid:
                        self.combo_step += 1
                        next_attack = f'light{self.combo_step}'
                        if next_attack in self.attacks:
                            self.perform_attack(next_attack, None); self.combo_input_timer = 0
                        else: self.attacking = False; self.combo_step = 0
                    else: self.attacking = False; self.combo_step = 0
            if self.dead: self.action = 'death'
            elif self.defending: self.action = 'defend'
            elif self.hit: self.action = 'take_hit'
            elif self.attacking: pass
            elif self.rolling: self.action = 'roll'
            elif self.in_air: self.action = 'jump_up' if self.vel_y < 0 else 'jump_down'
            elif self.moving: self.action = 'run'
            else: self.action = 'idle'
        if self.action != prev_action:
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        self.update_animation()
        self.rect.center = (self.anchor_x + self.pushbox_offset_x, self.anchor_y + self.pushbox_offset_y)
        self.hurtbox.center = (self.anchor_x + self.hurtbox_offset_x, self.anchor_y + self.hurtbox_offset_y)

    def update_animation(self):
        # ... (update_animation giữ nguyên) ...
        current_cooldown = self.animation_speeds.get(self.action, 100)
        animation_frames = self.animations.get(self.action, [pygame.Surface((1,1))])
        if not animation_frames: return
        if self.frame_index >= len(animation_frames): self.frame_index = 0
        self.image = animation_frames[self.frame_index]
        hold_frame_info = self.stats.get('hold_frames', {}); is_holding_frame = False
        if self.action in hold_frame_info:
            frame_to_hold = hold_frame_info[self.action] - 1
            if self.frame_index >= frame_to_hold:
                self.frame_index = min(frame_to_hold, len(animation_frames) - 1); is_holding_frame = True
        if pygame.time.get_ticks() - self.update_time > current_cooldown and not is_holding_frame:
            self.update_time = pygame.time.get_ticks()
            if not (self.action == 'death' and self.frame_index >= len(animation_frames) - 1): self.frame_index += 1
        if self.frame_index >= len(animation_frames):
            if self.action == 'death': self.frame_index = len(animation_frames) - 1
            elif self.action == 'take_hit': self.frame_index = 0
            else: self.frame_index = 0

    def move(self, target):
        dx = 0; dy = 0; self.moving = False
        can_move_freely = not self.attacking and not self.hit and not self.rolling and not self.dead
        if self.defending: can_move_freely = False
        if self.rolling:
            direction = 1 if not self.flip else -1
            dx += self.roll_velocity_x * direction
        if abs(self.knockback_vel_x) > 0.5: dx += self.knockback_vel_x; self.knockback_vel_x *= 0.8
        else: self.knockback_vel_x = 0
        if self.is_player_one and can_move_freely:
            key = pygame.key.get_pressed(); current_speed = self.air_speed if self.in_air else self.speed
            if key[pygame.K_LEFT]: dx = -current_speed; self.flip = True; self.moving = True
            if key[pygame.K_RIGHT]: dx = current_speed; self.flip = False; self.moving = True
        elif not self.is_player_one and can_move_freely:
            current_speed = self.air_speed if self.in_air else self.speed
            if self.ai_move_direction == -1: dx = -current_speed; self.flip = True; self.moving = True
            elif self.ai_move_direction == 1: dx = current_speed; self.flip = False; self.moving = True
        if (self.attacking and self.in_air) or self.rolling:
            self.vel_y = 0
        else:
            self.vel_y += GRAVITY
        dy += self.vel_y
        if self.rect.left + dx < 0: dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH: dx = SCREEN_WIDTH - self.rect.right
        
        # --- SỬA ĐỔI: Bỏ qua va chạm pushbox khi đang "tech rolling" ---
        temp_rect = self.rect.copy(); temp_rect.x += dx
        if not self.tech_rolling and temp_rect.colliderect(target.rect):
            dx = 0

        if self.rect.bottom + dy > GROUND_Y:
            dy = GROUND_Y - self.rect.bottom
            self.in_air = False; self.vel_y = 0; self.jumps_left = 2
            self.air_attacks_left = 2; self.air_rolls_left = 1
        self.anchor_x += dx; self.anchor_y += dy

    def draw(self, surface):
        # ... (draw giữ nguyên) ...
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.invincible:
            flipped_image.set_alpha(150)
        else:
            flipped_image.set_alpha(255)
        image_rect = flipped_image.get_rect(); image_rect.center = (self.anchor_x, self.anchor_y)
        surface.blit(flipped_image, image_rect.topleft)
        if DEBUG_DRAW:
            pygame.draw.rect(surface, BLUE, self.rect, 2)
            pygame.draw.rect(surface, GREEN, self.hurtbox, 2)
            if self.hitbox:
                hitbox_color = YELLOW if self.action == 'special' else RED
                hitbox_surface = pygame.Surface(self.hitbox.size, pygame.SRCALPHA)
                hitbox_surface.fill((hitbox_color[0], hitbox_color[1], hitbox_color[2], 100))
                surface.blit(hitbox_surface, self.hitbox.topleft)
            if self.character_type == 'B' and not self.attacking:
                attack_data = self.attacks.get('special', {})
                range_info = attack_data.get('range_box')
                if range_info:
                    range_w, range_h = range_info['size']
                    offset_x, offset_y = range_info['offset']
                    if not self.flip: range_x = self.rect.right + offset_x
                    else: range_x = self.rect.left - range_w - offset_x
                    range_y = self.rect.y + offset_y
                    range_rect = pygame.Rect(range_x, range_y, range_w, range_h)
                    pygame.draw.rect(surface, PURPLE, range_rect, 2)