import pygame
from src.fighter import Fighter

pygame.init()

player = Fighter('A', x=200, y=330, is_player_one=True)
enemy = Fighter('B', x=600, y=330, is_player_one=False)

# Test tấn công thường
player.reset()
player.in_air = False
player.defending = False
player.attacking = False
player.attack(enemy, 'light')
print("Tấn công thường:", player.attacking, player.action)

# Test tấn công đặc biệt
player.reset()
player.in_air = False
player.sp = player.max_sp
player.attack(enemy, 'special')
print("Tấn công đặc biệt:", player.attacking, player.action)

# Test nhảy
player.reset()
player.jumps_left = 2
player.jump()
print("Nhảy:", player.in_air, player.jumps_left)

# Test roll
player.reset()
player.sp = player.max_sp
player.roll()
print("Roll:", player.rolling)

# Test phòng thủ
player.reset()
player.in_air = False
player.defend(True)
print("Phòng thủ:", player.defending)
pygame.quit()