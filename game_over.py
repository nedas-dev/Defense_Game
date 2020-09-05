import pygame

class GameOver():

    def __init__(self, game):
        self.main_game = game
        self.game_over = False
        self.game_over_img = pygame.image.load(
            'images_final/Game_Over/bg.png')
        self.game_over_rect = self.game_over_img.get_rect(topleft=(0, 0))
        self._setup_game_over_restart_button()

    def _setup_game_over_restart_button(self):
        self.restart_button_rect = pygame.Rect(
            (self.main_game.rect.centerx - 35, self.main_game.rect.centery + 85), (81, 82))

    def _checking_collision_with_restart_button(self, mouse_pos):
        if self.restart_button_rect.collidepoint(mouse_pos):
            self.main_game._reset_game(mouse_pos)
