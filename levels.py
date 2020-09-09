import pygame
import random

class Level1():
    ''' Creating levels for the game.
        Available Level 1 only. It has 10 waves inside. '''

    def __init__(self, game):
        self.main_game = game

        # Setting up the font for the text.
        self.font = pygame.font.SysFont('metallord', 100)
        self.font_render = self.font.render('Wave 1', True, (255, 200, 0))
        self.font_rect = self.font_render.get_rect(
            center=(self.main_game.rect.center))

        # Variable which determines which wave is currently happening.
        self.current_wave = 1

        # Creating wave timer for creating enemies.
        self.WAVE = pygame.USEREVENT

        # Timer for how long the text should be drawn on the surface.
        self.font_timer = 0

        # Text that will appear in the beggining of each wave.
        self.text = 'Wave ' + str(self.current_wave)

        # Limit of enemies that will be in the wave.
        self.enemy_limit = 0

        # Current count of enemies in the game.
        self.current_amount_of_enemies = 0

        # Variable to tell what degree to turn the text to.
        self.turn_degree = 180

        # Bool switch
        self.switch = True

    def update(self):
        ''' Updating the text of the announcement which wave
            is coming. (Wave1 - Wave9, Last round). '''

        self.text = 'Wave ' + str(self.current_wave)
        if self.current_wave == 10:
            self.text = 'FINAL ROUND'
            self.font_render = self.font.render(self.text, True, (255, 200, 0))
            self.font_rect = self.font_render.get_rect(
                center=(self.main_game.rect.center))

    def draw(self):
        ''' Drawying the text to the surface of which wave is comming.
            Adding some visual effects to it (180 degree turn). '''

        if 0 <= self.font_timer < 180:
            self.font_render = self.font.render(self.text, True, (255, 200, 0))
            self.font_render = pygame.transform.rotozoom(
                self.font_render, self.turn_degree, 1)
            self.font_rect = self.font_render.get_rect(
                center=(self.main_game.rect.center))

            self.main_game.screen.blit(self.font_render, self.font_rect)
            self.font_timer += 1
            if 0 < self.turn_degree <= 180:
                self.turn_degree -= 2

        if self.font_timer >= 180:
            self.font_timer = -1
            self.turn_degree = 180
            self.call_wave(self.current_wave)

    def check_events(self, event):
        ''' Waiting for WAVE timer to kick in order to create enemies. '''

        if event.type == self.WAVE:
            self.current_amount_of_enemies += 1
            self.main_game._create_enemy(random.choice(self.randomenemy))

            if self.current_amount_of_enemies >= self.enemy_limit:
                pygame.time.set_timer(self.WAVE, 0)
                self.current_wave += 1
                self.switch = False

    def call_wave(self, wave_number):
        ''' Calling different waves, with different monsters, limit of monsters and etc. '''

        if wave_number == 1:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 10
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy1']
        elif wave_number == 2:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 15
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy1']
        elif wave_number == 3:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 20
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy1', 'enemy2']
        elif wave_number == 4:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 25
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy1', 'enemy2']
        elif wave_number == 5:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 30
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy1', 'enemy2', 'enemy3']
        elif wave_number == 6:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 35
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy2', 'enemy3', 'enemy4']
        elif wave_number == 7:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 18
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy4', 'enemy3']
        elif wave_number == 8:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 30
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy4', 'enemy3', 'enemy2']
        elif wave_number == 9:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 25
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy4', 'enemy3']
        elif wave_number == 10:
            pygame.time.set_timer(self.WAVE, 450)
            self.enemy_limit = 30
            self.current_amount_of_enemies = 0
            self.randomenemy = ['enemy4']

    def reset(self):
        ''' Resetting the wave to wave 1. '''
        self.current_wave = 1
        self.font_timer = 0

    def switch_on_n_off(self):
        ''' Bool function to check if the main game screen is runnning. '''

        if len(self.main_game.enemies) == 0 and self.font_timer == -1 and not self.current_wave == 11 and not self.switch:
            return True
        return False
