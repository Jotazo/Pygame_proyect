import pygame as pg
import sys, os

from folders import *
from tools import *

from the_quest.game_screen.sprites import *
from the_quest.game_screen.config import *

class Screen:

    pg.init()
    pg.mixer.init()

    def __init__(self):
        # Screen Configuration
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.rect = self.screen.get_rect()
        pg.display.set_caption("The Quest")

        # Background img
        self.background = load_image(IMAGES_FOLDER, 'background.xcf', rect=False)
        self.background_x = 0 # For moving_background

        self.meteors_timer = 0 # For adding meteors

        # Instances
        self.meteors = pg.sprite.Group()
        self.ship = Ship()
        self.clock = pg.time.Clock() 
        self.starting_screen = Starting_Screen(self.screen, self.ship)

        # Planet image and rect
        self.planet, self.rect_planet = load_image(IMAGES_FOLDER, 'jupiter.png', x=WIDTH, y=50)
        self.planet_x = 0 # For moving planet
        self.planet_timer = 0 # For speed draw planet

        # Vars top level
        self.score = 0
        self.meteors_dodged = 30

        self.ticks = 0
        
    def new_game(self):
        # Start a new game
        # self.starting_screen.initial_screen()
        self.run()

    def run(self):
        '''
        Main loop main game
        '''

        while self.ship.state != STATES['DEAD']:
            dt = self.clock.tick(FPS)
            if self.ship.lifes == 3:
                pass
                # self._initial_screen(dt)
            if self.ship.state == STATES['NOT ALIVE']:
                self._black_screen(self.ship.lifes, self.ticks)
                self._reset()
            self._add_meteors(dt)
            self._handle_events()
            self._update_screen(dt)
            self._update_sprites()
            self._collition()
            self._remove_meteors()

    def _handle_events(self):
        '''
        Handling events
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and self.ship.state == STATES['ALIVE']\
                                and self.meteors_dodged >= METEORS_TO_DODGE and self.planet_x == 272:
                    self.ship.state = STATES['ROTATING']

                if event.key == pg.K_SPACE and self.ship.state == STATES['PREPARED TO LAND']:
                    self.ship.state = STATES['LANDING']

    def _update_screen(self, dt):
        '''
        Update screen
        '''
        # Drawing background movement
        self._move_background()

        # Drawing top level menu
        self._top_level_menu()

        # Drawing Planet
        self.planet_timer += dt
        if self.meteors_dodged >= METEORS_TO_DODGE:
            if self.ship.state != STATES['LANDED'] and self.ship.state != STATES['HIDDEN']:
                self.screen.blit(self.planet, (self.rect_planet.x-self.planet_x, self.rect_planet.y))
                if self.planet_x <= 270 and self.planet_timer >= 85:
                    self.planet_x += 2
            else:
                if self.planet_x >= 0:
                    self.planet_x -= 2
                self.screen.blit(self.planet, (self.rect_planet.x-self.planet_x, self.rect_planet.y))
            

        # Drawing Ship
        self.screen.blit(self.ship.image, (self.ship.rect.x, self.ship.rect.y))

        # Drawing meteors
        self.meteors.draw(self.screen)

        # Drawing end level messages
        self._end_level_msg()

        pg.display.flip()

    def _update_sprites(self):
        '''
        Sprites update
        '''
        self.ship.update()
        self.meteors.update()

    def _add_meteors(self, dt):
        '''
        Adding meteors, when we reach the maximum meteors dodged we stop
        to add meteors, else, we continue adding meteors
        '''
        if self.meteors_dodged < METEORS_TO_DODGE:
            self.meteors_timer += dt
            if self.meteors_timer >= 85:
                if len(self.meteors) <= MAX_METEORS:
                    self.meteors.add(Meteor())
                self.meteors_timer = 0

    def _remove_meteors(self):
        '''
        Removing meteors.
        If we reach the maximum meteors dodged we stop to add meteors dodged and score
        '''
        for meteor in self.meteors:
            if meteor.rect.right <= 0:
                self.meteors.remove(meteor)
                if self.meteors_dodged < METEORS_TO_DODGE:
                    self.score += meteor.points
                    self.meteors_dodged += 1

    def _move_background(self):
        '''
        The method that makes the background movement
        '''
        x_rel = self.background_x % self.rect.width
        self.screen.blit(self.background, (x_rel - self.rect.width ,0))
        if x_rel < WIDTH:
            self.screen.blit(self.background, (x_rel,0))
        self.background_x -= 1

    def _collition(self):
        '''
        Collitions method.
        We check the collitions if the state of our ship is 'ALIVE'.
        Then we change the state to 'EXPLODING' and makes the explosion
        sound
        '''
        if self.ship.state == STATES['ALIVE']:
            if pg.sprite.spritecollide(self.ship, self.meteors, True):
                self.ship.state = STATES['EXPLODING']
                self.ship.explosion_sound.set_volume(0.02)
                self.ship.explosion_sound.play()

    def _initial_screen(self):
        #TODO: This method
        pass

    def _black_screen(self, lifes, ticks):
        '''
        The method that shows the black screen when ship
        explodes
        '''
        start = False
        while not start:
            dt = self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == K_SPACE:
                        start = True
            ticks += dt
            self.screen.fill(BLACK)
            
            draw_text2(self.screen, SPACE2, 32, 'Level 1 - 1', WHITE, position='closecenterup', width=WIDTH, height=HEIGHT)
            draw_text2(self.screen, SPACE, 16, 'Lifes - ', WHITE, position='closecenterleft', width=WIDTH, height=HEIGHT)
            
            x_pos_lifes = 0
            for life in range(lifes):
                self.screen.blit(self.ship.image, ((WIDTH/2-(self.ship.rect.w/2))+x_pos_lifes, HEIGHT/2-(self.ship.rect.w/2)))
                x_pos_lifes += self.ship.rect.w

            if ticks <= 500:                
                draw_text2(self.screen, SPACE, 16, 'Press < SPACE > to start', WHITE, position='bottomcenter', width=WIDTH, height=HEIGHT)
            elif ticks <= 1000:
                pass
            else:
                ticks = 0
            
            pg.display.flip()

    def _top_level_menu(self):
        '''
        Method that shows the top level image and text
        '''
        top_level_img, top_level_img_rect = load_image(IMAGES_FOLDER, 'score1.png')
        draw_text2(self.screen, SPACE, 16, f'Lifes - {self.ship.lifes}', WHITE, pos_x=50, pos_y=15)
        draw_text2(self.screen, SPACE, 16, f'Meteors Dodged - {self.meteors_dodged}', WHITE, pos_x=240, pos_y=15)
        draw_text2(self.screen, SPACE, 16, f'Score - {self.score}', WHITE, pos_x=590, pos_y=15)
        
        self.screen.blit(top_level_img, (0, 0))

    def _end_level_msg(self):
        '''
        Method that shows the last messages on the screen, when
        the planet appears
        '''
        if self.planet_x >= 270:
            if self.ship.state == STATES['ALIVE']:
                draw_text2(self.screen, SPACE, 16, 'Press < SPACE > to rotate the ship', WHITE, position='topcenter', pos_y=75, width=WIDTH)
            if self.ship.state == STATES['ROTATING']:
                draw_text2(self.screen, SPACE, 16, 'Rotating ship, please, wait...', WHITE, position='topcenter', pos_y=75, width=WIDTH)
            if self.ship.state == STATES['PREPARED TO LAND']:
                draw_text2(self.screen, SPACE, 16, 'Press < SPACE > to land', WHITE, position='topcenter', pos_y=75, width=WIDTH)
            if self.ship.state == STATES['LANDING']:
                draw_text2(self.screen, SPACE, 16, 'Landing, please, wait...', WHITE, position='topcenter', pos_y=75, width=WIDTH)
        else:
            if self.ship.state == STATES['LANDED']:
                draw_text2(self.screen, SPACE, 26, 'SUCCESSFULLY LANDED!', WHITE, position='topcenter', pos_y=75, width=WIDTH)
            if self.ship.state == STATES['HIDDEN']:
                draw_text2(self.screen, SPACE2, 54, 'JUPITER CONQUERED!', WHITE, position='center', width=WIDTH, height=HEIGHT)
                draw_text2(self.screen, SPACE, 16, 'Press < SPACE > to continue', WHITE, position='bottomcenter', width=WIDTH, height=HEIGHT)
                
    def _reset(self):
        '''
        Method that resets the meteors Group, ship state to "ALIVE", the ship rect y to 276(initial y),
        the var for the planet draw to 0, and meteors dodged and score to 0
        '''
        self.meteors.empty()
        self.ship.state = STATES['ALIVE']
        self.ship.rect.y = 276
        self.planet_x = 0
        self.meteors_dodged = 0
        self.score = 0


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
        '''
        The main loop for initial screen, that show slowly the top level and ship 
        '''
        while self.starting:
            dt = pg.time.Clock().tick(FPS)
            self._handle_events()
            self._update(dt)
            self._update_ix_pos(dt)
                
    def _handle_events(self):
        '''
        Handling events
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and self.ix_pos == 0:
                    self.starting = False

    def _update(self, dt):
        '''
        Update method, that draws everything we need, background, top level img, lifes, meteors dodged and score
        and ship.
        When all that stuff is in, then we show a Ready and press button message
        '''
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
        '''
        Method that shows the ready and press button message.
        We draw the press button message blink
        '''
        self.screen.blit(self.ready_txt, ((WIDTH/2)-(self.ready_txt.get_size()[0]//2), (HEIGHT/2)/2))

        if self.ticks <= 1000:
            self.screen.blit(self.start_txt, ((WIDTH/2)-(self.start_txt.get_size()[0]//2), (HEIGHT/2)-(self.start_txt.get_size()[1]//2)))
        elif self.ticks <= 1500:
            pass
        else:
            self.ticks = 0

        self.ticks += dt

    def _update_ix_pos(self, dt):
        '''
        The update for self.ix_pos. It works with top level and ship, for slowly movement
        '''
        if self.ix_pos == 0:
            return

        self.ticks += dt
        if self.ticks >= 85:
            self.ix_pos += 1
            self.ticks = 0
