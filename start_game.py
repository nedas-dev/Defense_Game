import pygame
class StartGame():

    def __init__(self, game):
        self.main_game = game

        self.menu_image = pygame.image.load('images_final/menu/menu.png')
        self.play_button = pygame.Rect((436, 272), (136, 141))

        self._setup_settings()

        self.menu = True
        self.settings = False

        self.active_game = False

        self.music = True
        self.sound = True

    def _pressing_buttons(self, mouse_pos):
        if not self.active_game:
            if self.play_button.collidepoint(mouse_pos) and not self.settings:
                self.menu = False
                self.active_game = True
                self.main_game.won_game.won_active = False
            elif self.settings_button.collidepoint(mouse_pos) and not self.settings:
                self.main_image = self.settings_image
                self.settings = True
                self.menu = False
            elif self.settings_exit_button.collidepoint(mouse_pos) and self.settings:
                self.settings = False
                self.menu = True
                self.main_image = self.menu_image
            elif self.music_on_image_rect.collidepoint(mouse_pos) and self.settings:
                if self.music:
                    self.music = False
                    pygame.mixer.music.pause()
                else:
                    self.music = True
                    pygame.mixer.music.unpause()
            elif self.sound_on_image_rect.collidepoint(mouse_pos) and self.settings:
                if self.sound:
                    self.sound = False
                else:
                    self.sound = True

    def _setup_settings(self):
        self.main_image = self.menu_image
        self.settings_image = pygame.image.load(
            'images_final/menu/settings.png')
        self.settings_button = pygame.Rect((58, 471), (100, 100))
        self.settings_exit_button = pygame.Rect((698, 167), (30, 26))

        self.music_on_image = pygame.transform.scale(
            pygame.image.load('images_final/menu/button_on.png'), (60, 35))
        self.music_off_image = pygame.transform.scale(
            pygame.image.load('images_final/menu/button_off.png'), (60, 35))
        self.music_on_image_rect = self.music_on_image.get_rect(
            center=(553, 312))

        self.sound_on_image = pygame.transform.scale(
            pygame.image.load('images_final/menu/button_on.png'), (60, 35))
        self.sound_off_image = pygame.transform.scale(
            pygame.image.load('images_final/menu/button_off.png'), (60, 35))
        self.sound_on_image_rect = self.sound_on_image.get_rect(
            center=(553, 380))

    def draw(self):

        if self.music:
            self.settings_image.blit(
                self.music_on_image, self.music_on_image_rect)
        else:
            self.settings_image.blit(
                self.music_off_image, self.music_on_image_rect)

        if self.sound:
            self.settings_image.blit(
                self.sound_on_image, self.sound_on_image_rect)
        else:
            self.settings_image.blit(
                self.sound_off_image, self.sound_on_image_rect)
