import pygame
import sys
from math import cos, sin, pi as PI

SCREEN_WIDTH, SCREEN_HEIGHT = (640, 480)
TIME_UNIT = 0.05
GRAV = 0.5

BULLET_PATH = "RainbowBall.png"
WORM_PATH = "madzia_small.png"

PLAYER_1, PLAYER_2 = 1, 2

BLACK = (0, 0, 0)

class Worm(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, image_name=WORM_PATH):
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.width = self.rect.width
        self.height = self.rect.height
        
        self.change_x = 0
        self.change_y = 0

    def move(self, event):
        # Check where to move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change_x = -1
            elif event.key == pygame.K_RIGHT:
                self.change_x = 1
            elif event.key == pygame.K_UP:
                self.change_y = -1
            elif event.key == pygame.K_DOWN:
                self.change_y = 1
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.change_x = self.change_x + 1 if self.change_x < 1 else 1
            elif event.key == pygame.K_RIGHT:
                self.change_x = self.change_x - 1 if self.change_x > -1 else -1
            elif event.key == pygame.K_UP:
                self.change_y = self.change_y + 1 if self.change_y < 1 else 1
            elif event.key == pygame.K_DOWN:
                self.change_y = self.change_y - 1 if self.change_y > -1 else -1
    
    def update(self):
         # Update position after moving
        self.rect = self.rect.move(self.change_x, self.change_y)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, v, alpha, image_path=BULLET_PATH):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        # x and y determine where bullet started
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

        # v: speed, assuming constant - no wind resistance
        self.v = v
        # alpha: angle in radians
        self.alpha = alpha

        self.v_x = v * cos(alpha)
        self.v_y = v * sin(alpha)
        
        # t: time
        self.t = 0

    def update(self):
        self.t += TIME_UNIT
        self.rect.x = self.x + self.v_x * self.t
        self.rect.y = self.y - self.v_y * self.t + GRAV * self.t**2 / 2
        

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  

worm = Worm(150, SCREEN_HEIGHT - 150, "madzia_small.png")
worm2 = Worm(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, "ania_small.png")
worms_list = pygame.sprite.Group()
worms_list.add([worm, worm2])

bullet = Bullet(0, 150, 10, PI/4)

mode = PLAYER_1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # TAB to change players 
        if event.type == pygame.KEYDOWN and pygame.key == pygame.K_TAB:
            mode = PLAYER_2 if mode == PLAYER_1 else PLAYER_2

        if mode == PLAYER_1:
            worm.move(event)

        elif mode == PLAYER_2:
            worm2.move(event)


    bullet.update()
    worm.update()

    screen.fill(BLACK)
    screen.blit(worm.image, worm.rect)
    screen.blit(bullet.image, bullet.rect)
    #worms_list.draw(screen)

    pygame.display.flip()




    

    
