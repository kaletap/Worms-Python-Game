# Welcome to Worms!

## Requirements
This script was tested on Python 3.6.4 with pygame version 1.9.4. It doesn't work with Python 2.

## Running instructions
I assume that you already have Python installed (preferably version >= 3.6).
To install pygame run `pip install pygame`.  To play a game run `python worm.py`.

There are a few options available when starting a game. You can choose number of worms each player has, time for each round and names of players. For example:

`python worms.py --time 15 --worms_number 5 --player1 Player1_name --player2 Player2_name`

This will run a game with 15 seconds per each player, 5 worms per each player, player1 and player2 will be called Player1_name and Player2_name respectively. Additionaly, you can use `--no_menu` option to hide menu on the right.


## Playing instructions
### Overview
Even though this game is called Worms, I use people characters in it, but still refer to them as "worms". Games starts with worms in randomly generated places. Each player has some amount of time per round. Players choose which worm to use, control them, move them right and left, jump, aim and shoot trying to kill opponent's worms. They have limited time to do it, so you have to be fast. Also, be careful not to shoot your own worm!

### Controlling
* **left arrow** : moving left
* **right arrow** : moving right
* **space** : jumping
* **up arrow** : moving gun up
* **down arrow** : moving gun down
* **enter** : shooting
* **tab** : changing worms

It's worth to remember, that the longer you press enter, the faster the bullet moves.

## Credits
In my game I used characters made by Fleurman: https://opengameart.org/content/tiny-characters-set

Sounds were made by Independent.nu:
https://opengameart.org/content/37-hitspunches,
https://opengameart.org/content/16-button-clicks

All above were shared under Public Domain License.
