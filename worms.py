import pygame, sys, random, os, time, string
from math import cos, sin, pi as PI

import defaults
from game_classes import *
from menu_classes import *
from utils import *
from defaults import *
        
    
def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH + MENU_WIDTH, SCREEN_HEIGHT]) 
    pygame.display.set_caption("Worms") 
    clock = pygame.time.Clock()

    # Sounds
    pygame.mixer.init()

    # Creating sprite_sheet object (image containing all needed images)
    sprite_sheet_path1 =  os.path.join("graphics/Males", "M_09.png")
    sprite_sheet1 = SpriteSheet(sprite_sheet_path1)

    sprite_sheet_path2 = os.path.join("graphics/Females", "F_01.png")
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
                player1.move(event, bullet_list)

            elif mode == PLAYER_2:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    player2.change_worm()
                player2.move(event, bullet_list)

        # Killling worms hitted by bullet
        killed_worms = pygame.sprite.groupcollide(worm_list, 
                                                  bullet_list, 
                                                  dokilla=True, 
                                                  dokillb=True, 
                                                  collided = lambda x, y: collided(x, y, menu.sound))
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




    

    
