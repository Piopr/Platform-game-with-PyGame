import pygame, random, os

# klasa przedmiotu
class Item(pygame.sprite.Sprite):
    def __init__(self, image, name):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name


# klasa pocisku
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, direction, movement_x):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.direction_of_movement = direction
        self.movement_x = movement_x

    def update(self):
        if self.direction_of_movement == 'right':
            self.rect.x += self.movement_x
        else:
            self.rect.x -= self.movement_x

class EnemyBullet(Bullet):
    pass
