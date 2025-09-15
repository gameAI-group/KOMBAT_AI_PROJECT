import pygame, sys
from .config import *
from .fighter import Fighter
from .ui import draw_character_select_screen, draw_difficulty_select_screen, draw_battle_hud, draw_game_over_screen
from .ai.ai_random import AIRandom

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "CHARACTER_SELECT"

        self.load_assets()

        self.p1_cursor_pos = 0; self.difficulty_cursor_pos = 0
        self.player_choice = None; self.ai_choice = None; self.difficulty_choice = None
        self.char_a_rect, self.char_b_rect = None, None
        self.easy_rect, self.medium_rect, self.hard_rect = None, None, None

        self.player = None; self.ai = None; self.ai_controller = None
        self.player_rounds_won = 0; self.ai_rounds_won = 0; self.current_round = 1
        self.round_start_time = 0; self.round_timer = ROUND_TIME_LIMIT
        self.round_over = False; self.round_over_time = 0
        self.winner = None
        self.replay_button_rect, self.quit_button_rect = None, None

    def load_assets(self):
        try:
            temp_bg_select = pygame.image.load(BG_CHAR_SELECT).convert()
            self.bg_char_select = pygame.transform.scale(temp_bg_select, (SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_bg_stage = pygame.image.load(BG_STAGE_1).convert()
            self.bg_stage_1 = pygame.transform.scale(temp_bg_stage, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.portrait_a = pygame.image.load(PORTRAIT_A).convert_alpha()
            self.portrait_b = pygame.image.load(PORTRAIT_B).convert_alpha()
            self.p1_cursor = pygame.image.load(CURSOR_P1).convert_alpha()
        except pygame.error as e: print(f"Lỗi tải tài nguyên: {e}"); self.running = False
        
        self.portraits = {'A': self.portrait_a, 'B': self.portrait_b}
        self.char_stats = {'A': CHAR_A_STATS, 'B': CHAR_B_STATS}
    
    def reset_game(self):
        self.player = Fighter(self.player_choice, x=200, y=330, is_player_one=True)
        self.ai = Fighter(self.ai_choice, x=600, y=330, is_player_one=False)
        self.ai_controller = AIRandom(self.ai, self.player, self.difficulty_choice)
        self.player_rounds_won, self.ai_rounds_won, self.current_round = 0, 0, 1
        self.winner = None
        self.start_new_round()
        self.game_state = "IN_GAME"

    def start_new_round(self):
        if self.player: self.player.reset()
        if self.ai: self.ai.reset()
        self.round_start_time = pygame.time.get_ticks()
        self.round_over = False

    def handle_events(self):
        if self.game_state == "IN_GAME" and self.player:
             keys = pygame.key.get_pressed()
             self.player.defend(keys[pygame.K_d])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            
            if self.game_state == "CHARACTER_SELECT": self.handle_character_selection(event)
            elif self.game_state == "DIFFICULTY_SELECT": self.handle_difficulty_selection(event)
            elif self.game_state == "IN_GAME": self.handle_in_game_input(event)
            elif self.game_state == "GAME_OVER": self.handle_game_over_input(event)
    
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
        if event.type == pygame.KEYDOWN:
            if not self.player or self.player.dead: return
            if event.key == pygame.K_a: self.player.attack(self.ai, 'air' if self.player.in_air else 'light')
            if event.key == pygame.K_f: self.player.attack(self.ai, 'special')
            if event.key == pygame.K_UP: self.player.jump()
            if event.key == pygame.K_SPACE: self.player.roll()
        
    def handle_game_over_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: self.game_state = "CHARACTER_SELECT"
            if event.key == pygame.K_ESCAPE: self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.replay_button_rect and self.replay_button_rect.collidepoint(event.pos): self.game_state = "CHARACTER_SELECT"
            if self.quit_button_rect and self.quit_button_rect.collidepoint(event.pos): self.running = False

    def update(self):
        if self.game_state != "IN_GAME" or not self.player or not self.ai: return

        if not self.round_over:
            elapsed = pygame.time.get_ticks() - self.round_start_time
            self.round_timer = ROUND_TIME_LIMIT - elapsed
            self.ai_controller.update()
            self.player.move(self.ai)
            self.ai.move(self.player)
            self.player.update()
            self.ai.update()
            self.player.check_attack_collision(self.ai)
            self.ai.check_attack_collision(self.player)
            if self.player.dead or self.ai.dead or self.round_timer <= 0:
                self.round_over = True; self.round_over_time = pygame.time.get_ticks()
                self.handle_round_end()
        else:
            self.player.update(); self.ai.update()
            if pygame.time.get_ticks() - self.round_over_time > ROUND_OVER_DELAY:
                if self.game_state == "IN_GAME": self.current_round += 1; self.start_new_round()

    def handle_round_end(self):
        winner = None
        if self.round_timer <= 0:
            if self.player.hp > self.ai.hp: winner = self.player
            elif self.ai.hp > self.player.hp: winner = self.ai
        else:
            if self.ai.dead: winner = self.player
            elif self.player.dead: winner = self.ai
        if winner == self.player: self.player_rounds_won += 1
        elif winner == self.ai: self.ai_rounds_won += 1
        if self.player_rounds_won >= ROUNDS_TO_WIN: self.winner = self.player.name; self.game_state = "GAME_OVER"
        elif self.ai_rounds_won >= ROUNDS_TO_WIN: self.winner = self.ai.name; self.game_state = "GAME_OVER"
        elif self.current_round >= 3:
            if self.player_rounds_won > self.ai_rounds_won: self.winner = self.player.name
            elif self.ai_rounds_won > self.player_rounds_won: self.winner = self.ai.name
            else: self.winner = "DRAW"
            self.game_state = "GAME_OVER"

    def draw(self):
        if self.game_state == "CHARACTER_SELECT":
            self.char_a_rect, self.char_b_rect = draw_character_select_screen(self.screen, self.bg_char_select, self.portraits, self.p1_cursor, self.p1_cursor_pos, self.char_stats)
        elif self.game_state == "DIFFICULTY_SELECT":
            self.easy_rect, self.medium_rect, self.hard_rect = draw_difficulty_select_screen(self.screen, self.bg_char_select, self.difficulty_cursor_pos)
        elif self.game_state in ["IN_GAME", "GAME_OVER"]:
            self.screen.blit(self.bg_stage_1, (0, 0))
            if self.player: self.player.draw(self.screen)
            if self.ai: self.ai.draw(self.screen)
            if self.player and self.ai: draw_battle_hud(self.screen, self.player, self.ai, self.round_timer, self.player_rounds_won, self.ai_rounds_won)
            if self.game_state == "GAME_OVER":
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