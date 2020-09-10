import pygame


class Settings():
    def __init__(self):
        ''' Simple settings atributtes to determine the screen size,
            player's amount of money. '''
        # Screen settings
        self.screen_width = 1000
        self.screen_height = 600

        # Amount of money player will have in the beggining of the game.
        self.money = 1500

        # Uploading backround image
        self.bg = pygame.image.load('images_final/Game_Background/bg.png')
        self.bg = pygame.transform.scale(
            self.bg, (self.screen_width, self.screen_height))
