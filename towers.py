import pygame
import math
class Tower1():

    def __init__(self, game, pos_x, pos_y):
        self.main_game = game
        self.screen = game.screen
        self.level1_tower = []
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.setup_level1()
        self.radar_setup()
        self.active = False
        self.fire_count = 0
        self.shot_fire_animation()
        self.locked_x = None
        self.locked_y = None

    def update(self):
        self.shoot_range()

    def draw(self):
        if self.active:
            self.screen.blit(self.circle, self.circle_rect)

        for ind in range(3):
            if ind == 0:
                self.screen.blit(self.image1, self.rect1)
            elif ind == 1:
                self.screen.blit(self.image2, self.rect2)
            elif ind == 2:
                self.screen.blit(self.image3, self.rect3)

        self.screen.blit(self.shot, self.shot_rect)

    def setup_level1(self):
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/3.png').convert_alpha(), (75, 85))
        top_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/1.png').convert_alpha(), (65, 20))
        bottom_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/2.png').convert_alpha(), (65, 20))

        self.level1_tower.append(top_part_image)
        self.level1_tower.append(tower_body_image)
        self.level1_tower.append(bottom_part_image)

        self.image1 = self.level1_tower[0]
        self.image2 = self.level1_tower[1]
        self.image3 = self.level1_tower[2]

        self.rect1 = self.image1.get_rect(
            center=(self.pos_x - 2, self.pos_y - 30))
        self.rect2 = self.image2.get_rect(center=(self.pos_x, self.pos_y))
        self.rect3 = self.image3.get_rect(
            center=(self.pos_x - 2, self.pos_y - 10))

    def radar_setup(self):
        self.circle = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/65.png').convert_alpha(), (300, 300))
        self.circle_rect = self.circle.get_rect(
            center=(self.pos_x, self.pos_y))

    def shoot_range(self):
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
        ''' Shooting an enemy. '''
        enemy.hp -= 0.10

        self.shot_fired(enemy)

        if enemy.hp <= 0:
            self.reset_rock_position()
            self.fire_count = 0
            self.main_game.enemies.remove(enemy)

    def shot_fire_animation(self):

        self.shot = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/40.png').convert_alpha(), (20, 20))
        self.shot_rect = self.shot.get_rect(
            center=(self.rect2.centerx - 2, self.rect2.top - 8))

    def reset_rock_position(self):
        self.shot_rect = self.shot.get_rect(
            center=(self.rect2.centerx - 2, self.rect2.top - 8))

    def shot_fired(self, enemy):
        if self.fire_count == 0:
            self.locked_x = (enemy.rect.centerx - self.shot_rect.x) / 30
            self.locked_y = (enemy.rect.centery - self.shot_rect.y) / 30

        if self.fire_count == 25:
            self.reset_rock_position()
            self.fire_count = 0
            return

        self.shot_rect.x += self.locked_x
        self.shot_rect.y += self.locked_y

        self.fire_count += 1
