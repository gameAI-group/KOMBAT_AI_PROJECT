# --- CÀI ĐẶT CƠ BẢN CỦA GAME ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
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

# --- THÔNG SỐ NHÂN VẬT A ---
CHAR_A_STATS = {
    'name': "Kiếm Sĩ Lửa", 'max_hp': 110, 'max_sp': 100, 'speed': 4, 'air_speed': 5,
    'defense_modifier': 0.4, 'sp_gain_on_block': 8,
    'attacks': {
        'light1': {'damage': 5, 'duration': 330, 'cooldown': 20, 'stun': 200, 'animation': 'assets/images/character_a/05_1_atk/'},
        'light2': {'damage': 7, 'duration': 475, 'cooldown': 20, 'stun': 250, 'animation': 'assets/images/character_a/06_2_atk/'},
        'light3': {'damage': 9, 'knockback': 8, 'duration': 700, 'cooldown': 40, 'stun': 350, 'animation': 'assets/images/character_a/07_3_atk/'},
        'air': {'damage': 8, 'duration': 400, 'cooldown': 30, 'stun': 300, 'animation': 'assets/images/character_a/air_atk/'},
        'special': {
            'damage': 25, 'knockback': 12, 'duration': 600, 'cooldown': 50, 'stun': 500,
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
    'animation_speeds': { 'light1': 30, 'light2': 25, 'light3': 30, 'take_hit': 50, 'death': 150, 'defend': 60,'roll': 90  },
    'hold_frames': { 'defend': 8 }
}

# --- THÔNG SỐ NHÂN VẬT B ---
CHAR_B_STATS = {
    'name': "Sát Thủ Tốc Độ", 'max_hp': 90, 'max_sp': 100, 'speed': 4.6, 'air_speed': 6,
    'defense_modifier': 0.6, 'sp_gain_on_combo_finish': 10,
    'attacks': {
        'light1': {'damage': 7, 'duration': 200, 'cooldown': 15, 'stun': 180, 'hit_on_frame': 3, 'animation': 'assets/images/character_b/1_atk/'},
        'light2': {'damage': 9, 'duration': 450, 'cooldown': 15, 'stun': 300, 'hit_on_frame': 5, 'animation': 'assets/images/character_b/2_atk/'},
        'light3': {'damage': 11, 'knockback': 10, 'duration': 780, 'cooldown': 35, 'stun': 400, 'hit_on_frame': 18, 'animation': 'assets/images/character_b/3_atk/'},
        'air': {'damage': 12, 'duration': 350, 'cooldown': 25, 'stun': 350, 'hit_on_frame': 4, 'animation': 'assets/images/character_b/air_atk/'},
        'special': {
            'damage': 10, 'hits': 3, 'hit_frames': [11, 17, 20],
            'knockback_on_last_hit': 15, 'duration': 800, 'cooldown': 60,
            'stun': 150, 'animation': 'assets/images/character_b/sp_atk/',
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

SFX_ROUND_1 = 'assets/audio/sfx/round1.wav'
SFX_ROUND_2 = 'assets/audio/sfx/round2.wav'
SFX_FINAL_ROUND = 'assets/audio/sfx/final_round.wav'
SFX_COUNTDOWN = 'assets/audio/sfx/countdown.wav'
SFX_FIGHT = 'assets/audio/sfx/fight.wav'
SFX_CONFIRM = 'assets/audio/sfx/select_confirm.wav'

# --- CÀI ĐẶT CHO ĐẾM NGƯỢC ---
ROUND_ANNOUNCE_DURATION = 2000 # Thời gian hiển thị "Round X" (2 giây)
COUNTDOWN_STEP_DURATION = 1000 # Thời gian mỗi bước đếm ngược "3, 2, 1" (1 giây)
FIGHT_ANNOUNCE_DURATION = 1000 # Thời gian hiển thị "FIGHT!" (1 giây)