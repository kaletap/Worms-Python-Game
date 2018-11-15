import pygame, os, random

from defaults import ON, hit_sound_paths
from game_classes import Worm, Bullet


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
            sound_path = os.path.join('sounds/hits', random.choice(hit_sound_paths))
            hit_sound = pygame.mixer.Sound(sound_path)
            hit_sound.play()
        return coll