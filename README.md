KOMBAT_AI_PROJECT/
│
├── assets/
│   ├── images/
│   │   ├── character_a/
│   │   │   ├── portrait.png          <-- Ảnh đại diện nhân vật để chọn khi menu chọn nhân vật
│   │   │   ├── 01_idle/              <-- Animation đứng yên (idle) của nhân vật A
│   │   │   ├── 02_run/               <-- Animation chạy
│   │   │   └── ...                   <-- Các folder khác: attack, jump, hit, die…
│   │   ├── character_b/              <-- Tương tự character_a, nhưng là nhân vật B
│   │   │   ├── portrait.png
│   │   │   ├── 01_idle/
│   │   │   └── ...
│   │   ├── backgrounds/
│   │   │   ├── main_menu_bg.png      <-- Background menu chính
│   │   │   ├── char_select_bg.png    <-- Background màn hình chọn nhân vật
│   │   │   └── stage_01.png          <-- Background của stage 1
│   │   └── ui/
│   │       ├── HP_SP_frame.png  <-- Khung thanh máu
│   │       ├── p1_cursor.png         <-- Con trỏ người chơi 1
│   │       ├── cpu_cursor.png        <-- Con trỏ AI / CPU
│   │       └── button_restart.png    <-- Nút restart game
│   ├── audio/
│   │   ├── music/
│   │   │   ├── menu_music.mp3        <-- Nhạc nền menu
│   │   │   └── battle_music.mp3      <-- Nhạc nền khi battle
│   │   └── sfx/
│   │       ├── select_move.wav       <-- Âm thanh di chuyển con trỏ khi chọn
│   │       └── select_confirm.wav    <-- Âm thanh khi confirm chọn
│   └── fonts/
│       └── main_font.ttf             <-- Font chữ chính của game
│
├── src/
│   ├── __init__.py
│   ├── config.py                     <-- Các thông số cấu hình game (screen size, FPS,…)
│   ├── game.py                       <-- Quản lý flow game: menu, chọn nhân vật, battle
│   ├── fighter.py                    <-- Quản lý fighter: máu, animation, di chuyển, attack
│   ├── ui.py                         <-- Giao diện: vẽ health bar, menu, cursors
│   └── ai/
│       ├── __init__.py
│       ├── ai_base.py                <-- Lớp base cho tất cả AI
│       ├── ai_random.py              <-- AI đánh ngẫu nhiên
│       ├── ai_rule_based.py          <-- AI theo luật (rule-based)
│       └── ai_heuristic.py           <-- AI nâng cao, heuristic
│
├── main.py                           <-- Entry point của game, chạy loop chính
├── requirements.txt                  <-- Thư viện cần cài (pygame,…)
├── README.md                          <-- Giới thiệu, hướng dẫn cài đặt & chơi
└── README_rules.md                    <-- Hướng dẫn rules / cơ chế combat game