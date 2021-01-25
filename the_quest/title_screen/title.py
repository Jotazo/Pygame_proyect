import pygame as pg

import os, sys

from config import *
from folders import *
from tools import *


class TitleScreen:

    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(GAME_TITLE)

        self.ship_img = load_image(SHIP_FOLDER, 'ship.xcf', rect=False)

        self.starting = True

        self.x_pos_ship = 800
        self.y_pos_ship = 110

        self.x_pos_title = 848
        self.y_pos_title = 75

        self.option = 0

        self.title_sound = load_sound(SOUNDS_FOLDER, 'title-screen.wav')

        self.clock = pg.time.Clock()

    def title_screen(self):
        self._intial_animation()
        self.title_sound.set_volume(0.2)
        self.title_sound.play()
        while self.starting:
            dt = self.clock.tick(FPS)
            self._handle_events()
            self._draw_title()
            self._draw_options()
            pg.display.flip()
        self.starting = True

    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                self._keydown_events(event)

    def _keydown_events(self, event):
        if event.key == pg.K_DOWN:
            if self.option < 2:
                self.option += 1
        if event.key == pg.K_UP:
            if self.option > 0:
                self.option -= 1
        if event.key == pg.K_RETURN:
            self._check_op(self.option)
        if event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

    def _check_op(self, option):
        if option == 0:
            # Start New Game
            self.starting = False
            self.title_sound.stop()
        elif option == 1:
            # Settings screen
            pass
        else:
            # Exit Game
            pg.quit()
            sys.exit()

    def _intial_animation(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)

            self.screen.fill(BLACK)

            load_and_draw_image(self.screen, SHIP_FOLDER, 'ship-title.png', x=self.x_pos_ship, y=self.y_pos_ship)
            create_draw_text(self.screen, TITLE, 120, 'THE QUEST', WHITE, pos_x=self.x_pos_title, pos_y=self.y_pos_title)
            self.x_pos_ship -= 5
            if self.x_pos_title >= 66.0:
                self.x_pos_title -= 5
            else:
                # title sound
                pass
            if self.x_pos_ship <= -55:
                running = False
            
            pg.display.flip()
            

    def _draw_title(self):
        create_draw_text(self.screen, TITLE, 120, 'THE QUEST', WHITE, position='topcenter', width=WIDTH, height=HEIGHT)

    def _draw_options(self):
        if self.option == 0:
            create_draw_text(self.screen, SPACE, 24, 'New Game', RED, position='center', width=WIDTH, height=HEIGHT)
            create_draw_text(self.screen, SPACE, 24, 'Settings', WHITE, position='closecenterbottom', width=WIDTH, height=HEIGHT)
            create_draw_text(self.screen, SPACE, 24, 'Exit', WHITE, position='closecenterbottom2', width=WIDTH, height=HEIGHT)
        elif self.option == 1:
            create_draw_text(self.screen, SPACE, 24, 'New Game', WHITE, position='center', width=WIDTH, height=HEIGHT)
            create_draw_text(self.screen, SPACE, 24, 'Settings', RED, position='closecenterbottom', width=WIDTH, height=HEIGHT)
            create_draw_text(self.screen, SPACE, 24, 'Exit', WHITE, position='closecenterbottom2', width=WIDTH, height=HEIGHT)
        else:
            create_draw_text(self.screen, SPACE, 24, 'New Game', WHITE, position='center', width=WIDTH, height=HEIGHT)
            create_draw_text(self.screen, SPACE, 24, 'Settings', WHITE, position='closecenterbottom', width=WIDTH, height=HEIGHT)
            create_draw_text(self.screen, SPACE, 24, 'Exit', RED, position='closecenterbottom2', width=WIDTH, height=HEIGHT)