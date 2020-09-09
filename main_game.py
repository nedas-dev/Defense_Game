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
    ''' THE MAIN FILE OF THE GAME. '''

    def __init__(self):
        ''' Initializing the game, setting up display, creating main variables for the game. '''

        # General setup for pygame.
        pygame.init()

        # Creating settings instance to access it's values.
        self.settings = Settings()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.screen.get_rect()
        pygame.display.set_caption('Tower Defense')

        # Creating a list of coordinates for enemies to follow (pathway).
        self.path = [(-10, 447), (96, 448), (147, 418), (170, 357), (204, 289), (273, 266), (328, 232), (350, 150), (392, 92), (470, 64), (574, 64), (655, 58), (710, 52), (799, 58),
                     (865, 67), (920, 93), (947, 139), (929, 188), (905, 224), (832, 261), (769, 284), (765, 321), (790, 383), (796, 429), (843, 454), (915, 464), (937, 514), (949, 580), (949, 630), (949, 700)]

        # Creating a list of rectangles where the towers will be available to be spawn.
        self.available_spots = [pygame.Rect((230,320),(81,151)), pygame.Rect((13,352),(95,50)),
                                pygame.Rect((425,123), (187,55)), pygame.Rect((781, 125), (79,82)),
                                pygame.Rect((562,301),(133,79)), pygame.Rect((816,320),(130,85)),
                                pygame.Rect((741,506), (129,88)), pygame.Rect((90,287), (50,70))]

        # Creating a list for enemies.
        self.enemies = []

        # Creating a list for towers
        self.towers = []

        # Player's amount of lives in the beggining of the game
        self.lives = 10

        # Player's money given in the beggining of the game.
        self.money = self.settings.money

        # Bool switch for pausing the game.
        self.pause = False

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

            if not self.pause:
                self.level1.check_events(event)

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

            # Checking for player's mouse coordinates when the left click is pressed.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = event.pos

                if not self.game_over.game_over and self.start_game.active_game and not self.won_game.won_active:
                    self._pause_collision(position)
                    if not self.pause:
                        self._tower_upgrade_collision(event.pos)
                        self._selected_tower_control(event.type, position)

                self.game_over._checking_collision_with_restart_button(
                    position)
                self.start_game._pressing_buttons(position)
                self.won_game.update(event.pos)

            # Checking player's mouse coordinate while it's pressing and being
            # dragged over the screen.
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                if not self.pause:
                    self._selected_tower_control(event.type, position)

            # Checking for player's mouse coordinate when button was released.
            if event.type == pygame.MOUSEBUTTONUP:
                position = event.pos
                if not self.pause:
                    self._selected_tower_control(event.type, position)

    def _create_enemy(self, name):
        ''' Creating an enemy. Four different enemies are available.'''

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
        ''' Creating a tower instance. Four different towers are available. '''

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
        ''' Updating game's music, level, enemies appearance,
            player's lives count, towers appearance... '''
        if not self.pause:
            self._update_music()

            self.level1.update()

            if self.level1.switch_on_n_off():
                self.level1.font_timer = 0
                self.level1.switch = True

            if len(self.enemies) == 0 and self.level1.font_timer == -1 and self.level1.current_wave == 11:
                self.won_game.won_active = True

            if self.lives <= 0:
                self.game_over.game_over = True

            for enemy in self.enemies:
                enemy.update()

            for tower in self.towers:
                tower.update()

    def draw_images(self):
        ''' Drawying all the images to game's screen when
            the game is active. '''
        if not self.pause:
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
            self._draw_pause_button()
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
        else:
            self._draw_pause_button()

    def _activate_tower_upgrade_screen(self, mouse_pos):
        ''' When player is pressing on any tower that he has already,
            tower upgrade screen appears so you could see the range of
            the tower and have an opportunity to upgrade it.'''

        for tower in self.towers:
            if tower.rect2.collidepoint(mouse_pos):
                if not tower.circle_active:
                    tower.circle_active = True
            else:
                if tower.circle_active:
                    tower.circle_active = False

    def _selected_tower_control(self, event, pos):
        ''' If self.selected_tower is not None value,
            controlling the selected tower that player is
            trying to buy and use it in the game. '''

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
        ''' Setup for player's lives images. '''

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
        ''' Updating player's lives images. '''

        if self.lives < 0:
            self.lives_img = self.lives_images[0]
            return
        self.lives_img = self.lives_images[self.lives]
        self.heart_img_rect.topleft = (0, 0)

    def _reset_game(self):
        ''' Function to reset the game. '''

        self.towers.clear()
        self.enemies.clear()
        self.level1.reset()
        self.level1.switch = True
        self.lives = 10
        self._update_lives_images()
        self.money = self.settings.money
        self._draw_update_font()


    def _setup_font(self):
        ''' Setting up text font for game's money. '''

        self.money_font = pygame.font.SysFont('metallord', 40)

    def _draw_update_font(self):
        ''' Updating money text image. '''

        self.text = self.money_font.render(f'{self.money}', True, (255, 200, 0))
        self.text_rect = self.text.get_rect(midleft=(self.star_rect.right +
                                                     10, self.star_rect.centery))
        self.screen.blit(self.text, self.text_rect)

    def _upload_star(self):
        ''' Uploading a yellow star image for the money system. '''

        self.star_img = pygame.transform.scale(
            pygame.image.load('images_final/HP_Money/star.png'), (30, 30))
        self.star_rect = self.star_img.get_rect(
            topleft=(self.heart_img_rect.bottomleft))
        self.star_rect.y += 10

    def _tower_upgrade_collision(self, mouse_pos):
        ''' If tower's circle is active, look for tower's upgrade collision
            between the mouse press coordinates and the upgrade image. '''

        for tower in self.towers:
            if tower.circle_active:
                tower._check_upgrade_collision(mouse_pos)

    def _important_setup(self):
        ''' Creating an instance of towers, so we could access it's values.
            Also calling different setups needed for the game. '''

        # Creating tower instances, to access tower's variables
        self.tower1 = Tower1(self, -100, -100)
        # Giving money back that was taken to the player
        #   when the instance created.
        self.money += self.tower1.cost_history
        self.tower2 = Tower2(self, -100, -100)
        self.money += self.tower2.cost_history
        self.tower3 = Tower3(self, -100, -100)
        self.money += self.tower3.cost_history
        self.tower4 = Tower4(self, -100, -100)
        self.money += self.tower4.cost_history

        #
        self._setup_lives_images()
        self._setup_font()
        self._upload_star()
        self._play_music()
        self._setup_pause_button()

        self._pack_of_instances()

    def _pack_of_instances(self):
        ''' Creating different class instances in order to access it's values/variables. '''

        # Creating instance for tower menu on the bottom
        self.tower_menu = TowerMenu(self)
        # Creating a variable in order to control selected towers.
        self.selected_tower = None
        # Creating instance of the game over setup.
        self.game_over = GameOver(self)
        # Creating an instance of the game's menu images/setup.
        self.start_game = StartGame(self)
        # Creating an instance of the enviroment the player will see
        #   when he will win.
        self.won_game = WonGame(self)
        # Creating an instance of level/stage 1 which has 10 waves.
        self.level1 = Level1(self)

    def _play_music(self):
        ''' Setting up and playing game music. '''

        pygame.mixer.music.load('images_final/menu/music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1)
        pygame.mixer.music.queue('images_final/menu/music1.mp3')

    def _update_music(self):
        ''' Updating game's music. '''

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(1)
            pygame.mixer.music.queue('images_final/menu/music.mp3')

    def _setup_pause_button(self):
        ''' Initializing pause button variables, rect. '''

        self.pause_button = pygame.transform.scale(pygame.image.load('images_final/Pause/button_pause.png'), (80,80))
        self.pause_button_rect = self.pause_button.get_rect(topright=(1000,0))
        self.play_button = pygame.transform.scale(pygame.image.load('images_final/Pause/button_play.png'), (80,80))

    def _draw_pause_button(self):
        ''' Drawying pause button the screen when needed. '''

        if self.pause:
            self.screen.blit(self.play_button, self.pause_button_rect)
        else:
            self.screen.blit(self.pause_button, self.pause_button_rect)

    def _pause_collision(self, mouse_pos):
        ''' Checking for collision between the mouse press coordinates
            and pause button rect. '''

        if self.pause_button_rect.collidepoint(mouse_pos):
            if not self.pause:
                self.pause = True
            else:
                self.pause = False

if __name__ == '__main__':
    thegame = MainGame()
    thegame.run_game()
