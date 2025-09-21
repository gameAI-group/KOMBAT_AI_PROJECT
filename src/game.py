import pygame, sys
from .config import *
from .fighter import Fighter
from .ui import (draw_main_menu_screen, draw_character_select_screen, 
                 draw_difficulty_select_screen, draw_battle_hud, 
                 draw_game_over_screen, draw_round_announcement)
from .ai.ai_random import AIRandom
from .ai.ai_rulebased import AIRuleBased

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "MAIN_MENU"

        self.load_assets()
        
        try:
            pygame.mixer.music.load(MUSIC_MENU)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Cảnh báo: Không thể tải nhạc menu: {e}")

        # Biến cho các trạng thái game
        self.start_button_rect, self.guide_button_rect, self.exit_button_rect = None, None, None
        self.p1_cursor_pos = 0
        self.difficulty_cursor_pos = 0
        self.player_choice = None
        self.ai_choice = None
        self.difficulty_choice = None
        self.char_a_rect, self.char_b_rect = None, None
        self.easy_rect, self.medium_rect, self.hard_rect = None, None, None
        self.replay_button_rect, self.quit_button_rect = None, None

        # Biến cho trận đấu
        self.player = None
        self.ai = None
        self.ai_controller = None
        self.player_rounds_won = 0
        self.ai_rounds_won = 0
        self.current_round = 1
        self.round_start_time = 0
        self.round_timer = ROUND_TIME_LIMIT
        self.round_over = False
        self.round_over_time = 0
        self.winner = None
        
        # Biến cho chuỗi sự kiện bắt đầu hiệp
        self.round_start_sequence_timer = 0
        self.round_announcement_text = ""
        self.round_announcement_step = 0

    def load_assets(self):
        try:
            # Tải ảnh và SFX
            temp_bg_main = pygame.image.load(BG_MAIN_MENU).convert()
            self.bg_main_menu = pygame.transform.scale(temp_bg_main, (SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_bg_select = pygame.image.load(BG_CHAR_SELECT).convert()
            self.bg_char_select = pygame.transform.scale(temp_bg_select, (SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_bg_stage = pygame.image.load(BG_STAGE_1).convert()
            self.bg_stage_1 = pygame.transform.scale(temp_bg_stage, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.portrait_a = pygame.image.load(PORTRAIT_A).convert_alpha()
            self.portrait_b = pygame.image.load(PORTRAIT_B).convert_alpha()
            self.p1_cursor = pygame.image.load(CURSOR_P1).convert_alpha()
            self.sfx = {
                'round1': pygame.mixer.Sound(SFX_ROUND_1),
                'round2': pygame.mixer.Sound(SFX_ROUND_2),
                'final_round': pygame.mixer.Sound(SFX_FINAL_ROUND),
                'countdown': pygame.mixer.Sound(SFX_COUNTDOWN),
                'fight': pygame.mixer.Sound(SFX_FIGHT)
            }
        except pygame.error as e: 
            print(f"Lỗi tải tài nguyên: {e}")
            self.running = False
        
        self.portraits = {'A': self.portrait_a, 'B': self.portrait_b}
        self.char_stats = {'A': CHAR_A_STATS, 'B': CHAR_B_STATS}
    
    def reset_game(self):
        self.player = Fighter(self.player_choice, x=200, y=330, is_player_one=True)
        self.ai = Fighter(self.ai_choice, x=600, y=330, is_player_one=False)
        
        if self.difficulty_choice == "EASY": self.ai_controller = AIRandom(self.ai, self.player)
        elif self.difficulty_choice == "MEDIUM": self.ai_controller = AIRuleBased(self.ai, self.player)
        elif self.difficulty_choice == "HARD": self.ai_controller = AIRuleBased(self.ai, self.player)
        
        self.player_rounds_won, self.ai_rounds_won, self.current_round = 0, 0, 1
        self.winner = None
        self.start_new_round()

    def start_new_round(self):
        """Bắt đầu một hiệp mới và kích hoạt chuỗi sự kiện thông báo."""
        pygame.mixer.music.fadeout(200)

        if self.player: self.player.reset()
        if self.ai: self.ai.reset()
        
        self.round_over = False
        self.game_state = "ROUND_START"
        self.round_start_sequence_timer = pygame.time.get_ticks()
        self.round_announcement_step = 0
        
        is_final_round = (self.player_rounds_won == ROUNDS_TO_WIN - 1 and self.ai_rounds_won == ROUNDS_TO_WIN - 1)
        
        if self.current_round >= (ROUNDS_TO_WIN * 2 - 1) or is_final_round:
             self.round_announcement_text = "FINAL ROUND"
             self.sfx['final_round'].play()
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
            self.round_announcement_step += 1; self.round_start_sequence_timer = pygame.time.get_ticks()
        elif self.round_announcement_step == 4 and elapsed > FIGHT_ANNOUNCE_DURATION:
            self.game_state = "IN_GAME"
            self.round_start_time = pygame.time.get_ticks()
            
            # --- TẠM THỜI VÔ HIỆU HÓA NHẠC BATTLE ---
            # Khi nào có nhạc, bạn chỉ cần xóa các dấu # ở 5 dòng dưới
            # try:
            #     pygame.mixer.music.load(MUSIC_BATTLE)
            #     pygame.mixer.music.play(-1)
            # except pygame.error:
            #     print(f"Cảnh báo: Không thể tải nhạc chiến đấu '{MUSIC_BATTLE}'.")
            # -----------------------------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            
            if self.game_state == "MAIN_MENU": self.handle_main_menu_input(event)
            elif self.game_state == "CHARACTER_SELECT": self.handle_character_selection(event)
            elif self.game_state == "DIFFICULTY_SELECT": self.handle_difficulty_selection(event)
            elif self.game_state == "IN_GAME": self.handle_in_game_input(event)
            elif self.game_state == "GAME_OVER": self.handle_game_over_input(event)
    
    def handle_main_menu_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                self.game_state = "CHARACTER_SELECT"
            if self.exit_button_rect and self.exit_button_rect.collidepoint(event.pos):
                self.running = False

    def handle_character_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: self.p1_cursor_pos = 1
            if event.key == pygame.K_LEFT: self.p1_cursor_pos = 0
            if event.key == pygame.K_RETURN: self.confirm_character_choice(self.p1_cursor_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.char_a_rect and self.char_a_rect.collidepoint(event.pos): self.confirm_character_choice(0)
            if self.char_b_rect and self.char_b_rect.collidepoint(event.pos): self.confirm_character_choice(1)

    def confirm_character_choice(self, choice_index):
        self.player_choice = 'A' if choice_index == 0 else 'B'
        self.ai_choice = 'B' if self.player_choice == 'A' else 'A'
        self.game_state = "DIFFICULTY_SELECT"

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: back_to_menu()
            if event.key == pygame.K_ESCAPE: self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.replay_button_rect and self.replay_button_rect.collidepoint(event.pos): back_to_menu()
            if self.quit_button_rect and self.quit_button_rect.collidepoint(event.pos): self.running = False

    def update(self):
        if self.game_state == "ROUND_START":
            self.update_round_start_sequence()
            if self.player: self.player.update()
            if self.ai: self.ai.update()
            return
        if self.game_state != "IN_GAME" or not self.player or not self.ai: return

        if not self.round_over:
            elapsed = pygame.time.get_ticks() - self.round_start_time
            self.round_timer = ROUND_TIME_LIMIT - elapsed
            keys = pygame.key.get_pressed()
            self.player.defend(keys[pygame.K_d])
            self.ai_controller.update()
            self.player.move(self.ai)
            self.ai.move(self.player)
            self.player.update()
            self.ai.update()
            self.player.check_attack_collision(self.ai)
            self.ai.check_attack_collision(self.player)
            
            if self.player.dead or self.ai.dead or self.round_timer <= 0:
                self.round_over = True
                self.round_over_time = pygame.time.get_ticks()
                self.handle_round_end()
        else:
            self.player.update()
            self.ai.update()
            if pygame.time.get_ticks() - self.round_over_time > ROUND_OVER_DELAY:
                if self.game_state == "IN_GAME":
                    self.current_round += 1
                    self.start_new_round()

    def handle_round_end(self):
        """Xử lý logic khi một hiệp đấu kết thúc."""
        round_winner = None
        if self.round_timer <= 0:
            if self.player.hp > self.ai.hp: round_winner = self.player
            elif self.ai.hp > self.player.hp: round_winner = self.ai
        else:
            if self.ai.dead: round_winner = self.player
            elif self.player.dead: round_winner = self.ai
        
        if round_winner == self.player: self.player_rounds_won += 1
        elif round_winner == self.ai: self.ai_rounds_won += 1
        
        def set_game_over(winner_name):
            self.winner = winner_name
            self.game_state = "GAME_OVER"
            try:
                pygame.mixer.music.load(MUSIC_MENU)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"Cảnh báo: Không thể tải nhạc menu: {e}")

        if self.player_rounds_won >= ROUNDS_TO_WIN:
            set_game_over(self.player.name)
        elif self.ai_rounds_won >= ROUNDS_TO_WIN:
            set_game_over(self.ai.name)

    def draw(self):
        if self.game_state == "MAIN_MENU":
            self.start_button_rect, self.guide_button_rect, self.exit_button_rect = draw_main_menu_screen(self.screen, self.bg_main_menu)
        elif self.game_state == "CHARACTER_SELECT":
            self.char_a_rect, self.char_b_rect = draw_character_select_screen(self.screen, self.bg_char_select, self.portraits, self.p1_cursor, self.p1_cursor_pos, self.char_stats)
        elif self.game_state == "DIFFICULTY_SELECT":
            self.easy_rect, self.medium_rect, self.hard_rect = draw_difficulty_select_screen(self.screen, self.bg_char_select, self.difficulty_cursor_pos)
        elif self.game_state in ["ROUND_START", "IN_GAME", "GAME_OVER"]:
            self.screen.blit(self.bg_stage_1, (0, 0))
            if self.player: self.player.draw(self.screen)
            if self.ai: self.ai.draw(self.screen)
            timer_display = self.round_timer if self.game_state == "IN_GAME" else ROUND_TIME_LIMIT
            if self.player and self.ai:
                draw_battle_hud(self.screen, self.player, self.ai, timer_display, self.player_rounds_won, self.ai_rounds_won)
            
            if self.game_state == "ROUND_START":
                draw_round_announcement(self.screen, self.round_announcement_text)
            elif self.game_state == "GAME_OVER":
                self.replay_button_rect, self.quit_button_rect = draw_game_over_screen(self.screen, self.winner)
                
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()