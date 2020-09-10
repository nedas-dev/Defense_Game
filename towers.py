import pygame
import math


class Tower1():
    ''' Tower 1. '''
    def __init__(self, game, pos_x, pos_y):
        # Gaining access to all variables in main game file
        self.main_game = game
        self.screen = game.screen

        # Creating an empty list for tower's images
        self.tower = []
        # Setting the tower's level to 1.
        self.level = 1
        # If self.level is equal to 3 it reaches it max.
        self.max = False
        # Coordinates for setting up a tower location on the background
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Bool to tell if the tower needs to be deleted.
        self.delete = False
        # The cost of tower in level 1.
        self.cost = 500
        # The original price of the tower at level 1.
        self.cost_history = self.cost
        # Check if player has enough money to buy the tower.
        self._check_for_money()
        # Setting up level 1 tower
        self.setup_level1()

        # Bool to tell if the tower's circle around it is active.
        self.circle_active = False

        # Settings for shotting the enemy, making damage to it.
        self.fire_count = 0
        self.shot_fire_animation_setup()
        self.locked_x = None
        self.locked_y = None

        # Invisible rect existing where the tower's icon is (in tower menu).
        self.rect_around_icon = pygame.Rect((0, 0), (54, 52))
        self.rect_around_icon.center = (362, 537)

        # Variable to tell if the tower is active or not.
        self.tower_active = False
        # Tower's damage to the enemies
        self.damage = float(0.08)
        # Tower's damage multiplier when the tower is upgraded.
        self.damagex = 1.4

        self._upload_upgrade_tower_images()

        # For one time use int variable.
        self.plus = 0

    def update(self):
        ''' Updating the shooting range. '''
        self.shoot_range()
        if not self.tower_active:
            self.update_tower_location()
        else:
            if self.plus == 0:
                self.plus += 1
                self._check_if_spawn_is_available()

    def draw(self):
        ''' drawing all images of the tower on the screen/surface. '''

        if self.circle_active:
            self.screen.blit(self.circle, self.circle_rect)
            if not self.max:
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
        self.cost = 750

    def setup_level2(self):
        ''' Initializing tower's level 2. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/6.png').convert_alpha(), (75, 85))
        self.level = 2
        self.image2 = tower_body_image
        self.damage *= self.damagex
        self.main_game.money -= self.cost
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
        self.damage *= self.damagex
        self.main_game.money -= self.cost
        self.max = True

    def radar_setup(self):
        ''' Initializing radar for tower. '''
        self.circle = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/65.png').convert_alpha(), (300, 300))
        self.circle_rect = self.circle.get_rect(
            center=(self.rect2.center))

    def shoot_range(self):
        ''' Calculating the shooting range. '''

        if self.tower_active:
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
            self.main_game.money += enemy.bonus

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
        ''' Calculating the distance between the enemie and the 'bullet'. '''
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
        ''' Updating tower's location while it's being dragged to final destination. '''

        self.rect1.center = (self.rect2.centerx - 2, self.rect2.centery - 30)
        self.rect3.center = (self.rect2.centerx - 2, self.rect2.centery - 10)
        self.reset_rock_position()
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))
        self.upgrade_img_rect.y -= 20

        if self.delete == True:
            del self.main_game.towers[-1]

    def activate_circle(self):
        ''' Updating circle's location so it's center would be in the middle of the tower. '''
        self.circle_rect.center = self.rect2.center

    def _check_for_money(self):
        ''' Checking if player has enough money to get the tower.'''

        if self.cost > self.main_game.money:
            self.delete = True
        else:
            self.main_game.money -= self.cost

    def _upload_upgrade_tower_images(self):
        ''' Loading upgrade icon images to the game. '''

        self.upgrade_img = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Upgrade_tower/rock.png').convert_alpha(), (60, 90))
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))

        self.upgrade_font = pygame.font.SysFont('metallord', 12)
        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))

    def _update_n_draw_tower_upgrade(self):
        ''' Updating and drawing tower's upgrade cost and it's image. '''

        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))
        self.upgrade_font_rect.x += 6
        self.upgrade_font_rect.y -= 10
        self.screen.blit(self.upgrade_font_surface, self.upgrade_font_rect)

    def _check_upgrade_collision(self, mouse_pos):
        ''' Checking if there is collision between the tower's
            upgrade image rect and player's mouse coordinates. '''

        if self.upgrade_img_rect.collidepoint(mouse_pos):
            if self.cost <= self.main_game.money:
                if self.level == 1:
                    self.setup_level2()
                elif self.level == 2:
                    self.setup_level3()


    def _check_if_spawn_is_available(self):
        ''' Checking if the location of the tower is available. '''

        for rect in self.main_game.available_spots:
            if rect.collidepoint((self.rect2.centerx, self.rect2.bottom - 20)):
                return
        del self.main_game.towers[-1]
        self.main_game.money += self.cost_history

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

#______________________________________________Tower2____________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
class Tower2():
    ''' Tower 2. '''

    def __init__(self, game, pos_x, pos_y):
        # Gaining access to all variables in main game file
        self.main_game = game
        self.screen = game.screen

        # Creating an empty list for tower's images
        self.tower = []
        # Setting the tower's level to 1.
        self.level = 1
        # Bool to determine if tower's level is max yet.
        self.max = False
        # Coordinates for setting up a tower location on the background
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Bool to tell if the tower needs to be deleted.
        self.delete = False
        # The cost of tower in level 1.
        self.cost = 700
        # The original price of the tower at level 1.
        self.cost_history = self.cost
        # Check if player has enough money to buy the tower.
        self._check_for_money()
        # Setting up level 1 tower
        self.setup_level1()

        # Bool to tell if the tower's circle around it is active.
        self.circle_active = False

        # Settings for shotting the enemy, making damage to it.
        self.fire_count = 0
        self.shot_fire_animation_setup()
        self.locked_x = None
        self.locked_y = None

        # Invisible rect existing where the tower's icon is (in tower menu).
        self.rect_around_icon = pygame.Rect((0, 0), (54, 52))
        self.rect_around_icon.center = (156, 537)

        # Variable to tell if the tower is active or not.
        self.tower_active = False
        # Tower's damage to the enemies
        self.damage = float(0.12)
        # Tower's damage multiplier when the tower is upgraded.
        self.damagex = 1.4
        #
        self._upload_upgrade_tower_images()

        # For one time use int variable.
        self.plus = 0


    def update(self):
        ''' Updating the shooting range. '''
        self.shoot_range()
        if not self.tower_active:
            self.update_tower_location()
        else:
            if self.plus == 0:
                self.plus += 1
                self._check_if_spawn_is_available()

    def draw(self):
        ''' drawing all images of the tower on the screen/surface. '''

        if self.circle_active:
            self.screen.blit(self.circle, self.circle_rect)
            if not self.max:
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
            'images_final/Towers/Tower2/12.png').convert_alpha(), (75, 85))
        top_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower2/8.png').convert_alpha(), (65, 20))
        bottom_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower2/9.png').convert_alpha(), (65, 20))

        self.tower.append(top_part_image)
        self.tower.append(tower_body_image)
        self.tower.append(bottom_part_image)

        self.image1 = self.tower[0]
        self.image2 = self.tower[1]
        self.image3 = self.tower[2]

        self.rect1 = self.image1.get_rect(
            center=(self.pos_x - 2, self.pos_y - 33))
        self.rect2 = self.image2.get_rect(center=(self.pos_x, self.pos_y))
        self.rect3 = self.image3.get_rect(
            center=(self.pos_x - 2, self.pos_y - 15))
        self.cost = 1300

    def setup_level2(self):
        ''' Initializing tower's level 2. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower2/13.png').convert_alpha(), (75, 85))
        self.level = 2
        self.image2 = tower_body_image
        self.damage *= self.damagex
        self.main_game.money -= self.cost
        self.cost = 1800

    def setup_level3(self):
        ''' Initializing tower's level 3. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower2/14.png').convert_alpha(), (75, 85))
        top_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower2/10.png').convert_alpha(), (65, 20))
        bottom_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower2/11.png').convert_alpha(), (65, 20))
        self.level = 3
        self.image1 = top_part_image
        self.image2 = tower_body_image
        self.image3 = bottom_part_image
        self.damage *= self.damagex
        self.main_game.money -= self.cost
        self.max = True

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
            self.main_game.money += enemy.bonus

    def shot_fire_animation_setup(self):
        ''' Animation of damage made for the enemies. '''
        self.shot = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower2/51.png').convert_alpha(), (20, 20))
        self.shot_rect = self.shot.get_rect(
            center=(self.rect2.centerx - 2, self.rect2.top - 12))

    def reset_rock_position(self):
        ''' Resetting stone's location. '''
        self.shot_rect.center = (self.rect2.centerx - 2, self.rect2.top - 12)

    def shot_fired(self, enemy):
        ''' Calculating the distance between the enemie and the 'bullet'. '''
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
        ''' Updating tower's location while it's being dragged to final destination. '''

        self.rect1.center = (self.rect2.centerx - 2, self.rect2.centery - 28)
        self.rect3.center = (self.rect2.centerx - 2, self.rect2.centery - 18)
        self.reset_rock_position()
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))
        self.upgrade_img_rect.y -= 20

        if self.delete == True:
            del self.main_game.towers[-1]

    def activate_circle(self):
        ''' Updating circle's location so it's center would be in the middle of the tower. '''
        self.circle_rect.center = self.rect2.center

    def _check_for_money(self):
        ''' Checking if player has enough money to get the tower.'''

        if self.cost > self.main_game.money:
            self.delete = True
        else:
            self.main_game.money -= self.cost

    def _upload_upgrade_tower_images(self):
        ''' Loading upgrade icon images to the game. '''

        self.upgrade_img = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Upgrade_tower/fire.png').convert_alpha(), (60, 90))
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))

        self.upgrade_font = pygame.font.SysFont('metallord', 12)
        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))

    def _update_n_draw_tower_upgrade(self):
        ''' Updating and drawing tower's upgrade cost and it's image. '''

        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))
        self.upgrade_font_rect.x += 6
        self.upgrade_font_rect.y -= 10
        self.screen.blit(self.upgrade_font_surface, self.upgrade_font_rect)

    def _check_upgrade_collision(self, mouse_pos):
        ''' Checking if there is collision between the tower's
            upgrade image rect and player's mouse coordinates. '''

        if self.upgrade_img_rect.collidepoint(mouse_pos):
            if self.cost <= self.main_game.money:
                if self.level == 1:
                    self.setup_level2()
                elif self.level == 2:
                    self.setup_level3()

    def _check_if_spawn_is_available(self):
        ''' Checking if the location of the tower is available. '''

        for rect in self.main_game.available_spots:
            if rect.collidepoint((self.rect2.centerx, self.rect2.bottom - 20)):
                return
        del self.main_game.towers[-1]
        self.main_game.money += self.cost_history

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#____________________________________________________Tower3______________________________________________

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

class Tower3():
    ''' Tower 3. '''

    def __init__(self, game, pos_x, pos_y):
        # Gaining access to all variables in main game file
        self.main_game = game
        self.screen = game.screen

        # Creating an empty list for tower's images
        self.tower = []
        # Setting the tower's level to 1.
        self.level = 1
        # If self.level is equal to 3 it reaches it max.
        self.max = False
        # Coordinates for setting up a tower location on the background
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Bool to determine if the tower needs to be deleted.
        self.delete = False
        # Current price of the tower in it's current level (1).
        self.cost = 500
        # The original price of the tower in level 1.
        self.cost_history = self.cost
        self._check_for_money()
        # Setting up level 1 tower
        self.setup_level1()

        # Bool to tell if the tower's circle around it is active.
        self.circle_active = False

        # Settings for shotting the enemys, making damage
        self.fire_count = 0
        self.shot_fire_animation_setup()
        self.locked_x = None
        self.locked_y = None
        # Coordinates for setting up a tower location on the background
        self.rect_around_icon = pygame.Rect((0, 0), (54, 52))
        self.rect_around_icon.center = (54, 537)

        # Bool to determine if the tower is active or not.
        self.tower_active = False
        # Tower's damage to the enemy.
        self.damage = float(0.10)
        # Tower's damage multiplier when it is upgraded.
        self.damagex = 1.4
        #
        self._upload_upgrade_tower_images()
        # One time use int variable.
        self.plus = 0

    def update(self):
        ''' Updating the shooting range. '''
        self.shoot_range()
        if not self.tower_active:
            self.update_tower_location()
        else:
            if self.plus == 0:
                self.plus += 1
                self._check_if_spawn_is_available()

    def draw(self):
        ''' drawing all images of the tower on the screen/surface. '''

        if self.circle_active:
            self.screen.blit(self.circle, self.circle_rect)
            if not self.max:
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
            'images_final/Towers/Tower3/15.png').convert_alpha(), (75, 85))
        top_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/20.png').convert_alpha(), (65, 20))
        bottom_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/21.png').convert_alpha(), (65, 20))

        self.tower.append(top_part_image)
        self.tower.append(tower_body_image)
        self.tower.append(bottom_part_image)

        self.image1 = self.tower[0]
        self.image2 = self.tower[1]
        self.image3 = self.tower[2]

        self.rect1 = self.image1.get_rect(
            center=(self.pos_x - 2, self.pos_y - 33))
        self.rect2 = self.image2.get_rect(center=(self.pos_x, self.pos_y))
        self.rect3 = self.image3.get_rect(
            center=(self.pos_x - 2, self.pos_y - 15))
        self.cost = 1000

    def setup_level2(self):
        ''' Initializing tower's level 2. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/16.png').convert_alpha(), (75, 85))
        top_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/22.png').convert_alpha(), (65, 20))
        bottom_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/23.png').convert_alpha(), (65, 20))
        self.level = 2

        self.image1 = top_part_image
        self.image2 = tower_body_image
        self.image3 = bottom_part_image

        self.damage *= self.damagex
        self.cost = 1500
        self.main_game.money -= 1000

    def setup_level3(self):
        ''' Initializing tower's level 3. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/17.png').convert_alpha(), (75, 85))
        top_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/18.png').convert_alpha(), (65, 20))
        bottom_part_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/19.png').convert_alpha(), (65, 20))
        self.level = 3
        self.image1 = top_part_image
        self.image2 = tower_body_image
        self.image3 = bottom_part_image
        self.damage *= self.damagex
        self.main_game.money -= 1500
        self.max = True

    def radar_setup(self):
        ''' Initializing radar for tower. '''
        self.circle = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/65.png').convert_alpha(), (300, 300))
        self.circle_rect = self.circle.get_rect(
            center=(self.rect2.center))

    def shoot_range(self):
        ''' Calculating the shooting range. '''

        if self.tower_active:
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
            self.main_game.money += enemy.bonus

    def shot_fire_animation_setup(self):
        ''' Animation of damage made for the enemies. '''
        self.shot = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower3/29.png').convert_alpha(), (25, 25))
        self.shot_rect = self.shot.get_rect(
            center=(self.rect2.centerx - 2, self.rect2.top - 13))

    def reset_rock_position(self):
        ''' Resetting stone's location. '''
        self.shot_rect.center = (self.rect2.centerx - 2, self.rect2.top - 13)

    def shot_fired(self, enemy):
        ''' Calculating the distance between the enemie and the 'bullet'. '''

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
        ''' Updating tower's location while it's being dragged to final destination. '''

        self.rect1.center = (self.rect2.centerx - 2, self.rect2.centery - 27)
        self.rect3.center = (self.rect2.centerx - 2, self.rect2.centery - 10)
        self.reset_rock_position()
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))
        self.upgrade_img_rect.y -= 20

        if self.delete == True:
            del self.main_game.towers[-1]

    def activate_circle(self):
        ''' Updating circle's location so it's center would be in the middle of the tower. '''

        self.circle_rect.center = self.rect2.center

    def _upload_upgrade_tower_images(self):
        ''' Loading upgrade icon images to the game. '''

        self.upgrade_img = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Upgrade_tower/grey_last_rock.png').convert_alpha(), (60, 90))
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))

        self.upgrade_font = pygame.font.SysFont('metallord', 12)
        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))

    def _update_n_draw_tower_upgrade(self):
        ''' Updating and drawing tower's upgrade cost and it's image. '''

        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))
        self.upgrade_font_rect.x += 6
        self.upgrade_font_rect.y -= 10
        self.screen.blit(self.upgrade_font_surface, self.upgrade_font_rect)

    def _check_upgrade_collision(self, mouse_pos):
        ''' Checking if there is collision between the tower's
            upgrade image rect and player's mouse coordinates. '''

        if self.upgrade_img_rect.collidepoint(mouse_pos):
            if self.cost <= self.main_game.money:
                if self.level == 1:
                    self.setup_level2()
                elif self.level == 2:
                    self.setup_level3()

    def _check_for_money(self):
        ''' Checking if player has enough money to get the tower.'''

        if self.cost > self.main_game.money:
            self.delete = True
        else:
            self.main_game.money -= self.cost

    def _check_if_spawn_is_available(self):
        ''' Checking if the location of the tower is available. '''

        for rect in self.main_game.available_spots:
            if rect.collidepoint((self.rect2.centerx, self.rect2.bottom - 20)):
                return
        del self.main_game.towers[-1]
        self.main_game.money += self.cost_history

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#___________________________________________________Tower4_______________________________________________

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________
#________________________________________________________________________________________________________

class Tower4():
    ''' Tower 4. '''

    def __init__(self, game, pos_x, pos_y):
        # Gaining access to all variables in main game file
        self.main_game = game
        self.screen = game.screen

        # Creating an empty list for tower's images
        self.tower = []

        # Setting the tower to level 1.
        self.level = 1
        # If self.level is equal to 3 it reaches it max.
        self.max = False
        # Coordinates for setting up a tower location on the background
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Bool to tell if the tower needs to be deleted.
        self.delete = False

        self.cost = 850
        self.cost_history = self.cost
        self._check_for_money()
        # Setting up level 1 tower
        self.setup_level1()

        # Bool to tell if the tower's circle around it is active.
        self.circle_active = False

        # Settings for shotting enemies and making damage to them.
        self.fire_count = 0
        self.shot_fire_animation_setup()
        self.locked_x = None
        self.locked_y = None

        # Coordinates for setting up a tower location on the background
        self.rect_around_icon = pygame.Rect((0, 0), (54, 52))
        self.rect_around_icon.center = (260, 537)

        # Bool to determine if the tower is active or not.
        self.tower_active = False
        # Current tower's damage.
        self.damage = float(0.16)
        # Tower's damage multiplier when the tower is being upgraded.
        self.damagex = 1.4
        # Shooting range radius of the tower.
        self.shoot_radius = 130
        #
        self._upload_upgrade_tower_images()
        # One time use int variable.
        self.plus = 0

    def update(self):
        ''' Updating the shooting range. '''
        self.shoot_range()
        if not self.tower_active:
            self.update_tower_location()
        else:
            if self.plus == 0:
                self.plus += 1
                self._check_if_spawn_is_available()

    def draw(self):
        ''' drawing all images of the tower on the screen/surface. '''

        if self.circle_active:
            self.screen.blit(self.circle, self.circle_rect)
            if not self.max:
                self.screen.blit(self.upgrade_img, self.upgrade_img_rect)
                self._update_n_draw_tower_upgrade()

        for ind in range(3):
            if ind == 0:
                self.screen.blit(self.image1, self.rect1)
            elif ind == 1:
                self.screen.blit(self.image3, self.rect3)
            elif ind == 2:
                self.screen.blit(self.image2, self.rect2)

        self.screen.blit(self.shot, self.shot_rect)

    def setup_level1(self):
        ''' Initializing tower's level 1. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/24.png').convert_alpha(), (75, 45))
        left_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/28.png').convert_alpha(), (35, 40))
        right_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/28.png').convert_alpha(), (35, 40))

        self.image1 = left_image
        self.image2 = tower_body_image
        self.image3 = right_image

        self.rect1 = self.image1.get_rect(
            center=(self.pos_x - 2, self.pos_y - 33))
        self.rect2 = self.image2.get_rect(center=(self.pos_x, self.pos_y))
        self.rect3 = self.image3.get_rect(
            center=(self.pos_x - 2, self.pos_y - 15))
        self.cost = 1350

    def setup_level2(self):
        ''' Initializing tower's level 2. '''
        self.level = 2

        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/25.png').convert_alpha(), (75, 45))
        left_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/27.png').convert_alpha(), (37, 40))
        right_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/27.png').convert_alpha(), (37, 40))

        self.image1 = left_image
        self.image2 = tower_body_image
        self.image3 = right_image
        self.rect2.x += 2
        self.rect3.x += 1
        self.rect1.x -= 2

        self.damage *= self.damagex
        self.main_game.money -= self.cost
        self.cost = 1950

    def setup_level3(self):
        ''' Initializing tower's level 3. '''
        tower_body_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/26.png').convert_alpha(), (75, 45))
        left_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/27.png').convert_alpha(), (37, 40))
        right_image = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/27.png').convert_alpha(), (37, 40))

        self.image1 = left_image
        self.image2 = tower_body_image
        self.image3 = right_image

        self.level = 3
        self.damage *= self.damagex
        self.shoot_radius = 195
        self.radar_setup_upgrade()
        self.main_game.money -= self.cost
        self.max = True

    def radar_setup(self):
        ''' Initializing radar for tower. '''
        self.circle = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/65.png').convert_alpha(), (300, 300))
        self.circle_rect = self.circle.get_rect(
            center=(self.rect2.center))

    def radar_setup_upgrade(self):
        ''' Initializing radar for tower. '''
        self.circle = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/PNG/65.png').convert_alpha(), (360, 360))
        self.circle_rect = self.circle.get_rect(
            center=(self.rect2.center))


    def shoot_range(self):
        ''' Calculating the shooting range. '''

        if self.tower_active:
            if len(self.main_game.enemies) == 0:
                self.reset_rock_position()

            number = 0
            for enemy in self.main_game.enemies:
                x = abs(self.pos_x - enemy.rect.centerx)
                y = abs(self.pos_y - enemy.rect.centery)
                xy = math.sqrt(x ** 2 + y ** 2)
                if xy <= self.shoot_radius:
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
            self.main_game.money += enemy.bonus

    def shot_fire_animation_setup(self):
        ''' Animation of damage made for the enemies. '''
        self.shot = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Tower4/45.png').convert_alpha(), (25, 25))
        self.shot_rect = self.shot.get_rect(
            center=(self.rect2.centerx - 2, self.rect2.top - 44))

    def reset_rock_position(self):
        ''' Resetting stone's location. '''
        if self.level == 1:
            self.shot_rect.center = (self.rect2.centerx - 2, self.rect2.top - 44)
        else:
            self.shot_rect.center = (self.rect2.centerx - 4, self.rect2.top - 44)

    def shot_fired(self, enemy):
        ''' Calculating the distance between the enemie and the 'bullet'. '''
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
        ''' Updating tower's location while it's being dragged to final destination. '''

        self.rect1.center = (self.rect2.centerx - 20, self.rect2.centery - 30)
        self.rect3.center = (self.rect2.centerx + 13, self.rect2.centery - 30)
        self.reset_rock_position()
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))
        self.upgrade_img_rect.y -= 55

        if self.delete == True:
            del self.main_game.towers[-1]

    def activate_circle(self):
        ''' Updating circle's location so it's center
            would be in the middle of the tower. '''
        self.circle_rect.center = self.rect2.center

    def _upload_upgrade_tower_images(self):
        ''' Loading upgrade icon images to the game. '''

        self.upgrade_img = pygame.transform.scale(pygame.image.load(
            'images_final/Towers/Upgrade_tower/brown_rock.png').convert_alpha(), (60, 90))
        self.upgrade_img_rect = self.upgrade_img.get_rect(
            midbottom=(self.rect2.midtop))

        self.upgrade_font = pygame.font.SysFont('metallord', 12)
        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))

    def _update_n_draw_tower_upgrade(self):
        ''' Updating and drawing tower's upgrade cost and it's image. '''

        self.upgrade_font_surface = self.upgrade_font.render(
            f'{self.cost}', True, (255, 200, 0))
        self.upgrade_font_rect = self.upgrade_font_surface.get_rect(
            bottomleft=(self.upgrade_img_rect.bottomleft))
        self.upgrade_font_rect.x += 6
        self.upgrade_font_rect.y -= 10
        self.screen.blit(self.upgrade_font_surface, self.upgrade_font_rect)

    def _check_upgrade_collision(self, mouse_pos):
        ''' Checking if there is collision between the tower's
            upgrade image rectangle and player's mouse coordinates. '''

        if self.upgrade_img_rect.collidepoint(mouse_pos):
            if self.cost <= self.main_game.money:
                if self.level == 1:
                    self.setup_level2()
                elif self.level == 2:
                    self.setup_level3()

    def _check_for_money(self):
        ''' Checking if player has enough money to get the tower.'''

        if self.cost > self.main_game.money:
            self.delete = True
        else:
            self.main_game.money -= self.cost

    def _check_if_spawn_is_available(self):
        ''' Checking if the location of the tower is available. '''

        for rect in self.main_game.available_spots:
            if rect.collidepoint((self.rect2.centerx, self.rect2.bottom - 20)):
                return
        del self.main_game.towers[-1]
        self.main_game.money += self.cost_history
