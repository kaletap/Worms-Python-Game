import pygame, os
from math import pi as PI

SCREEN_WIDTH, SCREEN_HEIGHT = (640, 480)
MENU_WIDTH, MENU_HEIGHT = (200, 480)

FRAME_RATE = 1000

TIME_UNIT = 0.05
SHOOTING_POWER_UNIT = 0.05
SHOOTING_ANGLE_CHANGE = PI / 500
GRAV = 3
GRAV_WORM = 3
JUMP_POWER = 15
WORM_SPEED = 1

PL, EN = "PL", "ENG"
ON, OFF = "ON", "OFF"

GUNPOINT_RADIUS = 10
GUNPOINT_CIRCLE_RADIUS = 2

BULLET_PATH = os.path.join("graphics", "RainbowBall.png")
player1_image_paths = os.listdir("graphics/Males")
player2_image_paths = os.listdir("graphics/Females")

PLAYER_1, PLAYER_2 = 1, 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

hit_sound_paths = os.listdir("sounds/hits")

