# src/game.py
import pygame
import sys
from .config import *
from .fighter import Fighter
from .ui import draw_character_select_screen, draw_difficulty_select_screen, draw_battle_hud, draw_game_over_screen
from .ai.ai_random import AIRandom
# (Trong tương lai có thể import thêm các AI khác)
# from .ai.ai_rule_based import AIRuleBased 
# from .ai.ai_heuristic import AIHeuristic

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Quản lý trạng thái game
        self.game_state = "CHARACTER_SELECT"
        
        self.load_assets()
        
        # Biến cho màn hình chọn nhân vật
        self.p1_cursor_pos = 0
        self.player_choice = None
        self.ai_choice = None
        # Rects để xử lý click chuột
        self.char_a_rect = None
        self.char_b_rect = None

        # Biến cho màn hình chọn độ khó
        self.difficulty_cursor_pos = 0 # 0: Dễ, 1: TB, 2: Khó
        self.difficulty_choice = None
        # Rects để xử lý click chuột
        self.easy_rect = None
        self.medium_rect = None
        self.hard_rect = None

        # Biến trong trận đấu
        self.player = None
        self.ai = None
        self.ai_controller = None
        self.winner = None

        # Biến kết thúc trận đấu
        self.replay_button_rect = None
        self.quit_button_rect = None

    def load_assets(self):
        try:
            temp_bg_select = pygame.image.load(BG_CHAR_SELECT).convert()
            self.bg_char_select = pygame.transform.scale(temp_bg_select, (SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_bg_stage = pygame.image.load(BG_STAGE_1).convert()
            self.bg_stage_1 = pygame.transform.scale(temp_bg_stage, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.portrait_a = pygame.image.load(PORTRAIT_A).convert_alpha()
            self.portrait_b = pygame.image.load(PORTRAIT_B).convert_alpha()
            self.p1_cursor = pygame.image.load(CURSOR_P1).convert_alpha()
        except pygame.error as e:
            print(f"Cảnh báo: Không thể load file ảnh. Lỗi: {e}.")
            self.bg_char_select = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); self.bg_char_select.fill(BLUE)
            self.bg_stage_1 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); self.bg_stage_1.fill(BLACK)
            self.portrait_a = pygame.Surface((200, 200)); self.portrait_a.fill(WHITE)
            self.portrait_b = pygame.Surface((200, 200)); self.portrait_b.fill(RED)
            self.p1_cursor = pygame.Surface((220, 220)); self.p1_cursor.fill(GREEN); self.p1_cursor.set_colorkey(BLACK)
        
        self.portraits = {'A': self.portrait_a, 'B': self.portrait_b}
        self.char_stats = {'A': CHAR_A_STATS, 'B': CHAR_B_STATS}

    def reset_game(self):
        # Thiết lập nhân vật
        self.player = Fighter(self.player_choice, x=200, y=GROUND_Y, is_player_one=True)
        self.ai = Fighter(self.ai_choice, x=600, y=GROUND_Y, is_player_one=False)
        
        # Chọn AI Controller dựa trên độ khó
        # Hiện tại tất cả đều là AIRandom, sẵn sàng để nâng cấp sau
        if self.difficulty_choice == "EASY":
            self.ai_controller = AIRandom(self.ai, self.player)
        elif self.difficulty_choice == "MEDIUM":
            self.ai_controller = AIRandom(self.ai, self.player) # Sẽ thay bằng AI tốt hơn
        elif self.difficulty_choice == "HARD":
            self.ai_controller = AIRandom(self.ai, self.player) # Sẽ thay bằng AI tốt hơn
            
        self.winner = None
        self.game_state = "IN_GAME"

    def handle_character_selection(self, event):
        # Bàn phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: self.p1_cursor_pos = 1
            if event.key == pygame.K_LEFT: self.p1_cursor_pos = 0
            if event.key == pygame.K_RETURN:
                self.confirm_character_choice(self.p1_cursor_pos)
        # Chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.char_a_rect and self.char_a_rect.collidepoint(event.pos):
                self.confirm_character_choice(0)
            if self.char_b_rect and self.char_b_rect.collidepoint(event.pos):
                self.confirm_character_choice(1)

    def confirm_character_choice(self, choice_index):
        self.player_choice = 'A' if choice_index == 0 else 'B'
        self.ai_choice = 'B' if self.player_choice == 'A' else 'A'
        self.game_state = "DIFFICULTY_SELECT" # Chuyển sang màn hình chọn độ khó

    def handle_difficulty_selection(self, event):
        # Bàn phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and self.difficulty_cursor_pos < 2:
                self.difficulty_cursor_pos += 1
            if event.key == pygame.K_UP and self.difficulty_cursor_pos > 0:
                self.difficulty_cursor_pos -= 1
            if event.key == pygame.K_RETURN:
                self.confirm_difficulty_choice(self.difficulty_cursor_pos)
        # Chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.easy_rect and self.easy_rect.collidepoint(event.pos):
                self.confirm_difficulty_choice(0)
            if self.medium_rect and self.medium_rect.collidepoint(event.pos):
                self.confirm_difficulty_choice(1)
            if self.hard_rect and self.hard_rect.collidepoint(event.pos):
                self.confirm_difficulty_choice(2)

    def confirm_difficulty_choice(self, choice_index):
        choices = ["EASY", "MEDIUM", "HARD"]
        self.difficulty_choice = choices[choice_index]
        self.reset_game() # Bắt đầu game sau khi đã chọn xong

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_state == "CHARACTER_SELECT":
                self.handle_character_selection(event)
            
            elif self.game_state == "DIFFICULTY_SELECT":
                self.handle_difficulty_selection(event)
            
            elif self.game_state == "IN_GAME":
                if event.type == pygame.KEYDOWN:
                    if not self.player.dead:
                        if event.key == pygame.K_a: self.player.attack(self.ai)
                        if event.key == pygame.K_UP: self.player.jump()
                        if event.key == pygame.K_SPACE: self.player.roll()
                        if event.key == pygame.K_f: self.player.special_attack(self.ai)
            
            elif self.game_state == "GAME_OVER":
                # Xử lý nhấn phím
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        # Reset lại các lựa chọn để bắt đầu lại từ đầu
                        self.player_choice = None
                        self.ai_choice = None
                        self.difficulty_choice = None
                        self.game_state = "CHARACTER_SELECT"
                    if event.key == pygame.K_ESCAPE: 
                        self.running = False
                
                # Xử lý click chuột
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Kiểm tra xem có click vào nút "Chơi Lại" không
                    if self.replay_button_rect and self.replay_button_rect.collidepoint(event.pos):
                        self.player_choice = None
                        self.ai_choice = None
                        self.difficulty_choice = None
                        self.game_state = "CHARACTER_SELECT"
                    
                    # Kiểm tra xem có click vào nút "Thoát" không
                    if self.quit_button_rect and self.quit_button_rect.collidepoint(event.pos):
                        self.running = False

    def update(self):
        if self.game_state == "IN_GAME":
            if not self.ai.dead:
                self.ai_controller.update()

            if not self.player.dead:
                self.player.move(target=self.ai)
            if not self.ai.dead:
                self.ai.move(target=self.player)

            self.player.update()
            self.ai.update()
            
            if self.player.dead and not self.winner:
                self.winner = self.ai.name
                self.game_state = "GAME_OVER"
            elif self.ai.dead and not self.winner:
                self.winner = self.player.name
                self.game_state = "GAME_OVER"

    def draw(self):
        if self.game_state == "CHARACTER_SELECT":
            # Hàm vẽ giờ đây trả về các Rect để xử lý click
            self.char_a_rect, self.char_b_rect = draw_character_select_screen(
                surface=self.screen, bg=self.bg_char_select, portraits=self.portraits,
                p1_cursor=self.p1_cursor, p1_pos=self.p1_cursor_pos, char_stats=self.char_stats
            )
        
        elif self.game_state == "DIFFICULTY_SELECT":
            # Hàm vẽ trả về Rect của các nút
            self.easy_rect, self.medium_rect, self.hard_rect = draw_difficulty_select_screen(
                surface=self.screen, bg=self.bg_char_select, cursor_pos=self.difficulty_cursor_pos
            )

        elif self.game_state in ["IN_GAME", "GAME_OVER"]:
            self.screen.blit(self.bg_stage_1, (0, 0))
            if self.player: self.player.draw(self.screen)
            if self.ai: self.ai.draw(self.screen)
            if self.player and self.ai: draw_battle_hud(self.screen, self.player, self.ai)
            
            if self.game_state == "GAME_OVER":
                # === CẬP NHẬT LOGIC VẼ CHO GAME_OVER ===
                # Hàm vẽ giờ sẽ trả về Rect của các nút để chúng ta có thể kiểm tra click
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