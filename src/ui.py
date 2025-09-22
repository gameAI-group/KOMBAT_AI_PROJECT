import pygame
from .config import *

# (Các hàm draw_text và draw_text_custom_font giữ nguyên)
def draw_text_custom_font(surface, font_path, text, size, x, y, color=WHITE, align="center"):
    try:
        font = pygame.font.Font(font_path, size)
    except Exception:
        font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center": text_rect.center = (x, y)
    elif align == "topleft": text_rect.topleft = (x, y)
    elif align == "topright": text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect

def draw_text(surface, text, size, x, y, color=WHITE, align="center"):
    return draw_text_custom_font(surface, FONT_PATH, text, size, x, y, color, align)

# (Hàm draw_main_menu_screen giữ nguyên)
def draw_main_menu_screen(surface, bg, logo_image):
    surface.blit(bg, (0, 0))
    if logo_image:
        logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, 180))
        surface.blit(logo_image, logo_rect)
    else:
        draw_text_custom_font(surface, FONT_TITLE_PATH, "KOMBAT AI", 90, SCREEN_WIDTH // 2, 180, YELLOW)
    button_w, button_h = 300, 65; button_x = SCREEN_WIDTH // 2
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

# (Hàm draw_detailed_character_info giữ nguyên)
def draw_detailed_character_info(surface, stats, position):
    panel_x, panel_y = position
    panel_w, panel_h = 380, 480
    panel_bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel_bg.fill((10, 20, 30, 220))
    surface.blit(panel_bg, (panel_x, panel_y))
    pygame.draw.rect(surface, GRAY, (panel_x, panel_y, panel_w, panel_h), 2)
    draw_text_custom_font(surface, FONT_PATH, stats.get('name', '???'), 40, panel_x + panel_w / 2, panel_y + 35, color=YELLOW)
    lore_text = stats.get('lore', 'Không có thông tin.')
    words = lore_text.split(' ')
    line = ""
    line_y = panel_y + 75
    for word in words:
        if draw_text(surface, line + word, 17, 0, 0).width > panel_w - 40:
            draw_text(surface, line, 17, panel_x + 20, line_y, color=WHITE, align="topleft")
            line = word + " "
            line_y += 20
        else:
            line += word + " "
    draw_text(surface, line, 17, panel_x + 20, line_y, color=WHITE, align="topleft")
    separator_y = line_y + 25
    pygame.draw.line(surface, GRAY, (panel_x + 15, separator_y), (panel_x + panel_w - 15, separator_y), 1)
    stats_y_start = separator_y + 15
    draw_text(surface, "Chỉ Số Cơ Bản", 22, panel_x + panel_w / 2, stats_y_start, color=WHITE)
    hp_text = f"Máu (HP): {stats.get('max_hp', 'N/A')}"
    draw_text(surface, hp_text, 20, panel_x + 25, stats_y_start + 35, align="topleft")
    speed_text = f"Tốc Độ: {stats.get('speed', 'N/A')}"
    draw_text(surface, speed_text, 20, panel_x + 25, stats_y_start + 60, align="topleft")
    defense_mod = stats.get('defense_modifier', 0)
    damage_reduction = int((1 - defense_mod) * 100)
    defense_text = f"Giảm Sát Thương: {damage_reduction}%"
    draw_text(surface, defense_text, 20, panel_x + 25, stats_y_start + 85, align="topleft")
    skills_y_start = stats_y_start + 120
    draw_text(surface, "Danh Sách Chiêu", 22, panel_x + panel_w / 2, skills_y_start, color=GREEN)
    attacks = stats.get('attacks', {})
    for i, (attack_key, attack_data) in enumerate(attacks.items()):
        display_name = attack_data.get('display_name', attack_key.capitalize())
        damage = attack_data.get('damage', '?')
        hits = attack_data.get('hits', 1)
        damage_text = f"{damage} x {hits} hits" if hits > 1 else str(damage)
        line_text = f"- {display_name}: {damage_text} ST"
        draw_text(surface, line_text, 19, panel_x + 25, skills_y_start + 35 + i * 28, align="topleft", color=GRAY)


# --- HÀM VẼ MÀN HÌNH CHỌN NHÂN VẬT (ĐÃ SỬA LỖI LẬT ẢNH) ---
def draw_character_select_screen(surface, bg, p1_cursor_pos, char_stats, select_anims, frame_index, game_state, cursor_frames, cursor_index, portraits):
    surface.blit(bg, (0, 0))
    draw_text(surface, "CHỌN CHIẾN BINH", 40, SCREEN_WIDTH // 2, 40)
    draw_text(surface, "Nhấn ENTER để xác nhận", 24, SCREEN_WIDTH // 2, 580)

    char_keys = ['A', 'B']
    selected_char_key = char_keys[p1_cursor_pos]

    # Vẽ các portrait bên trái
    portrait_x = 80
    for i, key in enumerate(char_keys):
        portrait_img = portraits.get(key)
        if portrait_img:
            p_rect = portrait_img.get_rect(center=(portrait_x, 150 + i * 200))
            surface.blit(portrait_img, p_rect)
            if i == p1_cursor_pos:
                pygame.draw.rect(surface, YELLOW, (p_rect.x-4, p_rect.y-4, p_rect.width+8, p_rect.height+8), 4, border_radius=5)

    character_x_position = SCREEN_WIDTH // 2 - 150
    character_y_position = 330

    # Vẽ nhân vật idle ở giữa
    anim_list = select_anims.get(selected_char_key, {}).get('idle', [])
    if anim_list:
        frame = anim_list[frame_index % len(anim_list)]
        scale_factor = 3.5
        new_size = (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor))
        scaled_frame = pygame.transform.scale(frame, new_size)

        # --- THAY ĐỔI Ở ĐÂY ---
        # Bỏ đi việc lật ảnh. Nhân vật sẽ luôn được vẽ với hướng gốc của file ảnh.
        final_frame = scaled_frame
        # ----------------------
        
        frame_rect = final_frame.get_rect(center=(character_x_position, character_y_position))
        surface.blit(final_frame, frame_rect)

    # Vẽ bảng thông tin chi tiết bên phải
    selected_stats = char_stats.get(selected_char_key)
    if selected_stats:
        draw_detailed_character_info(surface, selected_stats, (SCREEN_WIDTH - 400, 80))

    return None, None

# (Tất cả các hàm còn lại giữ nguyên)
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
# --- HÀM draw_health_bar ĐÃ THAY ĐỔI ---
def draw_health_bar(surface, x, y, width, height, hp, max_hp):
    ratio = max(0, hp / max_hp)
    
    # Vẽ nền và viền
    pygame.draw.rect(surface, (80,0,0), (x, y, width, height)) # Nền đỏ sẫm
    
    # THAY ĐỔI 1: Màu thanh máu là MÀU ĐỎ (RED)
    pygame.draw.rect(surface, RED, (x, y, width * ratio, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)

    # THAY ĐỔI 2: Vẽ số máu
    hp_text = f"{int(hp)} / {int(max_hp)}"
    draw_text(surface, hp_text, 16, x + width / 2, y + height / 2, color=WHITE)

# --- HÀM draw_sp_bar ĐÃ THAY ĐỔI ---
def draw_sp_bar(surface, x, y, width, height, sp, max_sp):
    ratio = max(0, sp / max_sp)
    
    # Vẽ nền và viền
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))
    pygame.draw.rect(surface, BLUE, (x, y, width * ratio, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)
    
    # THAY ĐỔI: Vẽ số năng lượng
    sp_text = f"{int(sp)} / {int(max_sp)}"
    draw_text(surface, sp_text, 14, x + width / 2, y + height / 2, color=WHITE)
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
# --- MỚI: Class để quản lý hiệu ứng số sát thương ---
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, font, color):
        super().__init__()
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.creation_time = pygame.time.get_ticks()
        self.duration = 800  # Tồn tại trong 0.8 giây
        self.y_velocity = -2 # Di chuyển lên trên

    def update(self):
        # Di chuyển số lên trên
        self.rect.y += self.y_velocity

        # Mờ dần theo thời gian
        elapsed_time = pygame.time.get_ticks() - self.creation_time
        if elapsed_time > self.duration:
            self.kill() # Tự hủy khi hết thời gian
            return

        alpha = 255 - (elapsed_time / self.duration) * 255
        self.image.set_alpha(max(0, alpha))