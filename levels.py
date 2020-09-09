import pygame
import random

class Level1():

    def __init__(self, game):
        self.main_game = game

        self.font = pygame.font.SysFont('metallord', 100)
        self.font_render = self.font.render('Wave 1', True, (255, 200, 0))
        self.font_rect = self.font_render.get_rect(
            center=(self.main_game.rect.center))

        self.current_wave = 1
        self.WAVE = pygame.USEREVENT

        self.font_timer = 0

        self.text = 'Wave ' + str(self.current_wave)

        self.enemy_limit = 0
        self.current_amount_of_enemies = 0

    def update(self):
        self.text = 'Wave ' + str(self.current_wave)
        if self.current_wave == 10:
            self.text = 'FINAL ROUND'
            self.font_render = self.font.render(self.text, True, (255, 200, 0))
            self.font_rect = self.font_render.get_rect(
                center=(self.main_game.rect.center))

    def draw(self):

        if 0 <= self.font_timer < 180:
            self.font_render = self.font.render(self.text, True, (255, 200, 0))
            self.main_game.screen.blit(self.font_render, self.font_rect)
            self.font_timer += 1

        if self.font_timer >= 180:
            self.font_timer = -1
            self.call_wave(self.current_wave)

    def check_events(self, event):
        if event.type == self.WAVE:
            self.current_amount_of_enemies += 1
            self.main_game._create_enemy(random.choice(self.randomenemy))

            if self.current_amount_of_enemies >= self.enemy_limit:
                pygame.time.set_timer(self.WAVE, 0)
                self.current_wave += 1

    def call_wave(self, wave_number):
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
        self.current_wave = 1
        self.font_timer = 0
