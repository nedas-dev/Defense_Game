import pygame


class GameOver():
    ''' When game is over this screen class will be used
        to show game over images on the surface. '''

    def __init__(self, game):
        self.main_game = game

        # Bool switch to determine if it's game over or not.
        self.game_over = False

        # Main screen of the game over mode/screen.
        self.game_over_img = pygame.transform.scale(pygame.image.load(
            'images_final/Game_Over/preview_failed.png'), (1000, 600))
        self.game_over_rect = self.game_over_img.get_rect(topleft=(0, 0))

        self._setup_game_over_restart_button()

    def _setup_game_over_restart_button(self):
        # Creating restart button.
        self.restart_button_rect = pygame.Rect(
            (531, 446), (67, 69))

        self.menu_button_rect = pygame.Rect((388, 447), (67, 69))

    def _checking_collision_with_restart_button(self, mouse_pos):
        ''' Checking for collision between
            the player's mouse coordinates and restart button,
            player's mouse coordinates and menu button. '''

        if self.game_over == True:
            # Restart button collision
            if self.restart_button_rect.collidepoint(mouse_pos):
                self.main_game.won_game.won_active = False
                self.main_game.start_game.active_game = True
                self.game_over = False
                self.main_game._reset_game()
                self.main_game.level1.reset()
                self.main_game.level1.switch = True

            # Menu button collision
            if self.menu_button_rect.collidepoint(mouse_pos):
                self.game_over = False
                self.main_game.start_game.menu = True
                self.main_game.start_game.active_game = False
                self.main_game._reset_game()
                self.main_game.level1.reset()
                self.main_game.level1.switch = True
