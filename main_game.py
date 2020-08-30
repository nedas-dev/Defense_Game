import pygame, sys

from settings import Settings

class MainGame():

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
        pygame.display.set_caption('Tower Defens')
