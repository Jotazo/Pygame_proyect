import pygame as pg
import sys, os

from folders import *
from tools import *


from the_quest.game_screen.sprites import *
from the_quest.game_screen.config import *

class Screen:

    pg.init()

    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("The Quest")

        self.background, self.rect = load_image(IMAGES_FOLDER, 'background.xcf')

        self.background_x = 0
        self.meteors_timer = 0

        self.meteors = pg.sprite.Group()
        self.ship = Ship()
        self.starting_screen = Starting_Screen(self.screen, self.ship)

        self.score = 0
        self.meteors_dodged = 0

        self.clock = pg.time.Clock() 

    def new_game(self):
        # Start a new game
        self.starting_screen.initial_screen()
        self.run()

    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS)
            self._add_meteors(dt)
            self._handle_events()
            self._update_screen()
            self._update_sprites()
            self._collition()
            self._remove_meteors()
            print(self.ship.rect.y)

    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def _update_screen(self):
        # Drawing background movement
        x_rel = self.background_x % self.rect.width
        self.screen.blit(self.background, (x_rel - self.rect.width ,0))
        if x_rel < WIDTH:
            self.screen.blit(self.background, (x_rel,0))
        self.background_x -= 1

        # Drawing top level menu
        self._top_level_menu()

        # Drawing Ship
        self.screen.blit(self.ship.image, (self.ship.rect.x, self.ship.rect.y))

        # Drawing meteors
        self.meteors.draw(self.screen)

        pg.display.flip()

    def _update_sprites(self):
        self.ship.update()
        self.meteors.update()

    def _add_meteors(self, dt):
        self.meteors_timer += dt
        if self.meteors_timer >= 85:
            if len(self.meteors) <= MAX_METEORS:
                self.meteors.add(Meteor())
            self.meteors_timer = 0

    def _remove_meteors(self):
        for meteor in self.meteors:
            if meteor.rect.right <= 0:
                self.meteors.remove(meteor)
                self.score += meteor.points
                self.meteors_dodged += 1

    def _collition(self):
        if self.ship.state != STATES['EXPLODING']:
            if pg.sprite.spritecollide(self.ship, self.meteors, True):
                self.ship.state = STATES['EXPLODING']

    def _top_level_menu(self):
        top_level_img, top_level_img_rect = load_image(IMAGES_FOLDER, 'score1.png')
        lifes_font, lifes_text = draw_text(SPACE, 16, f'Lifes - {self.ship.lifes}', WHITE)
        score_font, score_text = draw_text(SPACE, 16, f'Score - {self.score}', WHITE)
        meteors_dodged_font, meteors_dodged_text = draw_text(SPACE, 16, f'Meteors Dodged - {self.meteors_dodged}', WHITE)

        self.screen.blit(top_level_img, (0, 0))
        self.screen.blit(lifes_text, (50,15))
        self.screen.blit(meteors_dodged_text, (240, 15))
        self.screen.blit(score_text, (590, 15))

    def _black_screen(self):
        pass

class Starting_Screen:

    def __init__(self, screen, ship):

        self.screen = screen
        self.ship = ship
        self.bg , self.bg_rect = load_image(IMAGES_FOLDER, 'background.xcf')

        self.top_level_img, self.top_level_img_rect = load_image(IMAGES_FOLDER, 'score1.png', y=-50)
        self.lifes_font, self.lifes_text = draw_text(SPACE, 16, 'Lifes - 3', WHITE)
        self.score_font, self.score_text = draw_text(SPACE, 16, 'Score - 0', WHITE)
        self.meteors_dodged_font, self.meteors_dodged_text = draw_text(SPACE, 16, 'Meteors Dodged - 0', WHITE)
        self.ready_font, self.ready_txt = draw_text(SPACE2, 54, 'READY?', WHITE)
        self.start_font, self.start_txt = draw_text(SPACE, 16, 'Press < SPACE > to start', WHITE)

        self.starting = True

        self.ticks = 0
        self.ix_pos = -50

    def initial_screen(self):
        while self.starting:
            dt = pg.time.Clock().tick(FPS)
            self._handle_events()
            self._update(dt)
            self._update_ix_pos(dt)
                
    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and self.ix_pos == 0:
                    self.starting = False

    def _update(self, dt):
        self.screen.blit(self.bg, (0,0))

        self.screen.blit(self.top_level_img, (0, self.ix_pos))
        self.screen.blit(self.lifes_text, (50, self.ix_pos+15))
        self.screen.blit(self.meteors_dodged_text, (240, self.ix_pos+15))
        self.screen.blit(self.score_text, (590, self.ix_pos+15))
        
        self.screen.blit(self.ship.image, (self.ix_pos, self.ship.rect.y))
        if self.ix_pos == 0:
            self._show_ready_msg(dt)

        pg.display.flip()

    def _show_ready_msg(self, dt):
        self.screen.blit(self.ready_txt, ((WIDTH/2)-(self.ready_txt.get_size()[0]//2), (HEIGHT/2)/2))

        if self.ticks <= 1000:
            self.screen.blit(self.start_txt, ((WIDTH/2)-(self.start_txt.get_size()[0]//2), (HEIGHT/2)-(self.start_txt.get_size()[1]//2)))
        elif self.ticks <= 1500:
            pass
        else:
            self.ticks = 0

        self.ticks += dt

    def _update_ix_pos(self, dt):
        if self.ix_pos == 0:
            return

        self.ticks += dt
        if self.ticks >= 85:
            self.ix_pos += 1
            self.ticks = 0