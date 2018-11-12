#!opt/anaconda/bin/python
import pygame, sys, random, os, time, string
from math import cos, sin, pi as PI
import defaults
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

    def get_gunpoint_coordinates(self):
        if self.direction == "right":
            gunpoint_x = self.rect.x + 16 + int(GUNPOINT_RADIUS * cos(self.shooting_angle))

        else: # self.diretion == "left"
            gunpoint_x = self.rect.x - int(GUNPOINT_RADIUS * cos(self.shooting_angle))
            
        gunpoint_y = self.rect.y - int(GUNPOINT_RADIUS * sin(self.shooting_angle))

        return gunpoint_x, gunpoint_y

    def shoot(self): 
        """Creates a bullet object"""
        x, y = self.get_gunpoint_coordinates()
        # If worm is facing left we shoot a bullet from a point more on the left
        bullet = Bullet(x if self.direction=="right" else x-8, y, 
                        direction=self.direction, 
                        v=self.shooting_power, 
                        alpha=self.shooting_angle,
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
                self.change_x = self.change_x + WORM_SPEED if self.change_x < WORM_SPEED else WORM_SPEED

            elif event.key == pygame.K_RIGHT:
                self.change_x = self.change_x - WORM_SPEED if self.change_x > -WORM_SPEED else -WORM_SPEED

            # Aiming
            elif event.key == pygame.K_UP:
                self.change_angle = self.change_angle - SHOOTING_ANGLE_CHANGE

            elif event.key == pygame.K_DOWN:
                self.change_angle = self.change_angle + SHOOTING_ANGLE_CHANGE

            # Shooting
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.shooting = False
                self.shoot() 

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

    def move(self, event):
        """Moves current worm"""
        self.current_worm.move(event)
        
    def change_worm(self):
        """Changes worm to next one"""
        # First, stop moving current worm (problematic if called after player killed his own worm)
        #print("change worm")
        #print(self.current_worm_id, self.worms_number, len(self.worms))
        self.current_worm.change_x = 0
        new_worm_id = self.current_worm_id + 1
        self.current_worm_id = new_worm_id if new_worm_id < self.worms_number else 0

    def remove_worms(self, killed_worms):
        """Removes killed worms from player's list"""
        if killed_worms:
            self.worms = [worm for worm in self.worms if all(worm != w for w in killed_worms)]
            for worm in self.worms:
                worm.change_x = 0
            if len(self.worms) < self.worms_number:
                self.worms_number = len(self.worms)

                # Quiting game if player has no worms left
                if self.worms_number == 0:
                    print("{} lost".format(self.name))
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


class TextObject:
    """Simple class to represent a text object displaying in Menu"""
    def __init__(self, text: str, x: int, y: int, font_size:int=25, 
                bold:bool=False, 
                font=None):
        self.text = text
        self.x = x
        self.y = y
        # We don't want to open this SysFont to many times
        self.font = font or pygame.font.SysFont('Calibri', font_size, bold, False)
        #font = pygame.font.SysFont('Calibri', 25, True, False)
        self.image = self.font.render(text, True, GREEN)


class Menu:
    """Class responsible for the look of the Menu on the right"""
    def __init__(self, x=SCREEN_WIDTH + 20, y=20):
        self.x = x
        self.y = y
        self.texts = [TextObject("Menu", x, y, 25, bold=True)]
        self.language = EN 
        self.sound = ON
        self.time = 10

        self.font = pygame.font.SysFont('Calibri', 25, False, False)

        # TODO: Get rid of code repetition?
        # Creating language options
        y_lang = y + 1*20
        lang = TextObject("Language:", x, y_lang)
        lang_rect = lang.image.get_rect()
        lang_option = TextObject(self.language, x + lang_rect.width + 20, y_lang)
        self.add_text_objects(lang, lang_option)
        
        # Creating sound options
        y_sound = y + 2*20
        snd = TextObject("Sound:", x, y_sound)
        snd_rect = snd.image.get_rect()
        snd_option = TextObject(self.sound, x + snd_rect.width + 20, y_sound)
        self.add_text_objects(snd, snd_option)

    def add_raw_texts(self, *texts):
        for text in texts:
            self.texts.append(TextObject(text, self.x, self.y + 30*len(self.texts)))

    def add_text_objects(self, *text_objects):
        for text in text_objects:
            self.texts.append(text)

    def add_time(self, *text_objects):
        self.time_pics = list(text_objects)

    def draw(self, screen):
        for text_object in (self.texts + self.time_pics):
            screen.blit(text_object.image, (text_object.x, text_object.y))


def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH + MENU_WIDTH, SCREEN_HEIGHT]) 
    pygame.display.set_caption("Worms") 
    clock = pygame.time.Clock()

    # Sounds
    pygame.mixer.init()

    # Creating sprite_sheet object (image containing all needed images)
    sprite_sheet_path1 = "M_09.png"
    sprite_sheet1 = SpriteSheet(sprite_sheet_path1)

    sprite_sheet_path2 = "F_01.png"
    sprite_sheet2 = SpriteSheet(sprite_sheet_path2)

    # Creating worms
    worm = Worm(150, SCREEN_HEIGHT - 150, sprite_sheet1, name="artur")
    worm2 = Worm(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, sprite_sheet2, name="dent")
    worm3 = Worm(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 150, sprite_sheet2, name="ford")
    worm4 = Worm(SCREEN_WIDTH - 400, SCREEN_HEIGHT - 150, sprite_sheet1, name="prefect")
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

    ## Creating gunpoint object:
    gunpoint = GunPoint(player1.current_worm.rect.x+16+10, player1.current_worm.rect.y-10)

    # Creating walls
    wall_list = pygame.sprite.Group()
    floor = Wall(0, SCREEN_HEIGHT-10, SCREEN_WIDTH, 10)
    right_block = Wall(SCREEN_WIDTH-10, 0, 10, SCREEN_HEIGHT)
    random.seed(41)
    block1 = Wall(40, 150, 50, 60)
    block2 = Wall(200, 50, 50, 30)
    block3 = Wall(400, 300, 50, 30)
    blocks = [Wall(random.randint(0, SCREEN_WIDTH), 
                random.randint(0, SCREEN_HEIGHT),
                50, 
                10) 
            for _ in range(10)]
    wall_list.add(floor, right_block, block1, block2, block3, *blocks)

    #print(id(player1.worms[0]) == id(worm))

    # Creating Menu
    menu = Menu()

    # Creating font for displaying time
    font_bold = pygame.font.SysFont('Calibri', 25, True, False)
    font_not_bold = pygame.font.SysFont('Calibri', 25, True, False)

    frame_count = 0
    mode = PLAYER_1
    while True:
        # Filling screen with black 
        screen.fill(BLACK)

        # Calculating how much time is left
        print(frame_count)
        total_seconds = frame_count // FRAME_RATE
        print(total_seconds)
        menu.time = total_seconds
        x, y = SCREEN_WIDTH + 20, 20
        y_time = y + 3*20
        tim = TextObject("Time:", x, y_time, font=font_bold)
        tim_rect = tim.image.get_rect()
        tim_display = TextObject(str(total_seconds), x + tim_rect.width + 20, y_time, font=font_not_bold)
        menu.add_time(tim, tim_display)

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
        current_worm = player1.current_worm if mode==PLAYER_1 else player2.current_worm
        worm_list.update(wall_list, gunpoint, current_worm)

        # Drawing 
        pygame.draw.circle(screen, gunpoint.color, (gunpoint.x, gunpoint.y), gunpoint.radius)
        worm_list.draw(screen)
        bullet_list.draw(screen)
        wall_list.draw(screen)
        menu.draw(screen)

        frame_count += 1

        clock.tick(FRAME_RATE)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()




    

    
