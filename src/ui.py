# src/ui.py
import pygame
from .config import *

# --- HÀM TIỆN ÍCH ---

def draw_text(surface, text, size, x, y, color=WHITE, align="center"):
    try:
        font = pygame.font.Font(FONT_PATH, size)
    except:
        font = pygame.font.Font(None, size)
        
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "center":
        text_rect.center = (x, y)
    elif align == "topleft":
        text_rect.topleft = (x, y)
    elif align == "topright":
        text_rect.topright = (x, y)
        
    surface.blit(text_surface, text_rect)
    return text_rect # Trả về Rect để xử lý click

def draw_health_bar(surface, x, y, width, height, hp, max_hp):
    ratio = hp / max_hp
    if ratio < 0: ratio = 0
    pygame.draw.rect(surface, RED, (x, y, width, height))
    pygame.draw.rect(surface, GREEN, (x, y, width * ratio, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)

def draw_sp_bar(surface, x, y, width, height, sp, max_sp):
    ratio = sp / max_sp
    if ratio < 0: ratio = 0
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))
    pygame.draw.rect(surface, BLUE, (x, y, width * ratio, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)
    
# --- CÁC HÀM VẼ MÀN HÌNH CHÍNH ---

def draw_character_select_screen(surface, bg, portraits, p1_cursor, p1_pos, char_stats):
    """
    Vẽ màn hình chọn nhân vật.
    Trả về Rect của các chân dung để xử lý click chuột.
    """
    surface.blit(bg, (0, 0))
    
    # Vẽ chân dung và lưu lại Rect của chúng
    portrait_a_rect = surface.blit(portraits['A'], (150, 200))
    portrait_b_rect = surface.blit(portraits['B'], (450, 200))
    
    # Vẽ thông tin nhân vật đang được chọn
    selected_char = 'A' if p1_pos == 0 else 'B'
    draw_text(surface, char_stats[selected_char]['name'], 30, SCREEN_WIDTH // 2, 450)
    
    # Vẽ con trỏ dựa trên vị trí bàn phím
    cursor_pos_rect = portrait_a_rect if p1_pos == 0 else portrait_b_rect
    surface.blit(p1_cursor, (cursor_pos_rect.centerx - p1_cursor.get_width() // 2, cursor_pos_rect.centery - p1_cursor.get_height() // 2 - 80))

    # Vẽ hướng dẫn
    draw_text(surface, "CHỌN NHÂN VẬT", 50, SCREEN_WIDTH // 2, 80)
    draw_text(surface, "Dùng phím <- -> hoặc CHUỘT để chọn", 24, SCREEN_WIDTH // 2, 520)
    draw_text(surface, "Nhấn ENTER hoặc CLICK để xác nhận", 24, SCREEN_WIDTH // 2, 550)
    
    return portrait_a_rect, portrait_b_rect # Trả về để kiểm tra va chạm chuột

def draw_difficulty_select_screen(surface, bg, cursor_pos):
    """
    Vẽ màn hình chọn độ khó.
    Trả về Rect của các nút để xử lý click chuột.
    """
    surface.blit(bg, (0, 0))
    draw_text(surface, "CHỌN ĐỘ KHÓ", 50, SCREEN_WIDTH // 2, 80)

    # Tọa độ và kích thước nút
    button_w, button_h = 250, 60
    button_x = SCREEN_WIDTH // 2
    button_y_start = 200
    
    difficulties = ["DỄ", "TRUNG BÌNH", "KHÓ"]
    rects = []

    for i, text in enumerate(difficulties):
        button_y = button_y_start + i * 80
        # Nếu con trỏ đang ở vị trí này, vẽ nút màu khác để highlight
        is_selected = (i == cursor_pos)
        button_color = YELLOW if is_selected else WHITE
        text_color = BLACK 

        # Vẽ hình chữ nhật của nút
        button_rect = pygame.Rect(0, 0, button_w, button_h)
        button_rect.center = (button_x, button_y)
        pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
        pygame.draw.rect(surface, GRAY, button_rect, width=3, border_radius=10) # Viền
        
        # Vẽ chữ lên nút
        draw_text(surface, text, 30, button_x, button_y, color=text_color)
        rects.append(button_rect)

    draw_text(surface, "Dùng phím ↑ ↓ hoặc CHUỘT để chọn", 24, SCREEN_WIDTH // 2, 520)
    draw_text(surface, "Nhấn ENTER hoặc CLICK để bắt đầu", 24, SCREEN_WIDTH // 2, 550)

    return rects[0], rects[1], rects[2] # Trả về Rect của 3 nút

def draw_battle_hud(surface, player, ai):
    """Vẽ toàn bộ giao diện trong trận đấu (HUD)."""
    # Giao diện người chơi (trái)
    draw_text(surface, player.name, 22, 50, 20, align="topleft")
    draw_health_bar(surface, 50, 50, 300, 25, player.hp, player.max_hp)
    hp_text_player = f"{int(player.hp)} / {player.max_hp}"
    draw_text(surface, hp_text_player, 18, 50 + 150, 50 + 13)
    draw_sp_bar(surface, 50, 80, 250, 15, player.sp, player.max_sp)

    # Giao diện AI (phải)
    draw_text(surface, ai.name, 22, SCREEN_WIDTH - 50, 20, align="topright")
    draw_health_bar(surface, SCREEN_WIDTH - 350, 50, 300, 25, ai.hp, ai.max_hp)
    hp_text_ai = f"{int(ai.hp)} / {ai.max_hp}"
    draw_text(surface, hp_text_ai, 18, (SCREEN_WIDTH - 350) + 150, 50 + 13)
    draw_sp_bar(surface, SCREEN_WIDTH - 300, 80, 250, 15, ai.sp, ai.max_sp)

def draw_game_over_screen(surface, winner_name):
    """
    Vẽ màn hình Game Over với các nút có thể click.
    Trả về Rect của nút "Chơi Lại" và "Thoát".
    """
    # Vẽ một lớp nền mờ
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    # Hiển thị người chiến thắng
    if winner_name:
        draw_text(surface, f"{winner_name.upper()} WIN!", 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    else: 
        draw_text(surface, "DRAW", 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    
    # --- VẼ CÁC NÚT MỚI ---
    button_w, button_h = 220, 50
    
    # Nút "Chơi Lại"
    replay_button_rect = pygame.Rect(0, 0, button_w, button_h)
    replay_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    pygame.draw.rect(surface, GREEN, replay_button_rect, border_radius=10)
    draw_text(surface, "Chơi Lại (Enter)", 24, replay_button_rect.centerx, replay_button_rect.centery, color=BLACK)

    # Nút "Thoát Game"
    quit_button_rect = pygame.Rect(0, 0, button_w, button_h)
    quit_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
    pygame.draw.rect(surface, RED, quit_button_rect, border_radius=10)
    draw_text(surface, "Thoát Game (Esc)", 24, quit_button_rect.centerx, quit_button_rect.centery, color=BLACK)

    return replay_button_rect, quit_button_rect