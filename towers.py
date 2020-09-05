import pygame
import math


class Tower1():

    def __init__(self, game, pos_x, pos_y):
        # Gaining access to all variables in main game file
        self.main_game = game
        self.screen = game.screen

        # Creating an empty list for tower's images
        self.tower = []
        self.level = 1
        # Coordinates for setting up a tower on the background
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.delete = False
        # Setting up level 1 tower
        self.setup_level1()

        # For radar to show up we create a bool
        self.circle_active = False

        # Settings for shotting the enemys, making damage
        self.fire_count = 0
        self.shot_fire_animation_setup()
        self.locked_x = None
        self.locked_y = None

        self.rect_around_icon = pygame.Rect((0, 0), (54, 52))
        self.rect_around_icon.center = (362, 537)

        #
        self.tower_active = False
        self.damage = float(0.10)

        #
        self._check_for_money()
        self._upload_upgrade_tower_images()

    def update(self):
        ''' Updating the shooting range. '''
        self.shoot_range()
        if not self.tower_active:
            self.update_tower_location()

    def draw(self):
        ''' Drawying everything on the screen. '''
        if self.circle_active:
            self.screen.blit(self.circle, self.circle_rect)
            self.screen.blit(self.upgrade_img, self.upgrade_img_rect)
            self._update_n_draw_tower_upgrade()

        for ind in range(3):
            if ind == 0:
                self.screen.blit(self.image1, self.rect1)
            elif ind == 1:
                self.screen.blit(self.image2, self.rect2)
            elif ind == 2:
                self.screen.blit(self.image3, self.rect3)

        self.screen.blit(self.shot, self.shot_rect)

    def setup_level1(self):
        ''' Initializing tower's level 1. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/3.png').convert_alpha(), (75, 85))
        top_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/1.png').convert_alpha(), (65, 20))
        bottom_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/2.png').convert_alpha(), (65, 20))

        self.tower.append(top_part_image)
        self.tower.append(tower_body_image)
        self.tower.append(bottom_part_image)

        self.image1 = self.tower[0]
        self.image2 = self.tower[1]
        self.image3 = self.tower[2]

        self.rect1 = self.image1.get_rect(
            center=(self.pos_x - 2, self.pos_y - 30))
        self.rect2 = self.image2.get_rect(center=(self.pos_x, self.pos_y))
        self.rect3 = self.image3.get_rect(
            center=(self.pos_x - 2, self.pos_y - 10))
        self.cost = 500

    def setup_level2(self):
        ''' Initializing tower's level 2. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/6.png').convert_alpha(), (75, 85))
        self.level = 2
        self.image2 = tower_body_image
        self.damage = float(0.15)
        self.cost = 1000

    def setup_level3(self):
        ''' Initializing tower's level 3. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/7.png').convert_alpha(), (75, 85))
        top_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/4.png').convert_alpha(), (65, 20))
        bottom_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/5.png').convert_alpha(), (65, 20))
        self.level = 3
        self.image1 = top_part_image
        self.image2 = tower_body_image
        self.image3 = bottom_part_image
        self.damage = float(0.25)
        self.cost = 1500

    def radar_setup(self):
        ''' Initializing radar for tower. '''
        self.circle = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/65.png').convert_alpha(), (300, 300))
        self.circle_rect = self.circle.get_rect(
            center=(self.rect2.center))

    def shoot_range(self):
        if self.tower_active:
            ''' Calculating the shooting range. '''
            if len(self.main_game.enemies) == 0:
                self.reset_rock_position()

            number = 0
            for enemy in self.main_game.enemies:
                x = abs(self.pos_x - enemy.rect.centerx)
                y = abs(self.pos_y - enemy.rect.centery)
                xy = math.sqrt(x ** 2 + y ** 2)
                if xy <= 130:
                    self.shoot(enemy)
                    break
                else:
                    number += 1
                    continue
            if len(self.main_game.enemies) == number:
                self.reset_rock_position()
                self.fire_count = 0

    def shoot(self, enemy):
        ''' Making damage to an enemy. '''
        enemy.hp -= self.damage

        self.shot_fired(enemy)

        if enemy.hp <= 0:
            self.reset_rock_position()
            self.fire_count = 0
            self.main_game.enemies.remove(enemy)
            self.main_game.money += 50

    def shot_fire_animation_setup(self):
        ''' Animation of damage made for the enemies. '''
        self.shot = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/40.png').convert_alpha(), (20, 20))
        self.shot_rect = self.shot.get_rect(
            center=(self.rect2.centerx - 2, self.rect2.top - 8))

    def reset_rock_position(self):
        ''' Resetting stone's location. '''
        self.shot_rect.center = (self.rect2.centerx - 2, self.rect2.top - 8)

    def shot_fired(self, enemy):
        if self.fire_count == 0:
            self.locked_x = (enemy.rect.centerx -
                             self.shot_rect.x) / 30
            self.locked_y = (enemy.rect.centery -
                             self.shot_rect.y) / 30

        if self.fire_count == 25:
            self.reset_rock_position()
            self.fire_count = 0
            return

        self.shot_rect.x += self.locked_x
        self.shot_rect.y += self.locked_y
        self.fire_count += 1

    def update_tower_location(self):
        self.rect1.center = (self.rect2.centerx - 2, self.rect2.centery - 30)
        self.rect3.center = (self.rect2.centerx - 2, self.rect2.centery - 10)
        self.reset_rock_position()
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))
        self.upgrade_img_rect.y -= 20

        if self.delete == True:
            del self.main_game.towers[-1]

    def activate_circle(self):
        self.circle_rect.center = self.rect2.center

    def _check_for_money(self):
        if self.main_game.money >= self.cost:
            self.main_game.money -= self.cost
        else:
            self.delete = True

    def _upload_upgrade_tower_images(self):
        self.upgrade_img = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Upgrade_tower/rock.png').convert_alpha(), (60, 90))
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))

        self.upgrade_font = pygame.font.SysFont('metallord', 12)
        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost + 500}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))

    def _update_n_draw_tower_upgrade(self):
        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost + 500}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))
        self.upgrade_font_rect.x += 6
        self.upgrade_font_rect.y -= 10
        self.screen.blit(self.upgrade_font_surface, self.upgrade_font_rect)

    def _check_upgrade_collision(self, mouse_pos):
        if self.upgrade_img_rect.collidepoint(mouse_pos):
            print('yes')
