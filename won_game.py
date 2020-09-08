import pygame

class WonGame():

    def __init__(self, game):
        self.main_game = game

        self.star_images = []
        self.bg = pygame.image.load('images_final/Won/won.png')
        self.bg_rect = self.bg.get_rect()

        self._upload_star_images()
        self.won_active = False

    def _upload_star_images(self):
        self.star_images.append(pygame.transform.scale(
            pygame.image.load('images_final/Won/1star.png'), (240, 120)))
        self.star_images.append(pygame.transform.scale(
            pygame.image.load('images_final/Won/2stars.png'), (240, 120)))
        self.star_images.append(pygame.transform.scale(
            pygame.image.load('images_final/Won/3stars.png'), (240, 120)))

    def draw(self):
        self.main_game.screen.blit(self.bg, (0, 0))
        if self.main_game.lives >= 8:
            self.bg.blit(self.star_images[2], (380, 220))
        elif 8 > self.main_game.lives > 4:
            self.bg.blit(self.star_images[1], (380, 220))
        else:
            self.bg.blit(self.star_images[0], (380, 220))
