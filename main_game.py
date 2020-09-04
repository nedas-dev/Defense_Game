import pygame
import sys

from settings import Settings
from enemies import Enemy1
from towers import Tower1
from upgrade_bars import TowerMenu
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
        self.tower_menu = TowerMenu(self)
        self.tower_level1 = Tower1(self, -100, -100)
        self.selected_tower = None

    def run_game(self):
        # Main game loop
        while True:
            self.event_check()
            self.update_images()
            self.draw_images()
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
                    self.create_tower()
                elif event.key == pygame.K_j:
                    self.create_enemy()
                elif event.key == pygame.K_l:
                    print(len(self.enemies))

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.activate_tower_upgrade_screen(event.pos)
                self.tower_menu.check_collision(event.pos)

            if event.type == pygame.MOUSEMOTION:
                if self.selected_tower:
                    self.selected_tower.rect2.center = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if self.selected_tower:
                    self.selected_tower.pos_x, self.selected_tower.pos_y = event.pos
                    self.selected_tower.radar_setup()
                    self.selected_tower.activate_circle()
                    self.selected_tower.tower_active = True
                    self.selected_tower = None

    def create_enemy(self):
        ''' Creating an enemy. '''

        enemy = Enemy1(self, *self.path[0])
        self.enemies.append(enemy)

    def create_tower(self):
        ''' Creating a tower '''
        tower = Tower1(self, 362, 537)
        self.towers.append(tower)
        return tower

    def update_images(self):
        ''' Updating every object/image in the game. '''

        for enemy in self.enemies:
            enemy.update()

        for tower in self.towers:
            tower.update()

    def draw_images(self):
        ''' Drawying all the images to the screen. (background included) '''

        self.screen.blit(self.settings.bg, (0, 0))

        for enemy in self.enemies:
            enemy.draw()

        for tower in self.towers:
            tower.draw()

        self.tower_menu.draw()

    def activate_tower_upgrade_screen(self, mouse_pos):
        for tower in self.towers:
            if tower.rect2.collidepoint(mouse_pos):
                if not tower.circle_active:
                    tower.circle_active = True
                else:
                    tower.circle_active = False


if __name__ == '__main__':
    thegame = MainGame()
    thegame.run_game()
