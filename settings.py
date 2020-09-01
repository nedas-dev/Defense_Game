import pygame


class Settings():
    def __init__(self):

        # Screen settings
        self.screen_width = 1000
        self.screen_height = 600

        # Uploading backround image
        self.bg = pygame.image.load('images_final/Game_Background/bg.png')
        self.bg = pygame.transform.scale(
            self.bg, (self.screen_width, self.screen_height))
