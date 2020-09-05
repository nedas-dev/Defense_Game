import pygame
import sys

from settings import Settings
from enemies import Enemy1
from towers import Tower1
from upgrade_bars import TowerMenu
from game_over import GameOver

class MainGame():

    def __init__(self):
        ''' Initializing the game, setting up display '''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.screen.get_rect()
        pygame.display.set_caption('Tower Defense')

        self.path = [(-10, 457), (96, 458), (147, 418), (170, 357), (204, 289), (273, 266), (328, 232), (350, 150), (392, 92), (470, 77), (574, 74), (655, 58), (710, 62), (799, 68),
                     (865, 77), (910, 98), (932, 139), (929, 188), (905, 224), (832, 261), (769, 284), (749, 321), (772, 383), (786, 439), (843, 454), (903, 470), (926, 514), (929, 580), (929, 630), (929, 700)]

        self.enemies = []
        self.towers = []

        self.lives = 10
        self.money = 1000

        # Creating an instance of tower1
        self.tower1 = Tower1(self, -100, -100)
        self.money += 500

        self.tower_menu = TowerMenu(self)

        self.selected_tower = None
        self._setup_lives_images()
        self._setup_font()
        self.game_over = GameOver(self)
        self._upload_star()

    def run_game(self):
        # Main game loop
        while True:
            self.event_check()

            if not self.game_over.game_over:
                self.update_images()
                self.draw_images()
                self._draw_update_font()
            else:
                self.screen.blit(self.game_over.game_over_img,
                                 self.game_over.game_over_rect)

            self.update_screen()

    def update_screen(self):
        ''' Updating the screen. '''
        # Update the whole screen
        pygame.display.flip()

        # Regulate FPS (Frames per second).
        self.clock.tick(60)

    def event_check(self):
        ''' Checks player's inputs (buttons pressed / mouse clicked and etc.) '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_k:
                    pass
                elif event.key == pygame.K_j:
                    self._create_enemy()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = event.pos
                self._tower_upgrade_collision(event.pos)
                self._selected_tower_control(event.type, position)
                self.game_over._checking_collision_with_restart_button(
                    position)
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                self._selected_tower_control(event.type, position)

            if event.type == pygame.MOUSEBUTTONUP:
                position = event.pos
                self._selected_tower_control(event.type, position)

    def _create_enemy(self):
        ''' Creating an enemy. '''

        enemy = Enemy1(self, *self.path[0])
        self.enemies.append(enemy)

    def _create_tower(self):
        ''' Creating a tower '''
        tower = Tower1(self, 362, 537)
        self.towers.append(tower)
        return tower

    def update_images(self):
        ''' Updating every object/image in the game. '''

        if self.lives <= 0:
            self.game_over.game_over = True

        for enemy in self.enemies:
            enemy.update()

        for tower in self.towers:
            tower.update()

    def draw_images(self):
        ''' Drawying all the images to the screen. (background included) '''
        self.screen.blit(self.settings.bg, (0, 0))

        # Draw lives image
        self.screen.blit(self.lives_img, self.lives_img_rect)
        self.screen.blit(self.heart_img, self.heart_img_rect)

        # Draw money image
        self.screen.blit(self.star_img, self.star_rect)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw()

        # Draw towers
        for tower in self.towers:
            tower.draw()

        # Draw tower menu
        self.tower_menu.draw()

    def _activate_tower_upgrade_screen(self, mouse_pos):
        for tower in self.towers:
            if tower.rect2.collidepoint(mouse_pos):
                if not tower.circle_active:
                    tower.circle_active = True
            else:
                if tower.circle_active:
                    tower.circle_active = False

    def _selected_tower_control(self, event, pos):
        if event == pygame.MOUSEBUTTONDOWN:
            # Checks if player presses on the tower and the it activates the
                                                # tower upgrade/range screen
            self._activate_tower_upgrade_screen(pos)

            # Checks if player is pressing on the tower menu on the bottom
            self.tower_menu.check_collision(pos)
        elif event == pygame.MOUSEMOTION:
            # Updating the location of tower while dragging it to the final location
            if self.selected_tower:
                self.selected_tower.rect2.center = pos
        elif event == pygame.MOUSEBUTTONUP:
            # If selected tower is not none, it initializes the tower
            if self.selected_tower:
                self.selected_tower.pos_x, self.selected_tower.pos_y = pos
                self.selected_tower.radar_setup()
                self.selected_tower.activate_circle()
                self.selected_tower.tower_active = True
                self.selected_tower = None

    def _setup_lives_images(self):
        self.heart_img = pygame.transform.scale(pygame.image.load(
            f'images_final/HP_Money/heart.png').convert_alpha(), (30, 30))
        self.heart_img_rect = self.heart_img.get_rect(
            topleft=(0, 0))

        self.lives_images = []
        for i in range(0, 10):
            self.lives_images.append(pygame.transform.scale(pygame.image.load(
                f'images_final/HP_Money/{i}.png').convert_alpha(), (22, 30)))
        self.lives_images.append(pygame.transform.scale(pygame.image.load(
            f'images_final/HP_Money/10.png').convert_alpha(), (40, 30)))
        self.lives_img = self.lives_images[10]
        self.lives_img_rect = self.lives_img.get_rect(
            topleft=(self.heart_img_rect.topright))
        self.lives_img_rect.right += 5

    def _update_lives_images(self):
        if self.lives < 0:
            self.lives_img = self.lives_images[0]
            return
        self.lives_img = self.lives_images[self.lives]
        self.heart_img_rect.topleft = (0, 0)

    def _reset_game(self):
        self.towers.clear()
        self.enemies.clear()
        self.game_over.game_over = False
        self.lives = 10
        self.money = 1000

    def _setup_font(self):
        self.beautiful = pygame.font.SysFont('metallord', 40)

    def _draw_update_font(self):
        self.text = self.beautiful.render(f'{self.money}', True, (255, 200, 0))
        self.text_rect = self.text.get_rect(midleft=(self.star_rect.right +
                                                     10, self.star_rect.centery))
        self.screen.blit(self.text, self.text_rect)

    def _upload_star(self):
        self.star_img = pygame.transform.scale(
            pygame.image.load('images_final/HP_Money/star.png'), (30, 30))
        self.star_rect = self.star_img.get_rect(
            topleft=(self.heart_img_rect.bottomleft))
        self.star_rect.y += 10

    def _tower_upgrade_collision(self, mouse_pos):
        for tower in self.towers:
            if tower.circle_active:
                tower._check_upgrade_collision(mouse_pos)


if __name__ == '__main__':
    thegame = MainGame()
    thegame.run_game()
