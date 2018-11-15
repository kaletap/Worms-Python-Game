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


def collided(worm: Worm, bullet: Bullet, sound_option=ON) -> bool: 
    """ Check whether worm and bullet collide.
    Returns False when bullet was shooted by worm 
    (we doesn't let worm shoot himself)"""
    if worm.name == bullet.shooted_by:
        return False
    else:
        coll = pygame.sprite.collide_rect(worm, bullet)
        # Make a sound if collided
        if coll and sound_option == ON:
            sound_path = os.path.join('sounds/hits', random.choice(defaults.hit_sound_paths))
            hit_sound = pygame.mixer.Sound(sound_path)
            hit_sound.play()
        return coll


class TextObject(pygame.sprite.Sprite):
    """Simple class to represent a text object displaying in Menu"""
    def __init__(self, text, x, y, font=None, font_size=25, bold=False):
        super().__init__()

        self.text = text
        self.x = x
        self.y = y

        # We don't want to open this SysFont too many times
        # it's better to pass it as an argument than create each time
        self.font = font or pygame.font.SysFont('Calibri', font_size, bold, False)

        self.image = self.font.render(text, True, GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_text(self, new_text):
        """Changes text in displayed image"""
        self.image = self.font.render(new_text, True, GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Menu:
    """Class responsible for the look of the Menu on the right"""
    def __init__(self, x=SCREEN_WIDTH + 20, y=20):
        # x and y are starting points of menu
        self.x = x
        self.y = y

        # Options
        self.language = EN 
        self.sound = ON
        self.time = 10

        self.font = pygame.font.SysFont('Calibri', 25, False, False)
        self.font_bold = pygame.font.SysFont('Calibri', 25, True, False)

        self.positions = {
            "menu": (x, y+10),

            "language" : (x, y + 50),
            "language_option" : (x + 100, y + 50),

            "sound" : (x, y + 100),
            "sound_option" : (x + 100, y + 100),

            "time" : (x, SCREEN_HEIGHT - 50),
            "time_display" : (x + 100, SCREEN_HEIGHT - 50)
        }

        self.text_objects = {
            "menu": TextObject("MENU", *self.positions["menu"]),

            "language" : TextObject("Language:", *self.positions["language"], self.font),
            "language_option" : TextObject(self.language, *self.positions["language_option"], self.font),

            "sound" : TextObject("Sound:", *self.positions["sound"], self.font),
            "sound_option" : TextObject(self.sound, *self.positions["sound_option"], self.font),

            "time" : TextObject("TIME:", *self.positions["time"], font=self.font_bold),
            "time_display": TextObject(str(0), *self.positions["time_display"], self.font)
        }

    def update_options(self, x, y):
        if self.text_objects["language_option"].rect.collidepoint(x, y):
            #print("Changing language option")
            new_language_option = EN if self.language == PL else PL
            self.language = new_language_option
            self.text_objects["language_option"] = TextObject(new_language_option, 
                                                              *self.positions["language_option"], 
                                                              self.font)
            if self.language == PL:
                self.text_objects["time"].change_text("CZAS:")
                self.text_objects["language"].change_text("Jezyk:")
                self.text_objects["sound"].change_text("Dzwiek:")

            elif self.language == EN:
                self.text_objects["time"].change_text("TIME:")
                self.text_objects["language"].change_text("Language:")
                self.text_objects["sound"].change_text("Sound:")

        elif self.text_objects["sound_option"].rect.collidepoint(x, y):
            #print("Changing sound option")
            new_sound_option = OFF if self.sound == ON else ON
            self.sound = new_sound_option
            self.text_objects["sound_option"] = TextObject(new_sound_option, 
                                                          *self.positions["sound_option"],
                                                          self.font)

    def update_time(self, seconds, font=None):
        self.time = seconds
        self.text_objects["time_display"] = TextObject(str(seconds), 
                                                        *self.positions["time_display"], 
                                                        font=self.font)
        
    
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

    start = time.time()
    mode = PLAYER_1
    while True:
        # Filling screen with black 
        screen.fill(BLACK)

        # Calculating how much time is left
        total_seconds = int(time.time() - start)
        menu.update_time(total_seconds)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Backspace to change players 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                print("Changing players")
                mode = PLAYER_2 if mode == PLAYER_1 else PLAYER_1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                menu.update_options(x, y)

            if mode == PLAYER_1:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    player1.change_worm()
                player1.move(event)

            elif mode == PLAYER_2:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    player2.change_worm()
                player2.move(event)

        # Killling worms hitted by bullet
        killed_worms = pygame.sprite.groupcollide(worm_list, 
                                                  bullet_list, 
                                                  dokilla=True, 
                                                  dokillb=True, 
                                                  collided=lambda x, y: collided(x, y, menu.sound))
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

        # Drawing menu and time
        pygame.sprite.Group(menu.text_objects.values()).draw(screen)

        clock.tick(FRAME_RATE)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()




    

    
