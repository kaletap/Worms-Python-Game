import pygame
import sys
from math import cos, sin, pi as PI

SCREEN_WIDTH, SCREEN_HEIGHT = (640, 480)
TIME_UNIT = 0.05
SHOOTING_CHANGE_UNIT = 0.05
GRAV = 1
GRAV_WORM = 2
JUMP_POWER = 15
WORM_SPEED = 1

BULLET_PATH = "RainbowBall.png"
WORM_PATH = "madzia_small.png"

PLAYER_1, PLAYER_2 = 1, 2

BLACK = (0, 0, 0)

class Worm(pygame.sprite.Sprite):
    """Basic object in a game which can move left and right,
    jump and shoot"""

    def __init__(self, x=0, y=0, image_path=WORM_PATH, name="rick"):
        super().__init__()

        self.name = name
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.width = self.rect.width
        self.height = self.rect.height
        
        self.change_x = 0
        self.change_y = 0

        self.direction = "right"
        self.jumping = False
        self.shooting = False

    def shoot(self): 
        # Creating bullet object
        bullet = Bullet(self.rect.x, self.rect.y, 
                        direction=self.direction, 
                        v=self.shooting_power, 
                        alpha=PI/4,
                        shooted_by = self.name)
        global bullet_list
        bullet_list.add(bullet)

    def move(self, event):
        # Check where to move and if user is shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change_x = -WORM_SPEED
                self.direction = "left"
            elif event.key == pygame.K_RIGHT:
                self.change_x = WORM_SPEED
                self.direction = "right"
            elif event.key == pygame.K_UP:
                self.change_y = -WORM_SPEED
            elif event.key == pygame.K_DOWN:
                self.change_y = WORM_SPEED
            elif event.key == pygame.K_SPACE:
                # You cannot jump if you already are jumping
                if self.jumping is False:
                    self.jumping = True
                    self.y_0 = self.rect.y
                    self.t = 0
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.shooting = True
                self.shooting_power = 0
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.change_x = self.change_x + WORM_SPEED if self.change_x < WORM_SPEED else WORM_SPEED
            elif event.key == pygame.K_RIGHT:
                self.change_x = self.change_x - WORM_SPEED if self.change_x > -WORM_SPEED else -WORM_SPEED
            elif event.key == pygame.K_UP:
                self.change_y = self.change_y + WORM_SPEED if self.change_y < WORM_SPEED else WORM_SPEED
            elif event.key == pygame.K_DOWN:
                self.change_y = self.change_y - WORM_SPEED if self.change_y > -WORM_SPEED else -WORM_SPEED
            elif event.key == pygame.K_KP_ENTER:
                self.shooting = False
                self.shoot()

    def update(self):
         # Update position after jumping
        if self.jumping: 
            self.t += TIME_UNIT
            y_new = self.y_0 - JUMP_POWER * self.t + GRAV_WORM * self.t**2 / 2
            if y_new >= SCREEN_HEIGHT - 100:
                self.jumping = False
                self.t = 0
            else:
                self.rect.y = y_new

        # Update movement in x_direction
        self.rect = self.rect.move(self.change_x, 0)

        # Shooting power:
        if self.shooting:
            self.shooting_power += SHOOTING_CHANGE_UNIT


class Bullet(pygame.sprite.Sprite):
    """Class implementing Bullet object"""
    def __init__(self, x, y, direction="right", v=1, alpha=PI/4, image_path=BULLET_PATH, shooted_by=None):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        # x and y determine where bullet started
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

        # name of a worm which shooted
        self.shooted_by = shooted_by

        # v: speed, assuming constant - no wind resistance
        self.v = v

        # alpha: angle in radians
        self.alpha = alpha

        # direction: "left" or "right"
        self.direction = direction

        self.v_x = v * cos(alpha)
        self.v_y = v * sin(alpha)
        
        # t: time
        self.t = 0

    def update(self):
        # Updating time
        self.t += TIME_UNIT

        # Updating change in x direction
        if self.direction == "right":
            self.rect.x = self.x + self.v_x * self.t
        else: # self.direction == "left"
            self.rect.x = self.x - self.v_x * self.t

        # Updating change in y direction
        self.rect.y = self.y - self.v_y * self.t + GRAV * self.t**2 / 2

        # Deleting bullet if out of screen
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()


def collided(worm: Worm, bullet: Bullet) -> bool: 
    """ Check whether worm and bullet collide.
    Returns False when bullet was shooted by worm 
    (we doesn't let worm shoot himself)"""
    if worm.name == bullet.shooted_by:
        return False
    else:
        return pygame.sprite.collide_rect(worm, bullet)


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  
clock = pygame.time.Clock()

worm = Worm(150, SCREEN_HEIGHT - 100, "madzia_small.png", name="artur")
worm2 = Worm(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, "ania_small.png", name="dent")
worm_list = pygame.sprite.Group()
worm_list.add([worm, worm2])

bullet_list = pygame.sprite.Group()
bullet = Bullet(0, 150, direction="right", v=10, alpha=PI/4)
bullet_list.add(bullet)

mode = PLAYER_1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # TAB to change players 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            print("Changing players")
            mode = PLAYER_2 if mode == PLAYER_1 else PLAYER_1

        if mode == PLAYER_1:
            worm.move(event)

        elif mode == PLAYER_2:
            worm2.move(event)

    pygame.sprite.groupcollide(worm_list, bullet_list, dokilla=True, dokillb=True, collided=collided)
    bullet_list.update()
    worm_list.update()

    screen.fill(BLACK)
    worm_list.draw(screen)
    bullet_list.draw(screen)

    clock.tick()
    pygame.display.flip()




    

    
