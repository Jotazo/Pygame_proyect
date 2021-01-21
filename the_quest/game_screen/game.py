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
        self.black_screen = BlackScreen(self.screen)

        # Planet image and rect
        self.planet , self.planet_rect = load_image(IMAGES_FOLDER, 'jupiter.png')
        self.planet_x = 0 # For moving planet
        self.planet_timer = 0 # For speed draw planet

        # Vars top level
        self.score = 0
        self.meteors_dodged = 0
        
    def new_game(self):
        # Start a new game
        # self.starting_screen.initial_screen()
        self.run()

    def run(self):
        '''
        Main loop main game
        '''
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS)
            if self.ship.state == STATES['NOT ALIVE']:
                self.black_screen.black_screen(self.ship.lifes) # Look that return
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

    def _update_screen(self, dt):
        '''
        Update screen
        '''
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

        # Drawing Planet
        self.planet_timer += dt
        if self.meteors_dodged >= METEORS_TO_DODGE:
            self.screen.blit(self.planet, (WIDTH-self.planet_x, 50))
            if self.planet_x <= 270 and self.planet_timer >= 85:
                self.planet_x += 2

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

    def _top_level_menu(self):
        '''
        Method that shows the top level image and text
        '''
        top_level_img, top_level_img_rect = load_image(IMAGES_FOLDER, 'score1.png')
        lifes_font, lifes_text = draw_text(SPACE, 16, f'Lifes - {self.ship.lifes}', WHITE)
        score_font, score_text = draw_text(SPACE, 16, f'Score - {self.score}', WHITE)
        meteors_dodged_font, meteors_dodged_text = draw_text(SPACE, 16, f'Meteors Dodged - {self.meteors_dodged}', WHITE)

        self.screen.blit(top_level_img, (0, 0))
        self.screen.blit(lifes_text, (50,15))
        self.screen.blit(meteors_dodged_text, (240, 15))
        self.screen.blit(score_text, (590, 15))
        
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

class BlackScreen:

    def __init__(self, screen):

        self.screen = screen

        self.level_font, self.level_txt = draw_text(SPACE2, 32, 'Level 1 - 1', WHITE)
        self.lifes_font, self.lifes_txt = draw_text(SPACE, 16, 'Lifes - ', WHITE)
        self.lifes_img, self.lifes_rect = load_image(SHIP_FOLDER, 'ship.xcf')
        self.start_font, self.start_txt = draw_text(SPACE, 16, 'Press < SPACE > to start', WHITE)

        self.ticks = 0

        self.start = False

    def black_screen(self, lifes):
        '''
        Main loop
        '''
        while not self.start:
            dt = pg.time.Clock().tick(FPS)
            self._handle_events()
            self._update_screen(dt, lifes)
        self.start = False

    def _handle_events(self):
        '''
        Handling events
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.start = True
    
    def _update_screen(self, dt, lifes):
        '''
        Update screen filling the background with black color, and shows the text (level, lifes, press button "blink")
        '''

        self.ticks += dt

        self.screen.fill(BLACK)

        self.screen.blit(self.level_txt,  ((WIDTH/2)-(self.level_txt.get_size()[0]//2), (HEIGHT/2)//1.5))
        self.screen.blit(self.lifes_txt, ((WIDTH/2)-(self.lifes_txt.get_size()[0]//0.8), (HEIGHT/2)-(self.lifes_txt.get_size()[1]//2)))

        x_pos_lifes = 0
        for life in range(lifes):
            self.screen.blit(self.lifes_img, ((WIDTH/2-(self.lifes_rect.w/2))+x_pos_lifes, HEIGHT/2-(self.lifes_rect.w/2)))
            x_pos_lifes += self.lifes_rect.w

        if self.ticks <= 500:
            self.screen.blit(self.start_txt, (WIDTH/2-(self.start_txt.get_size()[0]//2), HEIGHT/2+HEIGHT/4))
        elif self.ticks <= 1000:
            pass
        else:
            self.ticks = 0

        pg.display.flip()