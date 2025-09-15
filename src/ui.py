import pygame
from .config import *

def draw_text(surface, text, size, x, y, color=WHITE, align="center"):
    try: font = pygame.font.Font(FONT_PATH, size)
    except: font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center": text_rect.center = (x, y)
    elif align == "topleft": text_rect.topleft = (x, y)
    elif align == "topright": text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect

def draw_health_bar(surface, x, y, width, height, hp, max_hp):
    ratio = max(0, hp / max_hp)
    pygame.draw.rect(surface, (80,0,0), (x, y, width, height))
    pygame.draw.rect(surface, GREEN, (x, y, width * ratio, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)

def draw_sp_bar(surface, x, y, width, height, sp, max_sp):
    ratio = max(0, sp / max_sp)
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))
    pygame.draw.rect(surface, BLUE, (x, y, width * ratio, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)

def draw_character_select_screen(surface, bg, portraits, p1_cursor, p1_pos, char_stats):
    surface.blit(bg, (0, 0))
    portrait_a_rect = surface.blit(portraits['A'], (150, 200))
    portrait_b_rect = surface.blit(portraits['B'], (450, 200))
    selected_char = 'A' if p1_pos == 0 else 'B'
    draw_text(surface, char_stats[selected_char]['name'], 30, SCREEN_WIDTH // 2, 450)
    cursor_pos = portrait_a_rect.center if p1_pos == 0 else portrait_b_rect.center
    surface.blit(p1_cursor, (cursor_pos[0] - p1_cursor.get_width()//2, cursor_pos[1] - p1_cursor.get_height()//2 - 80))
    draw_text(surface, "CHỌN NHÂN VẬT", 50, SCREEN_WIDTH // 2, 80)
    draw_text(surface, "Dùng phím <- -> hoặc CHUỘT để chọn", 24, SCREEN_WIDTH // 2, 520)
    draw_text(surface, "Nhấn ENTER hoặc CLICK để xác nhận", 24, SCREEN_WIDTH // 2, 550)
    return portrait_a_rect, portrait_b_rect

def draw_difficulty_select_screen(surface, bg, cursor_pos):
    surface.blit(bg, (0, 0))
    draw_text(surface, "CHỌN ĐỘ KHÓ", 50, SCREEN_WIDTH // 2, 80)
    button_w, button_h = 250, 60
    button_x = SCREEN_WIDTH // 2
    difficulties = ["DỄ", "TRUNG BÌNH", "KHÓ"]
    rects = []
    for i, text in enumerate(difficulties):
        button_y = 200 + i * 80
        is_selected = (i == cursor_pos)
        button_color = YELLOW if is_selected else WHITE
        button_rect = pygame.Rect(0, 0, button_w, button_h); button_rect.center = (button_x, button_y)
        pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
        pygame.draw.rect(surface, GRAY, button_rect, width=3, border_radius=10)
        draw_text(surface, text, 30, button_x, button_y, color=BLACK)
        rects.append(button_rect)
    draw_text(surface, "Dùng phím ↑ ↓ hoặc CHUỘT để chọn", 24, SCREEN_WIDTH // 2, 520)
    draw_text(surface, "Nhấn ENTER hoặc CLICK để bắt đầu", 24, SCREEN_WIDTH // 2, 550)
    return rects[0], rects[1], rects[2]

def draw_battle_hud(surface, player, ai, round_timer, player_wins, ai_wins):
    seconds = max(0, round_timer // 1000)
    draw_text(surface, str(seconds), 60, SCREEN_WIDTH // 2, 30)
    draw_text(surface, player.name, 22, 50, 20, align="topleft")
    draw_health_bar(surface, 50, 50, 300, 25, player.hp, player.max_hp)
    draw_text(surface, f"{int(player.hp)}/{player.max_hp}", 18, 50 + 150, 50 + 13)
    draw_sp_bar(surface, 50, 80, 250, 15, player.sp, player.max_sp)
    for i in range(ROUNDS_TO_WIN):
        color = YELLOW if i < player_wins else GRAY
        pygame.draw.circle(surface, color, (50 + i * 30, 110), 10); pygame.draw.circle(surface, WHITE, (50 + i * 30, 110), 10, 2)
    draw_text(surface, ai.name, 22, SCREEN_WIDTH - 50, 20, align="topright")
    draw_health_bar(surface, SCREEN_WIDTH - 350, 50, 300, 25, ai.hp, ai.max_hp)
    draw_text(surface, f"{int(ai.hp)}/{ai.max_hp}", 18, (SCREEN_WIDTH - 350) + 150, 50 + 13)
    draw_sp_bar(surface, SCREEN_WIDTH - 300, 80, 250, 15, ai.sp, ai.max_sp)
    for i in range(ROUNDS_TO_WIN):
        color = YELLOW if i < ai_wins else GRAY
        pygame.draw.circle(surface, color, ((SCREEN_WIDTH - 50) - i * 30, 110), 10); pygame.draw.circle(surface, WHITE, ((SCREEN_WIDTH - 50) - i * 30, 110), 10, 2)

def draw_game_over_screen(surface, winner_name):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)); surface.blit(overlay, (0, 0))
    if winner_name and winner_name != "DRAW": draw_text(surface, f"{winner_name.upper()} WINS!", 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    else: draw_text(surface, "DRAW", 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    button_w, button_h = 220, 50
    replay_rect = pygame.Rect(0, 0, button_w, button_h); replay_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    pygame.draw.rect(surface, GREEN, replay_rect, border_radius=10)
    draw_text(surface, "Chơi Lại (Enter)", 24, replay_rect.centerx, replay_rect.centery, color=BLACK)
    quit_rect = pygame.Rect(0, 0, button_w, button_h); quit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
    pygame.draw.rect(surface, RED, quit_rect, border_radius=10)
    draw_text(surface, "Thoát Game (Esc)", 24, quit_rect.centerx, quit_rect.centery, color=BLACK)
    return replay_rect, quit_rect