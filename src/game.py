import pygame, sys, os
from .config import *
from .fighter import Fighter
from .ui import (draw_main_menu_screen, draw_character_select_screen,
                 draw_difficulty_select_screen, draw_battle_hud,
                 draw_game_over_screen, draw_round_announcement, DamageText,
                 draw_guide_screen) # Thêm draw_guide_screen
from .ai.ai_random import AIRandom
from .ai.ai_rulebased import AIRuleBased
from .ai.ai_heuristic import AIHeuristic

def load_animation_frames(path):
    if not os.path.isdir(path):
        print(f"Cảnh báo: Không tìm thấy thư mục animation: {path}")
        return []
    frames = []
    for filename in sorted(os.listdir(path)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                frames.append(img)
            except pygame.error as e:
                print(f"Lỗi khi tải frame {filename}: {e}")
    return frames

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "MAIN_MENU"

        self.select_anims = {}
        self.select_frame_index = 0
        self.select_anim_timer = 0
        self.cursor_frames = []
        self.cursor_frame_index = 0
        self.cursor_anim_timer = 0
        
        self.confirmation_timer = 0

        self.damage_text_group = pygame.sprite.Group()
        self.damage_font = pygame.font.Font(FONT_PATH, 28)

        self.load_assets()

        try:
            pygame.mixer.music.load(MUSIC_MENU)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Cảnh báo: Không thể tải nhạc menu: {e}")

        # Biến cho các trạng thái game
        self.start_button_rect, self.guide_button_rect, self.exit_button_rect = None, None, None
        self.back_button_rect = None # Nút quay lại từ màn hình guide
        self.p1_cursor_pos = 0; self.difficulty_cursor_pos = 0
        self.player_choice = None; self.ai_choice = None; self.difficulty_choice = None
        self.char_a_rect, self.char_b_rect = None, None
        self.easy_rect, self.medium_rect, self.hard_rect = None, None, None
        self.replay_button_rect, self.quit_button_rect = None, None
        self.player = None; self.ai = None; self.ai_controller = None
        self.player_rounds_won = 0; self.ai_rounds_won = 0; self.current_round = 1
        self.round_start_time = 0; self.round_timer = ROUND_TIME_LIMIT
        self.round_over = False; self.round_over_time = 0
        self.winner = None
        self.final_winner = None 
        self.round_start_sequence_timer = 0
        self.round_announcement_text = ""; self.round_announcement_step = 0
        
        # --- MỚI: Biến cho việc cuộn trong màn hình hướng dẫn ---
        self.guide_scroll_y = 0
        self.guide_max_scroll = GUIDE_CONTENT_HEIGHT - SCREEN_HEIGHT # Tính toán giới hạn cuộn

    def load_assets(self):
        try:
            temp_bg_main = pygame.image.load(BG_MAIN_MENU).convert()
            self.bg_main_menu = pygame.transform.scale(temp_bg_main, (SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_bg_select = pygame.image.load(BG_CHAR_SELECT).convert()
            self.bg_char_select = pygame.transform.scale(temp_bg_select, (SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_bg_stage = pygame.image.load(BG_STAGE_1).convert()
            self.bg_stage_1 = pygame.transform.scale(temp_bg_stage, (SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_logo = pygame.image.load(LOGO_IMAGE).convert_alpha()
            self.logo_image = pygame.transform.scale(temp_logo, (650, 500))
            self.portrait_a = pygame.image.load(PORTRAIT_A).convert_alpha()
            self.portrait_b = pygame.image.load(PORTRAIT_B).convert_alpha()
            self.portraits = {'A': self.portrait_a, 'B': self.portrait_b}
            self.select_anims['A'] = {
                'idle': load_animation_frames(CHAR_A_STATS['animations']['idle']),
                'confirm': load_animation_frames(CHAR_A_STATS['animations']['jump_up'])
            }
            self.select_anims['B'] = {
                'idle': load_animation_frames(CHAR_B_STATS['animations']['idle']),
                'confirm': load_animation_frames(CHAR_B_STATS['animations']['jump_up'])
            }
            self.cursor_frames = load_animation_frames('assets/images/ui/cursor_anim/')
            if not self.cursor_frames:
                 self.cursor_frames.append(pygame.image.load(CURSOR_P1).convert_alpha())
            self.sfx = {
                'round1': pygame.mixer.Sound(SFX_ROUND_1),
                'round2': pygame.mixer.Sound(SFX_ROUND_2),
                'final_round': pygame.mixer.Sound(SFX_FINAL_ROUND),
                'countdown': pygame.mixer.Sound(SFX_COUNTDOWN),
                'fight': pygame.mixer.Sound(SFX_FIGHT),
                'confirm': pygame.mixer.Sound(SFX_CONFIRM)
            }
        except (pygame.error, KeyError) as e:
            print(f"Lỗi nghiêm trọng khi tải tài nguyên: {e}")
            self.running = False
        self.char_stats = {'A': CHAR_A_STATS, 'B': CHAR_B_STATS}

    def reset_game(self):
        self.player = Fighter(self.player_choice, 200, 330, is_player_one=True)
        self.ai = Fighter(self.ai_choice, 600, 330, is_player_one=False)

        if self.difficulty_choice == "EASY": self.ai_controller = AIRandom(self.ai, self.player)
        elif self.difficulty_choice == "MEDIUM": self.ai_controller = AIRuleBased(self.ai, self.player)
        elif self.difficulty_choice == "HARD": self.ai_controller = AIHeuristic(self.ai, self.player, difficulty='Hard')

        self.player_rounds_won, self.ai_rounds_won, self.current_round = 0, 0, 1
        self.winner = None
        self.start_new_round()

    def start_new_round(self):
        pygame.mixer.music.fadeout(500)
        if self.player: self.player.reset()
        if self.ai: self.ai.reset()
        self.round_over = False
        self.game_state = "ROUND_START"
        self.round_start_sequence_timer = pygame.time.get_ticks()
        self.round_announcement_step = 0
        is_final_round = (self.player_rounds_won == ROUNDS_TO_WIN - 1 and self.ai_rounds_won == ROUNDS_TO_WIN - 1)
        if self.current_round >= (ROUNDS_TO_WIN * 2 - 1) or is_final_round:
             self.round_announcement_text = "FINAL ROUND"; self.sfx['final_round'].play()
        else:
             self.round_announcement_text = f"ROUND {self.current_round}"
             if self.current_round == 1: self.sfx['round1'].play()
             else: self.sfx['round2'].play()

    def update_round_start_sequence(self):
        elapsed = pygame.time.get_ticks() - self.round_start_sequence_timer

        if self.round_announcement_step == 0 and elapsed > ROUND_ANNOUNCE_DURATION:
            self.round_announcement_text = "3"; self.sfx['countdown'].play()
            self.round_announcement_step += 1; self.round_start_sequence_timer = pygame.time.get_ticks()
        elif self.round_announcement_step == 1 and elapsed > COUNTDOWN_STEP_DURATION:
            self.round_announcement_text = "2"
            self.round_announcement_step += 1; self.round_start_sequence_timer = pygame.time.get_ticks()
        elif self.round_announcement_step == 2 and elapsed > COUNTDOWN_STEP_DURATION:
            self.round_announcement_text = "1"
            self.round_announcement_step += 1; self.round_start_sequence_timer = pygame.time.get_ticks()
        elif self.round_announcement_step == 3 and elapsed > COUNTDOWN_STEP_DURATION:
            self.round_announcement_text = "FIGHT!"; self.sfx['fight'].play()
            
            try:
                pygame.mixer.music.load(MUSIC_BATTLE)
                pygame.mixer.music.play(-1)
            except pygame.error:
                print(f"Cảnh báo: Không thể tải nhạc chiến đấu '{MUSIC_BATTLE}'.")
            
            self.round_announcement_step += 1; self.round_start_sequence_timer = pygame.time.get_ticks()
        elif self.round_announcement_step == 4 and elapsed > FIGHT_ANNOUNCE_DURATION:
            self.game_state = "IN_GAME"
            self.round_start_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if self.game_state == "MAIN_MENU": self.handle_main_menu_input(event)
            elif self.game_state == "GUIDE": self.handle_guide_input(event) # --- MỚI ---
            elif self.game_state == "CHARACTER_SELECT": self.handle_character_selection(event)
            elif self.game_state == "DIFFICULTY_SELECT": self.handle_difficulty_selection(event)
            elif self.game_state == "IN_GAME": self.handle_in_game_input(event)
            elif self.game_state == "GAME_OVER": self.handle_game_over_input(event)

    def handle_main_menu_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.sfx['confirm'].play() # <--- THÊM ÂM THANHv
            if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                self.game_state = "CHARACTER_SELECT"
                try:
                    pygame.mixer.music.load(MUSIC_CHAR_SELECT)
                    pygame.mixer.music.play(-1)
                except pygame.error as e:
                    print(f"Cảnh báo: Không tải được nhạc chọn nhân vật: {e}")
            # --- THAY ĐỔI: Chuyển sang màn hình hướng dẫn ---
            if self.guide_button_rect and self.guide_button_rect.collidepoint(event.pos):
                self.sfx['confirm'].play() # <--- THÊM ÂM THANH
                self.game_state = "GUIDE"
                self.guide_scroll_y = 0 # Reset vị trí cuộn
            if self.exit_button_rect and self.exit_button_rect.collidepoint(event.pos):
                self.sfx['confirm'].play() # <--- THÊM ÂM THANH
                self.running = False

    # --- HÀM MỚI: Xử lý input cho màn hình hướng dẫn ---
    def handle_guide_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = "MAIN_MENU"
            if event.key == pygame.K_UP:
                self.guide_scroll_y += SCROLL_SPEED
            if event.key == pygame.K_DOWN:
                self.guide_scroll_y -= SCROLL_SPEED
                
        # --- THÊM LOGIC CUỘN CHUỘT ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Nút 1 là click chuột trái
            if event.button == 1:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                    self.game_state = "MAIN_MENU"
            # Nút 4 là cuộn lên
            if event.button == 4:
                self.guide_scroll_y += SCROLL_SPEED
            # Nút 5 là cuộn xuống
            if event.button == 5:
                self.guide_scroll_y -= SCROLL_SPEED

        # Giới hạn cuộn (áp dụng cho cả phím và chuột)
        self.guide_scroll_y = min(0, self.guide_scroll_y) # Không cho cuộn lên quá đỉnh
        self.guide_scroll_y = max(-self.guide_max_scroll, self.guide_scroll_y) # Không cho cuộn xuống quá đáy
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                self.game_state = "MAIN_MENU"
        
        # Giới hạn cuộn
        self.guide_scroll_y = min(0, self.guide_scroll_y) # Không cho cuộn lên quá đỉnh
        self.guide_scroll_y = max(-self.guide_max_scroll, self.guide_scroll_y) # Không cho cuộn xuống quá đáy

    def handle_character_selection(self, event):
        if self.game_state != "CHARACTER_SELECT": return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: self.p1_cursor_pos = 1
            if event.key == pygame.K_LEFT: self.p1_cursor_pos = 0
            if event.key == pygame.K_RETURN: self.confirm_character_choice(self.p1_cursor_pos)

    def confirm_character_choice(self, choice_index):
        self.sfx['confirm'].play()
        self.player_choice = 'A' if choice_index == 0 else 'B'
        self.ai_choice = 'B' if self.player_choice == 'A' else 'A'
        self.game_state = "CHARACTER_CONFIRMED"
        self.select_frame_index = 0
        self.confirmation_timer = pygame.time.get_ticks()

    def handle_difficulty_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and self.difficulty_cursor_pos < 2: self.difficulty_cursor_pos += 1
            if event.key == pygame.K_UP and self.difficulty_cursor_pos > 0: self.difficulty_cursor_pos -= 1
            if event.key == pygame.K_RETURN: self.confirm_difficulty_choice(self.difficulty_cursor_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.easy_rect and self.easy_rect.collidepoint(event.pos): self.confirm_difficulty_choice(0)
            if self.medium_rect and self.medium_rect.collidepoint(event.pos): self.confirm_difficulty_choice(1)
            if self.hard_rect and self.hard_rect.collidepoint(event.pos): self.confirm_difficulty_choice(2)

    def confirm_difficulty_choice(self, choice_index):
        self.sfx['confirm'].play()
        choices = ["EASY", "MEDIUM", "HARD"]
        self.difficulty_choice = choices[choice_index]
        self.reset_game()

    def handle_in_game_input(self, event):
        if not self.player or self.player.dead: return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: self.player.attack(self.ai, 'air' if self.player.in_air else 'light')
            if event.key == pygame.K_f: self.player.attack(self.ai, 'special')
            if event.key == pygame.K_UP: self.player.jump()
            if event.key == pygame.K_SPACE: self.player.roll()

    def handle_game_over_input(self, event):
        def back_to_menu():
            self.game_state = "CHARACTER_SELECT"
            try:
                pygame.mixer.music.load(MUSIC_CHAR_SELECT)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"Cảnh báo: Không tải được nhạc chọn nhân vật: {e}")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: back_to_menu()
            if event.key == pygame.K_ESCAPE: self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.replay_button_rect and self.replay_button_rect.collidepoint(event.pos): back_to_menu()
            if self.quit_button_rect and self.quit_button_rect.collidepoint(event.pos): self.running = False

    def update(self):
        if self.game_state in ["CHARACTER_SELECT", "CHARACTER_CONFIRMED"]:
            now = pygame.time.get_ticks()
            anim_speed = 150 if self.game_state == "CHARACTER_CONFIRMED" else 100
            if now - self.select_anim_timer > anim_speed: self.select_frame_index += 1; self.select_anim_timer = now
            if now - self.cursor_anim_timer > 80: self.cursor_frame_index += 1; self.cursor_anim_timer = now
        if self.game_state == "CHARACTER_CONFIRMED":
            if pygame.time.get_ticks() - self.confirmation_timer > CONFIRMATION_DURATION: self.game_state = "DIFFICULTY_SELECT"
        
        if self.game_state == "ROUND_START":
            self.update_round_start_sequence()
            if self.player: self.player.update(); self.ai.update()
            return

        if self.game_state != "IN_GAME" or not self.player or not self.ai: 
            self.damage_text_group.update()
            return
            
        if not self.round_over:
            self.round_timer = ROUND_TIME_LIMIT - (pygame.time.get_ticks() - self.round_start_time)
            self.player.defend(pygame.key.get_pressed()[pygame.K_d])
            if self.ai_controller: self.ai_controller.update()
            self.player.move(self.ai); self.ai.move(self.player)
            self.player.update(); self.ai.update()
            
            self.player.check_attack_collision(self.ai)
            if self.ai.last_damage_taken > 0:
                damage_text = DamageText(self.ai.hurtbox.centerx, self.ai.hurtbox.top, self.ai.last_damage_taken, self.damage_font, YELLOW)
                self.damage_text_group.add(damage_text)
                self.ai.last_damage_taken = 0
            
            self.ai.check_attack_collision(self.player)
            if self.player.last_damage_taken > 0:
                damage_text = DamageText(self.player.hurtbox.centerx, self.player.hurtbox.top, self.player.last_damage_taken, self.damage_font, RED)
                self.damage_text_group.add(damage_text)
                self.player.last_damage_taken = 0

            if self.player.dead or self.ai.dead or self.round_timer <= 0:
                self.round_over = True; self.round_over_time = pygame.time.get_ticks()
                self.handle_round_end()
        else:
            self.player.update(); self.ai.update()
            if pygame.time.get_ticks() - self.round_over_time > ROUND_OVER_DELAY:
                if self.game_state == "IN_GAME": self.current_round += 1; self.start_new_round()

        self.damage_text_group.update()

    def handle_round_end(self):
        round_winner = None
        if self.round_timer <= 0:
            if self.player.hp > self.ai.hp: round_winner = self.player
            elif self.ai.hp > self.player.hp: round_winner = self.ai
            else: self.winner = "DRAW"
        else:
            if self.ai.dead: round_winner = self.player
            elif self.player.dead: round_winner = self.ai
        if round_winner == self.player: self.player_rounds_won += 1
        elif round_winner == self.ai: self.ai_rounds_won += 1
        def set_game_over(winner_name):
            self.winner = winner_name
            self.game_state = "GAME_OVER"
                        # --- LOGIC PHÁT NHẠC KẾT THÚC TRẬN ĐẤU ---
            pygame.mixer.music.fadeout(1000) # Làm mờ dần nhạc chiến đấu

            try:
                # Nếu người chơi thắng
                if winner_name == self.player.name:
                    pygame.mixer.music.load(MUSIC_WIN)
                # Nếu người chơi thua hoặc hòa
                else:
                    pygame.mixer.music.load(MUSIC_LOSE)
                
                pygame.mixer.music.play(-1) # Phát lặp lại nhạc thắng/thua
            except pygame.error as e:
                print(f"Cảnh báo: Không tải được nhạc kết thúc trận đấu: {e}")
            # ------------------------------------------
        if self.player_rounds_won >= ROUNDS_TO_WIN: set_game_over(self.player.name)
        elif self.ai_rounds_won >= ROUNDS_TO_WIN: set_game_over(self.ai.name)
        elif self.winner == "DRAW" and self.current_round >= (ROUNDS_TO_WIN * 2 -1):
            set_game_over("DRAW")

    def draw(self):
        if not self.running: return
        if self.game_state == "MAIN_MENU":
            self.start_button_rect, self.guide_button_rect, self.exit_button_rect = draw_main_menu_screen(self.screen, self.bg_main_menu, self.logo_image)
        # --- MỚI: Vẽ màn hình hướng dẫn ---
        elif self.game_state == "GUIDE":
            self.back_button_rect = draw_guide_screen(self.screen, self.bg_main_menu, self.guide_scroll_y)
        elif self.game_state in ["CHARACTER_SELECT", "CHARACTER_CONFIRMED"]:
            self.char_a_rect, self.char_b_rect = draw_character_select_screen(self.screen, self.bg_char_select, self.p1_cursor_pos,
                self.char_stats, self.select_anims, self.select_frame_index, self.game_state, self.cursor_frames, self.cursor_frame_index, self.portraits)
        elif self.game_state == "DIFFICULTY_SELECT":
            self.easy_rect, self.medium_rect, self.hard_rect = draw_difficulty_select_screen(self.screen, self.bg_char_select, self.difficulty_cursor_pos)
        elif self.game_state in ["ROUND_START", "IN_GAME", "GAME_OVER"]:
            self.screen.blit(self.bg_stage_1, (0, 0))
            if self.player: self.player.draw(self.screen)
            if self.ai: self.ai.draw(self.screen)
            
            self.damage_text_group.draw(self.screen)
            
            if self.player and self.ai:
                timer_display = self.round_timer if not self.round_over else 0
                draw_battle_hud(self.screen, self.player, self.ai, timer_display, self.player_rounds_won, self.ai_rounds_won)
            if self.game_state == "ROUND_START": draw_round_announcement(self.screen, self.round_announcement_text)
            elif self.game_state == "GAME_OVER":
                self.replay_button_rect, self.quit_button_rect = draw_game_over_screen(self.screen, self.winner)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events(); self.update(); self.draw()
            self.clock.tick(FPS)
        pygame.quit(); sys.exit()