import pygame

class WonGame():
    ''' The images player sees when the game is won. '''
    def __init__(self, game):
        self.main_game = game

        self.star_images = []
        self.bg = pygame.image.load('images_final/Won/won.png')
        self.bg_rect = self.bg.get_rect()

        self._upload_star_images()
        self.won_active = False
        self.menu_button = pygame.Rect((389, 439), (88, 84))
        self.continue_button = pygame.Rect((521, 439), (88, 84))

    def _upload_star_images(self):
        self.star_images.append(pygame.transform.scale(
            pygame.image.load('images_final/Won/1star.png'), (240, 120)))
        self.star_images.append(pygame.transform.scale(
            pygame.image.load('images_final/Won/2stars.png'), (240, 120)))
        self.star_images.append(pygame.transform.scale(
            pygame.image.load('images_final/Won/3stars.png'), (240, 120)))

    def draw(self):
        self.main_game.screen.blit(self.bg, (0, 0))
        if self.main_game.lives >= 9:
            self.bg.blit(self.star_images[2], (380, 220))
        elif 9 > self.main_game.lives > 4:
            self.bg.blit(self.star_images[1], (380, 220))
        else:
            self.bg.blit(self.star_images[0], (380, 220))

    def update(self, mouse_pos):
        if self.won_active == True and self.menu_button.collidepoint(mouse_pos):
            self.won_active = False
            self.main_game.start_game.menu = True
            self.main_game.start_game.active_game = False
            self.main_game.level1.reset()
            self.main_game._reset_game()
            self.main_game.level1.switch = True

        if self.won_active == True and self.continue_button.collidepoint(mouse_pos):
            self.won_active = False
            self.main_game.start_game.active_game = True
            self.main_game._reset_game()
            self.main_game.level1.reset()
            self.main_game.level1.switch = True
