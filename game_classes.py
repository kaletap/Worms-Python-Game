""" Implementation of several useful classes:
SpriteSheet
GunPoint
Worm
Bullet
Wall
Player
"""

import pygame, sys, random, string
from math import cos, sin, pi as PI

from defaults import *


class SpriteSheet:
    "Simple class for managing sprite_sheet images"
    def __init__(self, image_path):
        self.sprite_sheet = pygame.image.load(image_path).convert()

    def get_image(self, x, y, width, height):
        """Gets image from sprite sheet starting in (x,y)"""
        image = pygame.Surface((width, height))

        image.blit(self.sprite_sheet, (0,0), area=(x, y, width, height))

        return image


class GunPoint:
    "Represents a red dot which helps in shooting"
    def __init__(self, x, y, color=RED, radius=GUNPOINT_CIRCLE_RADIUS):
        self.x = x
        self.y = y
        self.color = RED
        self.radius = radius


class Worm(pygame.sprite.Sprite):
    """Basic object in a game which can move left and right, 
    jump and shoot Bullet objects"""

    def __init__(self, x, y, sprite_sheet:SpriteSheet, name=None):
        super().__init__()

        self.name = name or ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

        self.sprite_sheet = sprite_sheet
        self.image = self.sprite_sheet.get_image(0, 0, 17, 16)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.change_x = 0
        self.change_y = 0

        self.direction = "right"
        self.change_angle = 0
        self.shooting_angle = PI/4
        self.jumping = False
        self.shooting = False
        self.shooting_power = 0

    def get_gunpoint_coordinates(self):
        if self.direction == "right":
            gunpoint_x = self.rect.x + 16 + int(GUNPOINT_RADIUS * cos(self.shooting_angle))

        else: # self.diretion == "left"
            gunpoint_x = self.rect.x - int(GUNPOINT_RADIUS * cos(self.shooting_angle))
            
        gunpoint_y = self.rect.y - int(GUNPOINT_RADIUS * sin(self.shooting_angle))

        return gunpoint_x, gunpoint_y

    def shoot(self, bullet_list): 
        """Creates a bullet object"""
        x, y = self.get_gunpoint_coordinates()
        # If worm is facing left we shoot a bullet from a point more on the left
        bullet = Bullet(x if self.direction=="right" else x-8, y, 
                        direction=self.direction, 
                        v=self.shooting_power, 
                        alpha=self.shooting_angle,
                        shooted_by = self.name)
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

    def move(self, event, bullet_list):
        """Checks where to move and whether user is shooting"""
    
        if event.type == pygame.KEYDOWN:
            # Moving
            if event.key == pygame.K_LEFT:
                self.change_x = -WORM_SPEED
                self.set_direction("left")
                self.pressed_left = True
            elif event.key == pygame.K_RIGHT:
                self.change_x = WORM_SPEED
                self.set_direction("right")
                self.pressed_right = True

            # Jumping
            elif event.key == pygame.K_SPACE:
                # You cannot jump if you already are jumping
                if self.jumping is False:
                    self.jumping = True
                    self.y_0 = self.rect.y
                    self.t = 0

            # Aiming
            elif event.key == pygame.K_UP:
                self.change_angle = SHOOTING_ANGLE_CHANGE

            elif event.key == pygame.K_DOWN:
                self.change_angle = -SHOOTING_ANGLE_CHANGE

            # Shooting
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.shooting = True
                self.shooting_power = 0

        if event.type == pygame.KEYUP:
            # Moving
            if event.key == pygame.K_LEFT:
                if self.pressed_left:
                    self.change_x = self.change_x + WORM_SPEED if self.change_x < WORM_SPEED else WORM_SPEED
                else : # if KEYUP was done without KEYDOWN first (KDOWN done by previous player)
                    self.change_x = 0
            

            elif event.key == pygame.K_RIGHT:
                if self.pressed_right:
                    self.change_x = self.change_x - WORM_SPEED if self.change_x > -WORM_SPEED else -WORM_SPEED
                else:
                    self.change_x = 0

            # Aiming
            elif event.key == pygame.K_UP:
                self.change_angle = self.change_angle - SHOOTING_ANGLE_CHANGE

            elif event.key == pygame.K_DOWN:
                self.change_angle = self.change_angle + SHOOTING_ANGLE_CHANGE

            # Shooting
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.shooting = False
                self.shoot(bullet_list) 

    def update(self, walls:pygame.sprite.Group = None, gunpoint:GunPoint = None, current_worm=None):
        y_old = self.rect.y

        # Update position in y_direction
        if self.jumping: 
            self.t += TIME_UNIT
            y_new = self.y_0 - JUMP_POWER * self.t + GRAV_WORM * self.t**2 / 2
            self.rect.y = y_new

        else:
            self.rect.y += 1

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

        # Updating aiming
        self.shooting_angle += self.change_angle

        # Update gunpoints coordinates if we are updating active worm
        if self is current_worm:
            #print(GUNPOINT_RADIUS * cos(self.shooting_angle), GUNPOINT_RADIUS * sin(self.shooting_angle))
            gunpoint.x, gunpoint.y = self.get_gunpoint_coordinates()


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
        self.current_worm_id = 0
        
    @property
    def current_worm(self):
        # TODO: hacky, to be changed 
        # (self.current_worm_id might be >= self.worms_number if this function is called in remove_worms
        # after player killed his own worm, which was previous in the list than the current_worm)
        return self.worms[self.current_worm_id] if self.current_worm_id < self.worms_number \
                                                else self.worms[0]
    
    @current_worm.setter
    def current_worm(self, new_worm:Worm):
        self.__current_worm = new_worm

    def move(self, event, bullet_list):
        """Moves current worm"""
        self.current_worm.move(event, bullet_list)

    def stop_worm(self):
        self.current_worm.change_x = 0
        self.current_worm.pressed_left = False
        self.current_worm.pressed_right = False
        self.current_worm.jumping = False
        self.current_worm.shooting = False
        
    def change_worm(self):
        """Changes worm to next one"""
        # First, stop moving current worm (problematic if called after player killed his own worm)
        #print("change worm")
        #print(self.current_worm_id, self.worms_number, len(self.worms))
        self.current_worm.change_x = 0
        new_worm_id = self.current_worm_id + 1
        self.current_worm_id = new_worm_id if new_worm_id < self.worms_number else 0

    def remove_worms(self, killed_worms) -> bool:
        """Removes killed worms from player's list"""
        if killed_worms:
            self.worms = [worm for worm in self.worms if all(worm != w for w in killed_worms)]
            for worm in self.worms:
                worm.change_x = 0
            if len(self.worms) < self.worms_number:
                self.worms_number = len(self.worms)

                # Quiting game if player has no worms left
                if self.worms_number == 0:
                    return True

                # Otherwise, changing worm to not use a killed one
                self.change_worm()

        return False


