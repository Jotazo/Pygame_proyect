import pygame as pg

import os, sys

from the_quest.game_screen.config import *

from folders import *
from tools import *

class PauseScreen:
    
    def __init__(self):

        self.option = 0
        self.paused = True
        self.reset = False

    def on_pause(self, screen):
        self.reset = False
        pg.mixer.pause()
        while self.paused:
            self._handle_events()
            self._draw_paused_menu(self.option, screen)
        self.paused = True
        self.option = 0
        return self.reset

    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                self._keydown_events(event)

    def _keydown_events(self, event):
        if event.key == pg.K_ESCAPE:
            self.paused = False
        if event.key == pg.K_DOWN:
            if self.option < 2:
                self.option += 1
        if event.key == pg.K_UP:
            if self.option > 0:
                self.option -= 1
        if event.key == pg.K_RETURN:
            self._check_op(self.option)

    def _check_op(self, option):
        if option == 0:
            self.paused = False
            pg.mixer.unpause()
        if option == 1:
            self.paused = False
            self.reset = True
        if option == 2:
            pg.quit()
            sys.exit()

    def _draw_paused_menu(self, option, screen):

        load_and_draw_image(screen, IMAGES_FOLDER, 'pause1.png', x=200, y=170)

        if option == 0:
            draw_text2(screen, SPACE, 24, 'Continue', RED, position='center', width=WIDTH, height=HEIGHT)
            draw_text2(screen, SPACE, 24, 'Restart', WHITE, position="closecenterbottom", width=WIDTH, height=HEIGHT)
            draw_text2(screen, SPACE, 24, 'Quit', WHITE, position="closecenterbottom2", width=WIDTH, height=HEIGHT)
        elif option == 1:
            draw_text2(screen, SPACE, 24, 'Continue', WHITE, position='center', width=WIDTH, height=HEIGHT)
            draw_text2(screen, SPACE, 24, 'Restart', RED, position="closecenterbottom", width=WIDTH, height=HEIGHT)
            draw_text2(screen, SPACE, 24, 'Quit', WHITE, position="closecenterbottom2", width=WIDTH, height=HEIGHT)
        else:
            draw_text2(screen, SPACE, 24, 'Continue', WHITE, position='center', width=WIDTH, height=HEIGHT)
            draw_text2(screen, SPACE, 24, 'Restart', WHITE, position="closecenterbottom", width=WIDTH, height=HEIGHT)
            draw_text2(screen, SPACE, 24, 'Quit', RED, position="closecenterbottom2", width=WIDTH, height=HEIGHT)

        draw_text2(screen, SPACE2, 48, 'PAUSE', WHITE, position='closecenterup', width=WIDTH, height=HEIGHT)
        pg.display.flip()

class BlackScreen:
    pass