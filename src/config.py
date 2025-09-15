# src/config.py

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

# --- HẰNG SỐ VẬT LÝ VÀ GAMEPLAY ---
GRAVITY = 1
JUMP_POWER = -20 
GROUND_Y = 430 # Vị trí "mặt đất"
PASSIVE_SP_GAIN_RATE = 3000
PASSIVE_SP_GAIN_AMOUNT = 1
COMBO_WINDOW = 500
ROLL_DURATION = 250
ROLL_COOLDOWN = 2000
SPECIAL_ATTACK_COST = 30

# ===> THÊM MỚI: CÁC HẰNG SỐ COMBAT <===
STUN_LIGHT = 200     # 0.2 giây cho đòn nhẹ
STUN_CHAIN = 150     # 0.15 giây cho đòn nối
STUN_ENDER = 100     # 0.1 giây cho đòn kết thúc
KNOCKBACK_DISTANCE = 80 # Khoảng cách bị đẩy lùi

# --- CÀI ĐẶT ANIMATION ---
ANIMATION_COOLDOWN = 100
# HIT_STUN_DURATION sẽ được thay thế bằng các giá trị động ở trên
DEFAULT_STUN_DURATION = 300 # Stun mặc định cho các đòn không thuộc combo

# --- CHỈ SỐ NHÂN VẬT (LẤY TỪ LUẬT CHƠI) ---
# Dữ liệu cho Nhân vật A - "Người Bảo Hộ Kiên Cường"
CHAR_A_STATS = {
    'name': "Kiếm Sĩ Lửa",
    'max_hp': 110,
    'max_sp': 100,  
    'speed': 4,
    'damage_light': 5,
    'damage_chain': 7,
    'damage_ender': 9,
    'damage_air': 8,
    'special_damage': 25,
    'damage_reduction': 0.6,
    'sp_gain_on_hit': 5, 
    'sp_gain_on_get_hit': 3,
    'sp_gain_on_defend': 8,
    'animations': {
        'idle':      'assets/images/character_a/01_idle/',
        'run':       'assets/images/character_a/02_run/',
        'jump_up':   'assets/images/character_a/03_jump_up/',
        'jump_down': 'assets/images/character_a/03_jump_down/',
        'roll':      'assets/images/character_a/04_roll/',
        '1_atk':     'assets/images/character_a/05_1_atk/',
        '2_atk':     'assets/images/character_a/06_2_atk/',
        '3_atk':     'assets/images/character_a/07_3_atk/',
        'sp_atk':    'assets/images/character_a/08_sp_atk/',
        'defend':    'assets/images/character_a/09_defend/',
        'take_hit':  'assets/images/character_a/10_take_hit/',
        'death':     'assets/images/character_a/11_death/',
        'air_atk':   'assets/images/character_a/air_atk/'
    },
    'animation_speeds': {'1_atk': 85, '2_atk': 85, '3_atk': 85}
}

# Dữ liệu cho Nhân vật B - "Sát Thủ Tốc Độ"
CHAR_B_STATS = {
    'name': "Sát Thủ Tốc Độ",
    'max_hp': 90,
    'max_sp': 100,  
    'speed': 4.6,
    'damage_light': 7,
    'damage_chain': 9,
    'damage_ender': 11,
    'damage_air': 12,
    'special_damage': 30,
    'damage_reduction': 0.4,
    'sp_gain_on_hit': 5, 
    'sp_gain_on_get_hit': 3,
    'sp_gain_on_combo_ender': 10,
    'animations': {
        'idle':      'assets/images/character_b/idle/',
        'run':       'assets/images/character_b/run/',
        'jump_up':   'assets/images/character_b/j_up/',
        'jump_down': 'assets/images/character_b/j_down/',
        'roll':      'assets/images/character_b/roll/',
        '1_atk':     'assets/images/character_b/1_atk/',
        '2_atk':     'assets/images/character_b/2_atk/',
        '3_atk':     'assets/images/character_b/3_atk/',
        'sp_atk':    'assets/images/character_b/sp_atk/',
        'defend':    'assets/images/character_b/defend/',
        'take_hit':  'assets/images/character_b/take_hit/',
        'death':     'assets/images/character_b/death/',
        'air_atk':   'assets/images/character_b/air_atk/'
    },
    'animation_speeds': {}
}


# --- ĐƯỜNG DẪN TÀI NGUYÊN ---
FONT_PATH = 'assets/fonts/main_font.ttf'
BG_MAIN_MENU = 'assets/images/backgrounds/main_menu_bg.png'
BG_CHAR_SELECT = 'assets/images/backgrounds/char_select_bg.png'
BG_STAGE_1 = 'assets/images/backgrounds/stage_01.png'
PORTRAIT_A = 'assets/images/character_a/portrait.png'
PORTRAIT_B = 'assets/images/character_b/portrait.png'
CURSOR_P1 = 'assets/images/ui/p1_cursor.png'