import pygame, sys, random, os, time
from math import cos, sin, pi as PI
import defaults
from defaults import *


class SpriteSheet:
    "Simple class for managing sprite_sheet images"
    def __init__(self, image_path):
        self.sprite_sheet = pygame.image.load(image_path).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))

        image.blit(self.sprite_sheet, (0,0), area=(x, y, width, height))

        return image


class Worm(pygame.sprite.Sprite):
    """Basic object in a game which can move left and right, 
    jump and shoot Bullet objects"""

    def __init__(self, x, y, sprite_sheet:SpriteSheet, name="rick"):
        super().__init__()

        self.name = name

        self.sprite_sheet = sprite_sheet
        self.image = self.sprite_sheet.get_image(0, 0, 17, 16)
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

        self.gun_sight = pygame.draw.circle(pygame.Surface(size=(15, 15)), 
                                            RED, 
                                            (self.rect.x+10, self.rect.y-10),
                                            3
                                            )


    def shoot(self): 
        """Creates a bullet object"""
        bullet = Bullet(self.rect.x, self.rect.y, 
                        direction=self.direction, 
                        v=self.shooting_power, 
                        alpha=PI/4,
                        shooted_by = self.name)
        # TODO: Change this ;__;
        global bullet_list
        bullet_list.add(bullet)

    def set_direction(self, direction):
        """Sets direction and image after moving left/right"""
        self.direction = direction

        x, y = self.rect.x, self.rect.y

        if direction == "left":
            self.image = self.sprite_sheet.get_image(48, 0, 17, 16)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

        elif direction == "right":
            self.image = self.sprite_sheet.get_image(16, 0, 17, 16)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

    def move(self, event):
        """Checks where to move and whether user is shooting"""
    
        if event.type == pygame.KEYDOWN:
            # Moving
            if event.key == pygame.K_LEFT:
                self.change_x = -WORM_SPEED
                self.set_direction("left")
            elif event.key == pygame.K_RIGHT:
                self.change_x = WORM_SPEED
                self.set_direction("right")

            # Jumping
            elif event.key == pygame.K_SPACE:
                # You cannot jump if you already are jumping
                if self.jumping is False:
                    self.jumping = True
                    self.y_0 = self.rect.y
                    self.t = 0

            # Shooting
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.shooting = True
                self.shooting_power = 0
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.change_x = self.change_x + WORM_SPEED if self.change_x < WORM_SPEED else WORM_SPEED
            elif event.key == pygame.K_RIGHT:
                self.change_x = self.change_x - WORM_SPEED if self.change_x > -WORM_SPEED else -WORM_SPEED
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.shooting = False
                self.shoot()

    def update(self, walls:pygame.sprite.Group = None):
        y_old = self.rect.y

        # Update position in y_direction
        if self.jumping: 
            self.t += TIME_UNIT
            y_new = self.y_0 - JUMP_POWER * self.t + GRAV_WORM * self.t**2 / 2
            self.rect.y = y_new

        else:
            self.rect.y += WORM_SPEED

        # Check if worm is not colliding with wall after moving up/down
        if walls:
            block_hit_list = pygame.sprite.spritecollide(self, walls, dokill=False)
            # Stop jumping if we hitted something
            if block_hit_list:
                self.jumping = False
                self.t = 0
            for block in block_hit_list:
                if self.rect.y >= y_old: # Going down  
                    self.rect.bottom = block.rect.top

                elif self.rect.y < y_old: # Going up
                    self.rect.top = block.rect.bottom

        # Update position in x_direction
        self.rect = self.rect.move(self.change_x, 0)

        # Check if worm is not colliding with wall after moving left/right
        if walls:
            block_hit_list = pygame.sprite.spritecollide(self, walls, dokill=False)

            for block in block_hit_list:
                if self.direction == "right":
                    self.rect.right = block.rect.left
                else: # self.direction == "left"
                    self.rect.left = block.rect.right

        # Shooting power:
        if self.shooting:
            self.shooting_power += SHOOTING_POWER_UNIT


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


class Wall(pygame.sprite.Sprite):
    """Implements simple rectangular walls"""
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player:
    """Basic functionalities of a player: storing and changing worms, moving active one"""
    def __init__(self, *worms, name="Player"):
        """Accepts worms as arguments and name as a keyword argument"""
        self.worms = list(worms)
        self.name = name
        self.worms_number = len(self.worms)
        self.current_worm = 0

    def move(self, event:pygame.event.EventType):
        """Moves current worm"""
        self.worms[self.current_worm].move(event)

    def change_worm(self):
        """Changes worm to next one"""
        # First, stop moving current worm
        self.worms[self.current_worm].change_x = 0
        new_worm_num = self.current_worm + 1
        self.current_worm = new_worm_num if new_worm_num < self.worms_number else 0

    def remove_worms(self, killed_worms):
        """Removes killed worms from player's list"""
        if killed_worms:
            self.worms = [worm for worm in self.worms if all(worm != w for w in killed_worms)]
            if len(self.worms) < self.worms_number:
                self.worms_number = len(self.worms)

                # Quiting game if player has no worms left
                if self.worms_number == 0:
                    print("{} won, congratulations".format(self.name))
                    sys.exit()

                # Otherwise, changing worm to not use a killed one
                self.change_worm()


def collided(worm: Worm, bullet: Bullet) -> bool: 
    """ Check whether worm and bullet collide.
    Returns False when bullet was shooted by worm 
    (we doesn't let worm shoot himself)"""
    if worm.name == bullet.shooted_by:
        return False
    else:
        coll = pygame.sprite.collide_rect(worm, bullet)
        # Make a sound if collided
        if coll:
            sound_path = os.path.join('sounds/hits', random.choice(defaults.hit_sound_paths))
            hit_sound = pygame.mixer.Sound(sound_path)
            hit_sound.play()
        return coll


def main():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  
    clock = pygame.time.Clock()

    # Sounds
    pygame.mixer.init()

    # Creating sprite_sheet object (image containing all needed images)
    sprite_sheet_path1 = "F_01.png"
    sprite_sheet1 = SpriteSheet(sprite_sheet_path1)

    sprite_sheet_path2 = "M_09.png"
    sprite_sheet2 = SpriteSheet(sprite_sheet_path2)

    # Creating worms
    worm = Worm(150, SCREEN_HEIGHT - 150, sprite_sheet1, name="artur")
    worm2 = Worm(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, sprite_sheet2, name="dent")
    worm3 = Worm(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 150, sprite_sheet2, name="zaphod")
    worm4 = Worm(SCREEN_WIDTH - 400, SCREEN_HEIGHT - 150, sprite_sheet1, name="beeblebrox")
    # Group containing all worms
    worm_list = pygame.sprite.Group()
    worm_list.add(worm, worm2, worm3, worm4)

    # Creating players
    player1 = Player(worm, worm4, name="Przemek")
    player2 = Player(worm2, worm3, name="Madzia")

    # Creating bullet
    global bullet_list
    bullet_list = pygame.sprite.Group()
    bullet = Bullet(0, 100, direction="right", v=10, alpha=PI/4)
    bullet_list.add(bullet)

    # Creating walls
    wall_list = pygame.sprite.Group()
    floor = Wall(0, SCREEN_HEIGHT-10, SCREEN_WIDTH, 10)
    random.seed(41)
    block1 = Wall(40, 150, 50, 60)
    block2 = Wall(200, 50, 50, 30)
    block3 = Wall(400, 300, 50, 30)
    blocks = [Wall(random.randint(0, SCREEN_WIDTH), 
                random.randint(0, SCREEN_HEIGHT),
                50, 
                10) 
            for _ in range(10)]
    wall_list.add(floor, block1, block2, block3, *blocks)

    #print(id(player1.worms[0]) == id(worm))

    mode = PLAYER_1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Backspace to change players 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                print("Changing players")
                mode = PLAYER_2 if mode == PLAYER_1 else PLAYER_1

            if mode == PLAYER_1:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    player1.change_worm()
                player1.move(event)

            elif mode == PLAYER_2:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    player2.change_worm()
                player2.move(event)

        # Killling worms hitted by bullet
        killed_worms = pygame.sprite.groupcollide(worm_list, bullet_list, dokilla=True, dokillb=True, collided=collided)
        player1.remove_worms(killed_worms.keys())
        player2.remove_worms(killed_worms.keys())

        # Deleting bullets which hitted wall
        pygame.sprite.groupcollide(bullet_list, wall_list, dokilla=True, dokillb=False)

        # Updating bullets and worms
        bullet_list.update()
        worm_list.update(wall_list)

        # Drawing  
        screen.fill(BLACK)
        worm_list.draw(screen)
        bullet_list.draw(screen)
        wall_list.draw(screen)

        clock.tick(2000)

        pygame.display.flip()

if __name__ == "__main__":
    main()




    

    
