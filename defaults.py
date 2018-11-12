import pygame, os
from math import pi as PI

SCREEN_WIDTH, SCREEN_HEIGHT = (640, 480)

TIME_UNIT = 0.05
SHOOTING_POWER_UNIT = 0.05
SHOOTING_ANGLE_CHANGE = PI / 1000
GRAV = 1
GRAV_WORM = 2
JUMP_POWER = 15
WORM_SPEED = 1

GUNPOINT_RADIUS = 10
GUNPOINT_CIRCLE_RADIUS = 2

BULLET_PATH = "RainbowBall.png"

PLAYER_1, PLAYER_2 = 1, 2

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

hit_sound_paths = os.listdir("sounds/hits")

