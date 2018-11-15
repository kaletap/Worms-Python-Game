#!/opt/anaconda/bin//python
import pygame, sys, random, os, time, argparse
from math import cos, sin, pi as PI

import defaults
from game_classes import *
from menu_classes import *
from utils import *
from defaults import *
        
    
def main(args):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    if args.no_menu:
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    else:
        screen = pygame.display.set_mode([SCREEN_WIDTH + MENU_WIDTH, SCREEN_HEIGHT]) 
    pygame.display.set_caption("Worms") 
    clock = pygame.time.Clock()

    # Creating sprite_sheet object (image containing all needed images)
    sprite_sheet_path1 =  os.path.join("graphics/Males", random.choice(player1_image_paths))
    sprite_sheet1 = SpriteSheet(sprite_sheet_path1)

    sprite_sheet_path2 = os.path.join("graphics/Females", random.choice(player2_image_paths))
    sprite_sheet2 = SpriteSheet(sprite_sheet_path2)

    # Creating worms
    worms_player1 = [Worm(random.randrange(20, SCREEN_WIDTH-20),
                   random.randrange(0, SCREEN_HEIGHT-10),
                   sprite_sheet1) for _ in range(args.worms_number)]
    worms_player2 = [Worm(random.randrange(20, SCREEN_WIDTH-20),
                   random.randrange(0, SCREEN_HEIGHT-10),
                   sprite_sheet2) for _ in range(args.worms_number)]
    # Group containing all worms
    worm_list = pygame.sprite.Group()
    worm_list.add(*worms_player1, *worms_player2)

    # Creating players
    player1 = Player(*worms_player1, name=args.player1)
    player2 = Player(*worms_player2, name=args.player2)

    ## Creating gunpoint object:
    gunpoint = GunPoint(player1.current_worm.rect.x+16+10, player1.current_worm.rect.y-10)

    # Creating walls
    wall_list = pygame.sprite.Group()
    floor = Wall(0, SCREEN_HEIGHT-10, SCREEN_WIDTH, 10)
    right_block = Wall(SCREEN_WIDTH-10, 0, 10, SCREEN_HEIGHT)
    left_block = Wall(0, 0, 10, SCREEN_HEIGHT)
    random.seed(41)
    block1 = Wall(40, 150, 50, 60)
    block2 = Wall(100, 50, 350, 30)
    block3 = Wall(90, 350, 150, 10)
    block4 = Wall(550, 100, 50, 30)
    blocks = [Wall(10*i, 10*i + 40, 20, 10) for i in range(0, SCREEN_HEIGHT // 10, 3)]
    other_blocks = [Wall(SCREEN_WIDTH // 2 + 10*i + 80, 
                         SCREEN_HEIGHT - 30 * i - 140, 20, 10) 
                    for i in range(0, 10, 1)]

    wall_list.add(floor, right_block, left_block, block1, block2, block3, block4, *blocks, *other_blocks)

    # Creating bullet list
    bullet_list = pygame.sprite.Group()

    # Creating Menu
    menu = Menu()

    print("Welcome to worms")

    # Playing game
    done, player1_lost, player2_lost = False, False, False
    start = time.time()
    mode = PLAYER_1
    while not done:
        # Filling screen with black 
        screen.fill(BLACK)

        # Calculating how much time is left
        time_left = args.time - int(time.time() - start)
        menu.update_time(time_left)

        # Changing players if time is up
        if time_left < 0:
            mode = PLAYER_2 if mode == PLAYER_1 else PLAYER_1
            player1.stop_worm()
            player2.stop_worm()
            changing_players_text = TextObject("Changing players", 50, 50, font=None, font_size=50)
            pygame.sprite.Group(changing_players_text).draw(screen)
            pygame.time.delay(1000)
            start = time.time()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Backspace to change players (useful for debugging)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                mode = PLAYER_2 if mode == PLAYER_1 else PLAYER_1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                menu.update_options(x, y)

            if mode == PLAYER_1:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    player1.stop_worm()
                    player1.change_worm()
                player1.move(event, bullet_list)

            elif mode == PLAYER_2:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    player2.stop_worm()
                    player2.change_worm()
                player2.move(event, bullet_list)

        # Killling worms hitted by bullet
        killed_worms = pygame.sprite.groupcollide(worm_list, 
                                                  bullet_list, 
                                                  dokilla=True, 
                                                  dokillb=True, 
                                                  collided = lambda x, y: collided(x, y, menu.sound))
        player1_lost = player1.remove_worms(killed_worms.keys()) 
        player2_lost = player2.remove_worms(killed_worms.keys())
        done = player1_lost or player2_lost

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

    # Displaying game over and who won
    screen.fill(BLACK)
    font = pygame.font.SysFont('Calibri', 50, True, False)
    game_over = font.render("GAME OVER", True, RED)
    who_won_text = args.player1 if player2_lost else args.player1
    who_won_text = "{} won!".format(who_won_text)
    who_won = font.render(who_won_text, False, RED)
    screen.blit(game_over, (50, 50))
    screen.blit(who_won, (50, 200))
    pygame.display.flip()
    pygame.time.delay(3000)

    pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--worms_number", type=int, default=3, help="Number of worms each player has")
    parser.add_argument("-t", "--time", type=int, default=10, help="Time per each player")
    parser.add_argument("--no_menu", action="store_true", help="Don't display menu")
    parser.add_argument("--player1", type=str, default="Player1", help="Name of first player")
    parser.add_argument("--player2", type=str, default="Player2", help="Name of second player")
    args = parser.parse_args()

    main(args)




    

    
