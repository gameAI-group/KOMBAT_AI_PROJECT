import pygame
from .config import *

def draw_text_custom_font(surface, font_path, text, size, x, y, color=WHITE, align="center"):
    """Hàm vẽ chữ với font tùy chỉnh, có dự phòng nếu font lỗi."""
    try:
        font = pygame.font.Font(font_path, size)
    except Exception:
        font = pygame.font.Font(None, size) # Dùng font mặc định nếu không tải được
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "topleft":
        text_rect.topleft = (x, y)
    elif align == "topright":
        text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect

def draw_text(surface, text, size, x, y, color=WHITE, align="center"):
    """Hàm vẽ chữ tiện ích, sử dụng font mặc định của game."""
    return draw_text_custom_font(surface, FONT_PATH, text, size, x, y, color, align)

def draw_main_menu_screen(surface, bg, logo_image):
    """Vẽ màn hình menu chính với logo và các nút."""
    surface.blit(bg, (0, 0))
    if logo_image:
        logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, 180))
        surface.blit(logo_image, logo_rect)
    else:
        draw_text_custom_font(surface, FONT_TITLE_PATH, "KOMBAT AI", 90, SCREEN_WIDTH // 2, 180, YELLOW)

    button_w, button_h = 300, 65
    button_x = SCREEN_WIDTH // 2
    start_rect = pygame.Rect(0, 0, button_w, button_h); start_rect.center = (button_x, 350)
    pygame.draw.rect(surface, GREEN, start_rect, border_radius=10)
    draw_text(surface, "START", 30, start_rect.centerx, start_rect.centery, color=BLACK)
    guide_rect = pygame.Rect(0, 0, button_w, button_h); guide_rect.center = (button_x, 430)
    pygame.draw.rect(surface, WHITE, guide_rect, border_radius=10)
    draw_text(surface, "HƯỚNG DẪN", 30, guide_rect.centerx, guide_rect.centery, color=BLACK)
    exit_rect = pygame.Rect(0, 0, button_w, button_h); exit_rect.center = (button_x, 510)
    pygame.draw.rect(surface, RED, exit_rect, border_radius=10)
    draw_text(surface, "THOÁT", 30, exit_rect.centerx, exit_rect.centery, color=BLACK)
    return start_rect, guide_rect, exit_rect

def draw_character_info_panel(surface, char_key, char_stats, position, is_selected):
    """Hàm trợ giúp, vẽ khung thông tin chi tiết cho một nhân vật."""
    panel_w, panel_h = 280, 180
    x, y = position
    panel_bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel_bg.fill((0, 0, 0, 150 if is_selected else 100))
    surface.blit(panel_bg, (x, y))
    border_color = YELLOW if is_selected else GRAY
    pygame.draw.rect(surface, border_color, (x, y, panel_w, panel_h), 2)
    
    stats = char_stats.get(char_key, {}) # Dùng .get() để tránh lỗi
    draw_text(surface, stats.get('name', '???'), 28, x + panel_w / 2, y + 25, color=YELLOW)
    draw_text(surface, f"HP: {stats.get('max_hp', 0)}", 20, x + 20, y + 60, align="topleft")
    draw_text(surface, f"Tốc độ: {stats.get('speed', 0)}", 20, x + 150, y + 60, align="topleft")
    draw_text(surface, "Chiêu thức:", 20, x + 20, y + 100, align="topleft", color=WHITE)
    attack_names = list(stats.get('attacks', {}).keys())
    for i, attack in enumerate(attack_names[:3]):
        draw_text(surface, f"- {attack.capitalize()}", 18, x + 30, y + 125 + i * 20, align="topleft", color=GRAY)

def draw_character_select_screen(surface, bg, p1_cursor_pos, char_stats, select_anims, frame_index, game_state, cursor_frames, cursor_index):
    """Vẽ màn hình chọn nhân vật sống động với nhân vật được phóng to và căn chỉnh vị trí."""
    surface.blit(bg, (0, 0))

    p1_char_key = 'A' if p1_cursor_pos == 0 else 'B'
    other_char_key = 'B' if p1_cursor_pos == 0 else 'A'

    # Lấy animation an toàn
    p1_anim_list = []
    other_anim_list = []
    if p1_char_key in select_anims:
        anim_type = 'confirm' if game_state == "CHARACTER_CONFIRMED" else 'idle'
        p1_anim_list = select_anims[p1_char_key].get(anim_type, [])
    if other_char_key in select_anims:
        other_anim_list = select_anims[other_char_key].get('idle', [])

    p1_frame = p1_anim_list[frame_index % len(p1_anim_list)] if p1_anim_list else pygame.Surface((1, 1), pygame.SRCALPHA)
    other_frame = other_anim_list[frame_index % len(other_anim_list)] if other_anim_list else pygame.Surface((1, 1), pygame.SRCALPHA)

    # === THAY ĐỔI 1: ĐIỀU CHỈNH ĐỘ LỚN ===
    # Phóng to nhân vật lên 2.2 lần kích thước gốc. Bạn có thể đổi số này.
    scale_factor = 3
    # =====================================

    original_width = p1_frame.get_width()
    original_height = p1_frame.get_height()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))

    scaled_p1_frame = pygame.transform.scale(p1_frame, new_size)
    scaled_other_frame = pygame.transform.scale(other_frame, new_size)

    # === THAY ĐỔI 2: ĐIỀU CHỈNH VỊ TRÍ ĐỨNG ===
    # Tăng giá trị Y của tâm ảnh (ví dụ: 350) để hạ nhân vật xuống thấp hơn.
    character_y_position = 200
    # ==========================================

    # Vẽ nhân vật bên trái (P1)
    p1_image = pygame.transform.flip(scaled_p1_frame, False, False)
    p1_rect = p1_image.get_rect(center=(SCREEN_WIDTH * 0.25, character_y_position))
    surface.blit(p1_image, p1_rect)

    # Vẽ nhân vật bên phải (AI)
    other_image = pygame.transform.flip(scaled_other_frame, True, False)
    other_rect = other_image.get_rect(center=(SCREEN_WIDTH * 0.75, character_y_position))
    surface.blit(other_image, other_rect)

    # Vẽ 2 khung thông tin ở dưới
    draw_character_info_panel(surface, 'A', char_stats, (40, 400), p1_cursor_pos == 0)
    draw_character_info_panel(surface, 'B', char_stats, (SCREEN_WIDTH - 320, 400), p1_cursor_pos == 1)

    # Vẽ cursor động
    if game_state != "CHARACTER_CONFIRMED" and cursor_frames:
        current_cursor_frame = cursor_frames[cursor_index % len(cursor_frames)]
        cursor_y = 120
        cursor_x = p1_rect.centerx if p1_cursor_pos == 0 else other_rect.centerx
        cursor_rect = current_cursor_frame.get_rect(center=(cursor_x, cursor_y))
        surface.blit(current_cursor_frame, cursor_rect)

    # Vẽ tiêu đề và hướng dẫn
    draw_text(surface, "CHỌN CHIẾN BINH", 40, SCREEN_WIDTH // 2, 50)
    if game_state != "CHARACTER_CONFIRMED":
        draw_text(surface, "Nhấn ENTER để xác nhận", 24, SCREEN_WIDTH // 2, 580)

    return None, None

def draw_difficulty_select_screen(surface, bg, cursor_pos):
    surface.blit(bg, (0, 0))
    draw_text(surface, "CHỌN ĐỘ KHÓ", 50, SCREEN_WIDTH // 2, 80)
    button_w, button_h = 250, 60; button_x = SCREEN_WIDTH // 2
    difficulties = ["DỄ", "TRUNG BÌNH", "KHÓ"]; rects = []
    for i, text in enumerate(difficulties):
        button_y = 200 + i * 80
        is_selected = (i == cursor_pos)
        button_color = YELLOW if is_selected else WHITE
        button_rect = pygame.Rect(0, 0, button_w, button_h); button_rect.center = (button_x, button_y)
        pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
        pygame.draw.rect(surface, GRAY, button_rect, width=3, border_radius=10)
        draw_text(surface, text, 30, button_x, button_y, color=BLACK)
        rects.append(button_rect)
    return rects[0], rects[1], rects[2]

def draw_round_announcement(surface, text):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120)); surface.blit(overlay, (0, 0))
    draw_text_custom_font(surface, FONT_TITLE_PATH, text, 100, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, YELLOW)

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

def draw_battle_hud(surface, player, ai, round_timer, player_wins, ai_wins):
    seconds = max(0, round_timer // 1000)
    draw_text(surface, str(seconds), 60, SCREEN_WIDTH // 2, 30)
    draw_text(surface, player.name, 22, 50, 20, align="topleft")
    draw_health_bar(surface, 50, 50, 300, 25, player.hp, player.max_hp)
    draw_sp_bar(surface, 50, 80, 250, 15, player.sp, player.max_sp)
    for i in range(ROUNDS_TO_WIN):
        color = YELLOW if i < player_wins else GRAY
        pygame.draw.circle(surface, color, (50 + i * 30, 110), 10)
    draw_text(surface, ai.name, 22, SCREEN_WIDTH - 50, 20, align="topright")
    draw_health_bar(surface, SCREEN_WIDTH - 350, 50, 300, 25, ai.hp, ai.max_hp)
    draw_sp_bar(surface, SCREEN_WIDTH - 300, 80, 250, 15, ai.sp, ai.max_sp)
    for i in range(ROUNDS_TO_WIN):
        color = YELLOW if i < ai_wins else GRAY
        pygame.draw.circle(surface, color, ((SCREEN_WIDTH - 50) - i * 30, 110), 10)

def draw_game_over_screen(surface, winner_name):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180)); surface.blit(overlay, (0, 0))
    if winner_name and winner_name != "DRAW": draw_text(surface, f"{winner_name.upper()} WINS!", 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    else: draw_text(surface, "DRAW", 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    replay_rect = pygame.Rect(0, 0, 220, 50); replay_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    pygame.draw.rect(surface, GREEN, replay_rect, border_radius=10)
    draw_text(surface, "Chơi Lại", 24, replay_rect.centerx, replay_rect.centery, color=BLACK)
    quit_rect = pygame.Rect(0, 0, 220, 50); quit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
    pygame.draw.rect(surface, RED, quit_rect, border_radius=10)
    draw_text(surface, "Thoát Game", 24, quit_rect.centerx, quit_rect.centery, color=BLACK)
    return replay_rect, quit_rect