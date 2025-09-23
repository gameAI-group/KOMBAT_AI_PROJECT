# --- CÀI ĐẶT CƠ BẢN CỦA GAME ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GUIDE_CONTENT_HEIGHT = 1200 # Chiều cao của toàn bộ nội dung hướng dẫn (lớn hơn chiều cao màn hình)
SCROLL_SPEED = 30           # Tốc độ cuộn (pixel mỗi lần cuộn)
GAME_TITLE = "Kombat AI"

# --- MÀU SẮC ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
PURPLE = (128, 0, 128)

# --- THÔNG SỐ TRẬN ĐẤU ---
ROUNDS_TO_WIN = 2
ROUND_TIME_LIMIT = 60000  # 60 giây
ROUND_OVER_DELAY = 3000   # 3 giây nghỉ giữa các hiệp

# --- VẬT LÝ VÀ COMBAT ---
GRAVITY = 1
JUMP_POWER = -18
GROUND_Y = 550
DEFAULT_HIT_STUN = 200  # 0.2s
ROLL_DURATION = 350     # Tổng thời gian của hành động lướt (0.35s)
ROLL_COOLDOWN_DURATION = 180 # Thời gian hồi chiêu
ROLL_SPEED = 8          # Tốc độ của cú lướt
COMBO_TIMEOUT = 400

# --- CÀI ĐẶT I-FRAME CHO ROLL ---
ROLL_IFRAME_START = 50      # Bất tử bắt đầu sau 50ms (khung hình khởi động)
ROLL_IFRAME_DURATION = 200  # Bất tử kéo dài trong 200ms

# --- CÀI ĐẶT HỒI CHIÊU ĐẶC BIỆT ---
SPECIAL_ATTACK_COOLDOWN = 5000 # 5 giây (tính bằng mili-giây)

# --- CÀI ĐẶT CHO "TECH ROLL" (LƯỚT KHI BỊ ĐÁNH) ---
TECH_ROLL_WINDOW = 150  # Cửa sổ 150ms sau khi trúng đòn để có thể lướt
SP_COST_TECH_ROLL = 35  # Chi phí SP cao hơn cho hành động này

# --- CÀI ĐẶT SP ---
PASSIVE_SP_GAIN_RATE = 3000
PASSIVE_SP_GAIN_AMOUNT = 1
SP_COST_SPECIAL = 45
SP_COST_ROLL = 25       # Chi phí SP cho mỗi lần roll thông thường

# --- THÔNG SỐ NHÂN VẬT A (ĐÃ CẬP NHẬT) ---
# --- THÔNG SỐ NHÂN VẬT A (ĐÃ CẬP NHẬT) ---
CHAR_A_STATS = {
    'lore': "Một kiếm sĩ lang thang với khả năng điều khiển ngọn lửa từ thanh quỷ kiếm. Anh ta chiến đấu để tìm lại danh dự đã mất.",
    'name': "Kiếm Sĩ Lửa", 'max_hp': 120, 'max_sp': 100, 'speed': 4, 'air_speed': 5,
    'defense_modifier': 0.4, 'sp_gain_on_block': 8,
    'attacks': {
        # --- CẬP NHẬT: Thêm 'hit_on_frame' để kiểm soát khi nào hitbox active ---
        'light1': {'display_name': "Chém Thường",'damage': 6, 'duration': 330, 'cooldown': 28, 'stun': 220, 'hit_on_frame': 2, 'animation': 'assets/images/character_a/05_1_atk/'},
        'light2': {'display_name': "Liên Hoàn Trả",'damage': 7, 'duration': 475, 'cooldown': 32, 'stun': 280, 'hit_on_frame': 4, 'animation': 'assets/images/character_a/06_2_atk/'},
        'light3': {'display_name': "Trảm Hỏa",'damage': 9, 'knockback': 8, 'duration': 700, 'cooldown': 50, 'stun': 400, 'hit_on_frame': 8, 'animation': 'assets/images/character_a/07_3_atk/'},
        'air': {'display_name': "Trảm Không",'damage': 10, 'duration': 400, 'cooldown': 30, 'stun': 300, 'hit_on_frame': 5, 'animation': 'assets/images/character_a/air_atk/'},
        'special': {
            'display_name': "Hỏa Long Ba",
            'damage': 25, 'knockback': 15, 'duration': 733, 'cooldown': 50, 'stun': 550, 
            'animation': 'assets/images/character_a/08_sp_atk/',
            'hitbox_size': (200, 200),
            'hitbox_offset': (30, -200)
        }
    },
    'sp_gain_on_hit': 5, 'sp_gain_on_get_hit': 3,
    'animations': {
        'idle': 'assets/images/character_a/01_idle/', 'run': 'assets/images/character_a/02_run/',
        'jump_up': 'assets/images/character_a/03_jump_up/', 'jump_down': 'assets/images/character_a/03_jump_down/',
        'defend': 'assets/images/character_a/09_defend/', 'roll': 'assets/images/character_a/04_roll/',
        'take_hit': 'assets/images/character_a/10_take_hit/', 'death': 'assets/images/character_a/11_death/'
    },
    # --- CẬP NHẬT: Tăng giá trị để làm chậm animation ---
     'animation_speeds': { 'light1': 25, 'light2': 35, 'light3': 30, 'special': 25, 'air': 40, 'death': 100, 'defend': 60,'roll': 80 },
    'hold_frames': { 'defend': 8 }
}

# --- THÔNG SỐ NHÂN VẬT B (ĐÃ CẬP NHẬT) ---
CHAR_B_STATS = {
    'lore': "Một sát thủ nhanh nhẹn thuộc một tổ chức bí ẩn. Hắn sử dụng song đao để kết liễu mục tiêu trong chớp mắt.",
    'name': "Sát Thủ Tốc Độ", 'max_hp': 90, 'max_sp': 100, 'speed': 4.6, 'air_speed': 6,
    'defense_modifier': 0.6, 'sp_gain_on_combo_finish': 10,
    'attacks': {
        'light1': {'display_name': "Chém Thường",'damage': 7, 'duration': 200, 'cooldown': 12, 'stun': 160, 'hit_on_frame': 2, 'animation': 'assets/images/character_b/1_atk/'},
        'light2': {'display_name': "Song Đao Liên Ảnh",'damage': 8, 'duration': 350, 'cooldown': 15, 'stun': 260, 'hit_on_frame': 5, 'animation': 'assets/images/character_b/2_atk/'}, # Duration giảm ~6 frame
        'light3': {'display_name': "Liên Vũ Phong Đao",'damage': 10, 'knockback': 10, 'duration': 647, 'cooldown': 35, 'stun': 320, 'hit_on_frame': 14, 'animation': 'assets/images/character_b/3_atk/'}, # Duration giảm ~8 frame
        'air': {'display_name': "Đoạn Không Trảm",'damage': 12, 'duration': 350, 'cooldown': 25, 'stun': 350, 'hit_on_frame': 4, 'animation': 'assets/images/character_b/air_atk/'},
        'special': {
            'display_name': "Vô Ảnh Sát",
            'damage': 10, 'hits': 3, 'hit_frames': [11, 17, 20],
            'knockback_on_last_hit': 15, 'duration': 800, 'cooldown': 55,
            'stun': 120, 'animation': 'assets/images/character_b/sp_atk/',
            'hitbox_size': (80, 190),
            'hitbox_offset': (10, -185),
            'range_box': {'size': (250, 250), 'offset': (10, -250)}
        }
    },
    'sp_gain_on_hit': 5, 'sp_gain_on_get_hit': 3,
    'animations': {
        'idle': 'assets/images/character_b/idle/', 'run': 'assets/images/character_b/run/',
        'jump_up': 'assets/images/character_b/j_up/', 'jump_down': 'assets/images/character_b/j_down/',
        'defend': 'assets/images/character_b/defend/', 'roll': 'assets/images/character_b/roll/',
        'take_hit': 'assets/images/character_b/take_hit/', 'death': 'assets/images/character_b/death/'
    },
    'animation_speeds': { 'light1': 25, 'light2': 25, 'light3': 30, 'special': 25, 'air': 40, 'death': 100, 'defend': 60,'roll': 80  },
    'hold_frames': { 'defend': 5 }
}

# --- ĐƯỜNG DẪN TÀI NGUYÊN ---
FONT_PATH = 'assets/fonts/main_font.ttf'
FONT_TITLE_PATH = 'assets/fonts/BoldPixels.ttf'

BG_MAIN_MENU = 'assets/images/backgrounds/main_menu_bg.png'
BG_CHAR_SELECT = 'assets/images/backgrounds/char_select_bg.png'
BG_STAGE_1 = 'assets/images/backgrounds/stage_01.png'

PORTRAIT_A = 'assets/images/character_a/portrait.png'
PORTRAIT_B = 'assets/images/character_b/portrait.png'
CURSOR_P1 = 'assets/images/ui/p1_cursor.png'
LOGO_IMAGE = 'assets/images/ui/logo.png'

MUSIC_MENU = 'assets/audio/music/menu_music.mp3'
MUSIC_BATTLE = 'assets/audio/music/battle_music.mp3'
MUSIC_CHAR_SELECT = 'assets/audio/music/char_select_music.mp3'
MUSIC_WIN = 'assets/audio/music/victory_music.mp3'  # Nhạc khi người chơi thắng
MUSIC_LOSE = 'assets/audio/music/defeat_music.mp3' # Nhạc khi người chơi thua (hoặc hòa)

SFX_ROUND_1 = 'assets/audio/sfx/round1.wav'
SFX_ROUND_2 = 'assets/audio/sfx/round2.wav'
SFX_FINAL_ROUND = 'assets/audio/sfx/final_round.wav'
SFX_COUNTDOWN = 'assets/audio/sfx/countdown.wav'
SFX_FIGHT = 'assets/audio/sfx/fight.wav'
SFX_CONFIRM = 'assets/audio/sfx/select_confirm.wav'
SFX_JUMP = 'assets/audio/sfx/jump.wav'
SFX_HIT_A = 'assets/audio/sfx/hit4A.wav'      # Âm thanh đánh của Kiếm Sĩ
SFX_HIT_B = 'assets/audio/sfx/hit4B.wav'      # Âm thanh đánh của Sát Thủ
SFX_AIR_HIT = 'assets/audio/sfx/airhit.wav'   # Âm thanh khi đòn đánh trên không trúng

# --- CÀI ĐẶT CHO ĐẾM NGƯỢC ---
ROUND_ANNOUNCE_DURATION = 2000 # Thời gian hiển thị "Round X" (2 giây)
COUNTDOWN_STEP_DURATION = 1000 # Thời gian mỗi bước đếm ngược "3, 2, 1" (1 giây)
FIGHT_ANNOUNCE_DURATION = 1000 # Thời gian hiển thị "FIGHT!" (1 giây)
CONFIRMATION_DURATION = 1500