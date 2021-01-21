import pygame as pg
from pygame.locals import *

import random

import os

from folders import *
from tools import *

from the_quest.game_screen.config import *


class Ship(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image(SHIP_FOLDER, 'ship_1_48x48.xcf', y=276)

        self.selected_expl_img = 0
        self.speed_explosion = 0

        self.lifes = 3

        self.state = STATES['ALIVE']

        self.vy = 0

    def update(self):
        
        self.rect.y += self.vy
        
        if self.state == STATES['EXPLODING']:
            self.image = self._explosion()

        if self.rect.top <= 50:
            self.rect.top = 50

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        self._moving_ship()

    def _moving_ship(self):

        key_pressed = pg.key.get_pressed()

        if key_pressed[K_UP]:
            self.vy = -SPEED
        elif key_pressed[K_DOWN]:
            self.vy = SPEED
        else:
            self.vy = 0

    def _explosion(self):

        if self.selected_expl_img >= 8:
            img = load_image(SHIP_FOLDER, 'ship_1_48x48.xcf', rect=False)
            self.selected_expl_img = 0
            self.lifes -= 1
            self.state = STATES['ALIVE']
        else:
            img = load_image(EXPLOSION_FOLDER, f'explosion_{self.selected_expl_img}.xcf', rect=False)
            if self.speed_explosion % 4 == 0:
                self.selected_expl_img += 1

        self.speed_explosion += 1
        return img

class Meteor(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.random_meteor = random.randrange(1,6)

        self.image, self.rect = load_image(
                        METEORS_FOLDER, 
                        f'meteor{self.random_meteor}.png', 
                        x=WIDTH, y=random.randrange(50, HEIGHT-METEORS_DATA[f'meteor{self.random_meteor}']['height'])
                        ) 

        self.points = METEORS_DATA[f'meteor{self.random_meteor}']['points']

        self.vx = random.randint(4, 12)

    def update(self):
        self.rect.x -= self.vx
