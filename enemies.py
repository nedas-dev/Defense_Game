import pygame

class Enemy1():

    def __init__(self, game, x, y):
        self.main_game = game

        self.image_lib = self.upload_images()
        self.img_index = 0

        self.image = self.image_lib[self.img_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.counter = 1

        self.floatx = float(x)
        self.floaty = float(y)

        self.hp = float(15)

    def upload_images(self):
        ''' Uploading all the images for animation of an enemy. '''
        return [pygame.transform.scale(pygame.image.load('images_final/Enemies/1/2_enemies_1_walk_000.png').convert_alpha(), (80, 80)), pygame.transform.scale(pygame.image.load(
            'images_final/Enemies/1/2_enemies_1_walk_001.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_002.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_003.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_004.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_005.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_006.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_007.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_008.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_009.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_010.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_011.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_012.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_013.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_014.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_015.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_016.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_017.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'images_final/Enemies/1/2_enemies_1_walk_018.png').convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load('images_final/Enemies/1/2_enemies_1_walk_019.png').convert_alpha(), (80, 80))]

    def update(self):
        ''' Updating the enemy '''
        pot_x = self.update_walk_path(self.main_game.path)
        self.update_image(pot_x)

    def update_image(self, pot_x):
        ''' Updating the animation '''
        self.img_index += 0.35
        if int(self.img_index) == 20:
            self.img_index = 0
        self.image = self.image_lib[int(self.img_index)]
        if pot_x > 0:
            x, y = self.rect.midbottom
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(midbottom=(x - 22, y))

    def update_walk_path(self, path):
        ''' Updating the path that enemies are using to walk. '''

        # x, y are the new direction that the enemy has to reach
        x, y = path[self.counter]

        pot_xx = (path[self.counter - 1][0] - x) / 100

        # Calculating the speed of enemy
        pot_x = abs((path[self.counter - 1][0] - x) / 100)
        pot_y = abs((path[self.counter - 1][1] - y) / 100)

        # Updating enemy's location
        if path[self.counter - 1][0] < x:
            self.floatx += pot_x
            self.rect.centerx = self.floatx
        else:
            self.floatx -= pot_x
            self.rect.centerx = self.floatx

        if path[self.counter - 1][1] < y:
            self.floaty += pot_y
            self.rect.centery = self.floaty
        else:
            self.floaty -= pot_y
            self.rect.centery = self.floaty

        # Updating self.counter, updating directions for enemy
        if abs(self.rect.centerx - x) <= 3 and abs(self.rect.centery - y) <= 3:
            self.counter += 1

        # Removing the enemy from the list when it is no longer on the screen
        if self.counter + 1 == len(path):
            self.main_game.enemies.remove(self)

        return pot_xx

    def draw(self):
        ''' Drawying the enemy to the screen. '''
        self.main_game.screen.blit(self.image, self.rect)
