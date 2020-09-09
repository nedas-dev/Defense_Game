import pygame
import sys

from settings import Settings
from enemies import Enemy1, Enemy2, Enemy3, Enemy4
from towers import Tower1, Tower2, Tower3, Tower4
from upgrade_bars import TowerMenu
from game_over import GameOver
from start_game import StartGame
from won_game import WonGame
from levels import Level1

class MainGame():

    def __init__(self):
        ''' Initializing the game, setting up display '''
        pygame.init()
        self.xsas = 1
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.screen.get_rect()
        pygame.display.set_caption('Tower Defense')

        self.path = [(-10, 447), (96, 448), (147, 418), (170, 357), (204, 289), (273, 266), (328, 232), (350, 150), (392, 92), (470, 64), (574, 64), (655, 58), (710, 52), (799, 58),
                     (865, 67), (920, 93), (947, 139), (929, 188), (905, 224), (832, 261), (769, 284), (765, 321), (790, 383), (796, 429), (843, 454), (915, 464), (937, 514), (949, 580), (949, 630), (949, 700)]

        self.available_spots = [pygame.Rect((230,320),(81,151)), pygame.Rect((13,352),(95,50)),
                                pygame.Rect((425,123), (187,55)), pygame.Rect((781, 125), (79,82)),
                                pygame.Rect((562,301),(133,79)), pygame.Rect((816,320),(130,85)),
                                pygame.Rect((741,506), (129,88)), pygame.Rect((90,287), (50,70))]
        self.enemies = []
        self.towers = []

        self.lives = 10
        self.money = 1500

        self._important_setup()

    def run_game(self):
        # Main game loop
        while True:
            self.event_check()

            if not self.game_over.game_over and self.start_game.active_game and not self.won_game.won_active:
                self.update_images()
                self.draw_images()
                self._draw_update_font()
            elif self.game_over.game_over:
                self.screen.blit(self.game_over.game_over_img,
                                 self.game_over.game_over_rect)
            elif not self.start_game.active_game:
                self.screen.blit(self.start_game.main_image, (0,0))
                self.start_game.draw()
            elif self.won_game.won_active:
                self.won_game.draw()


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

            self.level1.check_events(event)

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = event.pos
                print(position)
                if not self.game_over.game_over and self.start_game.active_game and not self.won_game.won_active:
                    self._tower_upgrade_collision(event.pos)
                    self._selected_tower_control(event.type, position)
                self.game_over._checking_collision_with_restart_button(
                    position)
                self.start_game._pressing_buttons(position)
                self.won_game.update(event.pos)

            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                self._selected_tower_control(event.type, position)

            if event.type == pygame.MOUSEBUTTONUP:
                position = event.pos
                self._selected_tower_control(event.type, position)

    def _create_enemy(self, name):
        ''' Creating an enemy. '''
        if name == 'enemy1':
            enemy = Enemy1(self, *self.path[0])
        elif name == 'enemy2':
            enemy = Enemy2(self, *self.path[0])
        elif name == 'enemy3':
            enemy = Enemy3(self, *self.path[0])
        elif name == 'enemy4':
            enemy = Enemy4(self, *self.path[0])
        self.enemies.append(enemy)

    def _create_tower(self, name):
        ''' Creating a tower '''
        if name == 'Tower1':
            tower1 = Tower1(self, 362, 537)
            self.towers.append(tower1)
            return tower1
        elif name == 'Tower2':
            tower2 = Tower2(self, 156, 537)
            self.towers.append(tower2)
            return tower2
        elif name == 'Tower3':
            tower3 = Tower3(self, 54, 537)
            self.towers.append(tower3)
            return tower3
        elif name == 'Tower4':
            tower4 = Tower4(self, 260, 537)
            self.towers.append(tower4)
            return tower4

    def update_images(self):
        ''' Updating every object/image in the game. '''

        self._update_music()

        self.level1.update()
        if self.xsas == 1:
            self.won_game.won_active = True
            self.xsas+=1
        if len(self.enemies) == 0 and self.level1.font_timer == -1 and not self.level1.current_wave == 11:
            self.level1.font_timer = 0

        if len(self.enemies) == 0 and self.level1.font_timer == -1 and self.level1.current_wave == 11:
            self.won_game.won_active = True

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

        if self.selected_tower:
            for rect in self.available_spots:
                if rect.collidepoint((self.selected_tower.rect2.centerx, self.selected_tower.rect2.bottom-20)):
                    pygame.draw.rect(self.screen, (192, 192, 192), rect, width=3)

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

        # announcements about which wave is coming (drawying font)
        self.level1.draw()

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
        self._update_lives_images()
        self.money = 1500
        self._draw_update_font()

    def _setup_font(self):
        self.money_font = pygame.font.SysFont('metallord', 40)

    def _draw_update_font(self):
        self.text = self.money_font.render(f'{self.money}', True, (255, 200, 0))
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

    def _important_setup(self):
        # Creating an instance of tower1
        self.tower1 = Tower1(self, -100, -100)
        self.money += self.tower1.cost_history
        self.tower2 = Tower2(self, -100, -100)
        self.money += self.tower2.cost_history
        self.tower3 = Tower3(self, -100, -100)
        self.money += self.tower3.cost_history
        self.tower4 = Tower4(self, -100, -100)
        self.money += self.tower4.cost_history

        # Creating an instance of tower's menu
        self.tower_menu = TowerMenu(self)

        self.selected_tower = None
        # Setting up lives images, font, game over setup, uploading
                                # a star image for money
        self._setup_lives_images()
        self._setup_font()
        self.game_over = GameOver(self)
        self._upload_star()
        self.squares = []
        self.start_game = StartGame(self)
        self._play_music()
        self.won_game = WonGame(self)
        self.level1 = Level1(self)

    def _play_music(self):
        pygame.mixer.music.load('images_final/menu/music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1)
        pygame.mixer.music.queue('images_final/menu/music1.mp3')

    def _update_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(1)
            pygame.mixer.music.queue('images_final/menu/music.mp3')

if __name__ == '__main__':
    thegame = MainGame()
    thegame.run_game()
