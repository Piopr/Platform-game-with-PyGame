import pygame, random, os
from modules import consts, players, enemies, items, levels


# klasa platformy
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, rect_x, rect_y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y

    def draw(self, surface, image_list):
        if self.width == 70:
            surface.blit(image_list[0], self.rect)
        else:
            surface.blit(image_list[1], self.rect)
            for i in range(70, self.width - 70, 70):
                surface.blit(image_list[2], [self.rect.x + i,self.rect.y])
            surface.blit(image_list[3], [self.rect.x + self.width - 70,self.rect.y])


# ruchoma platforma
class MovingPlatform(Platform):
    def __init__(self, width, height, rect_x, rect_y):
        super().__init__(width, height, rect_x, rect_y)
        self.movement_x = 0
        self.movement_y = 0
        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0
        self.level = None

            
    def update(self):
        # ruch prawo/lewo
        self.rect.x += self.movement_x
        # sprawdzamy kontakt z graczem
        colliding_sprites = pygame.sprite.spritecollide(
            self, self.level.set_of_moving_enemies | {self.level.player}, False)
        for sp in colliding_sprites:
            if self.movement_x < 0:
                sp.rect.right = self.rect.left
            else:
                sp.rect.left = self.rect.right

        # ruch góra/dół
        self.rect.y += self.movement_y
        # sprawdzamy kontakt z graczem i ruchomymi
        colliding_sprites = pygame.sprite.spritecollide(
            self, self.level.set_of_moving_enemies | {self.level.player}, False)

        for sp in colliding_sprites:
            if self.movement_y < 0:
                sp.rect.bottom = self.rect.top
            else:
                sp.rect.top = self.rect.bottom

        # sprawdzamy granice i decydujemy o zmianie kierunku
        if self.rect.bottom > self.boundary_bottom \
           or self.rect.top < self.boundary_top:
            self.movement_y *= -1

        position = self.rect.x - self.level.world_shift
        if position < self.boundary_left or position + self.rect.width > self.boundary_right:
            self.movement_x *= -1


# ściana
class Wall(Platform):
    def draw(self, surface, image_list_wall, image_list_wall_corner):
        for row in range(0, self.height, 70):
            if row == 0:
                surface.blit(image_list_wall_corner[0], self.rect)
                for column in range(70, self.width - 70, 70):
                    surface.blit(
                        image_list_wall[2],[self.rect.x + column, self.rect.y])
                surface.blit(image_list_wall_corner[1],
                             [self.rect.x + self.width - 70, self.rect.y])
                    
            elif row == self.height - 70:
                surface.blit(image_list_wall_corner[3],
                             [self.rect.x, self.rect.y + row])
                for column in range(70, self.width - 70, 70):
                    surface.blit(
                        image_list_wall[4],
                        [self.rect.x + column, self.rect.y + row])
                surface.blit(image_list_wall_corner[2],
                             [self.rect.x + self.width - 70, self.rect.y + row])

            else:
                surface.blit(image_list_wall[1],
                             [self.rect.x, self.rect.y + row])
                for column in range(70, self.width - 70, 70):
                    surface.blit(
                        image_list_wall[0],
                        [self.rect.x + column, self.rect.y + row])
                surface.blit(image_list_wall[3],
                             [self.rect.x + self.width - 70, self.rect.y + row])
                
        
