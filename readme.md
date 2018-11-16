# Welcome to Worms!

## Requirements
This script was tested on Python 3.6.4 with pygame version 1.9.4. It doesn't work with Python 2.

## Running instructions
I assume that you already have Python installed (preferably version >= 3.6).
To install pygame run `pip install pygame`.  To play a game run `python worm.py`.

There are a few options available when starting a game. You can choose number of worms each player has, time for each round and names of players. For example:

`python worms.py --time 15 --worms_number 5 --player1 Alice --player2 Bob`

This will run a game with 15 seconds per each player, 5 worms per each player, player1 and player2 will be called Alice and Bob respectively. Additionaly, you can use `--no_menu` option to hide menu on the right.


## Playing instructions
### Overview
Even though this game is called Worms, I use people characters in it, but still refer to them as "worms". Game starts with worms in randomly generated places. Each player has some amount of time per round. Players choose which worm to use, control them, move them right and left, jump, aim and shoot trying to kill opponent's worms. They have limited time to do it, so you have to be fast. Also, be careful not to shoot your own worm!

### Controlling
* **left arrow** : moving left
* **right arrow** : moving right
* **space** : jumping
* **up arrow** : moving gun up
* **down arrow** : moving gun down
* **enter** : shooting
* **tab** : changing worms

It's worth to remember, that the longer you press enter, the faster the bullet moves. 

You can change sound / no sound options and language in the menu by clicking on text.

## Technical details
Game may run slower or faster on different peoples computers. If you think that it runs too fast or too slow you may want to change FRAME_RATE located in `defaults.py`. Also, you may want to play around with GRAV and GRAV_WORM which are responsible for gravitation working on bullet and worms respectively. Running worms.py with --no_menu option also makes game faster (I don't know why).

This project implements some features that original Worms 2D have. It's possible to make it better by adding better graphics and some cool features (like different weapons and tools, implementing wind etc.) and by improving existing features a little bit. One thing that it's lacking though, and I don't know what to do about it, is having diversified and interactive environment consisting of something more than just rectangles. It is something I will think about in the future.

## Credits
In my game I used characters made by Fleurman: https://opengameart.org/content/tiny-characters-set

Ball image was created by BananaOwl (https://opengameart.org/content/rainbow-ball) and shared under Creative Common License (https://creativecommons.org/licenses/by/3.0/).

Sounds were made by Independent.nu:
https://opengameart.org/content/37-hitspunches,
https://opengameart.org/content/16-button-clicks

Music made by cynicmusic: https://opengameart.org/content/battle-theme-a


