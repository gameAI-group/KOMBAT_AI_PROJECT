# --- CÀI ĐẶT CƠ BẢN CỦA GAME ---
SCREEN_WIDTH = 800; SCREEN_HEIGHT = 600; FPS = 60; GAME_TITLE = "Kombat AI"

# --- MÀU SẮC ---
BLACK = (0,0,0); WHITE = (255,255,255); RED = (255,0,0); GREEN = (0,255,0); BLUE = (0,0,255);YELLOW = (255, 255, 0);GRAY = (100, 100, 100)


# --- THÔNG SỐ TRẬN ĐẤU ---
ROUNDS_TO_WIN = 2
ROUND_TIME_LIMIT = 60000 # 60 giây
ROUND_OVER_DELAY = 3000 # 3 giây nghỉ giữa các hiệp

# --- VẬT LÝ VÀ COMBAT ---
GRAVITY = 1; JUMP_POWER = -20; GROUND_Y = 550
DEFAULT_HIT_STUN = 200 # 0.2s
ROLL_DURATION =  400 # 0.4s
ROLL_COOLDOWN_DURATION = 180 # Thời gian hồi chiêu 3 giây
ROLL_SPEED = 10# Tốc độ của cú lướt
COMBO_TIMEOUT = 400


# --- CÀI ĐẶT SP ---
PASSIVE_SP_GAIN_RATE = 3000; PASSIVE_SP_GAIN_AMOUNT = 1
SP_COST_SPECIAL = 45
SP_COST_ROLL = 25 # Chi phí SP cho mỗi lần roll

# --- CHỈ SỐ NHÂN VẬT (LẤY TỪ LUẬT CHƠI) ---
# Dữ liệu cho Nhân vật A ("Người Bảo Hộ Kiên Cường")
CHAR_A_STATS = {
    'name': "Kiếm Sĩ Lửa", 'max_hp': 110, 'max_sp': 100, 'speed': 4, 'air_speed': 5,
    'defense_modifier': 0.4, 'sp_gain_on_block': 8,
    'attacks': {
        'light1': {'damage': 5, 'duration': 330, 'cooldown': 20, 'stun': 200, 'animation': 'assets/images/character_a/05_1_atk/'},
        'light2': {'damage': 7, 'duration': 475, 'cooldown': 20, 'stun': 250, 'animation': 'assets/images/character_a/06_2_atk/'},
        'light3': {'damage': 9, 'knockback': 8, 'duration': 700, 'cooldown': 40, 'stun': 350, 'animation': 'assets/images/character_a/07_3_atk/'},
        'air': {'damage': 8, 'duration': 400, 'cooldown': 30, 'stun': 300, 'animation': 'assets/images/character_a/air_atk/'},
        'special': {'damage': 25, 'knockback': 12, 'duration': 600, 'cooldown': 50, 'stun': 500, 'animation': 'assets/images/character_a/08_sp_atk/'}
    },
    'sp_gain_on_hit': 5, 'sp_gain_on_get_hit': 3,
    'animations': {
        'idle': 'assets/images/character_a/01_idle/', 'run': 'assets/images/character_a/02_run/',
        'jump_up': 'assets/images/character_a/03_jump_up/', 'jump_down': 'assets/images/character_a/03_jump_down/',
        'defend': 'assets/images/character_a/09_defend/', 'roll': 'assets/images/character_a/04_roll/',
        'take_hit': 'assets/images/character_a/10_take_hit/', 'death': 'assets/images/character_a/11_death/'
    },
    'animation_speeds': { 'light1': 30, 'light2': 25, 'light3': 25, 'take_hit': 50, 'death': 150, 'defend': 60,'roll': 90  },
    'hold_frames': { 'defend': 8 }
}

# Dữ liệu cho Nhân vật B ("Sát Thủ Tốc Độ")
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
            'stun': 150, 'animation': 'assets/images/character_b/sp_atk/'
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
BG_MAIN_MENU = 'assets/images/backgrounds/main_menu_bg.png'
BG_CHAR_SELECT = 'assets/images/backgrounds/char_select_bg.png'
BG_STAGE_1 = 'assets/images/backgrounds/stage_01.png'
PORTRAIT_A = 'assets/images/character_a/portrait.png'
PORTRAIT_B = 'assets/images/character_b/portrait.png'
CURSOR_P1 = 'assets/images/ui/p1_cursor.png'