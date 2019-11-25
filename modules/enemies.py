import pygame, random, os
from modules import items, consts, platforms

# ogólna klasa wroga
class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_image, image_right, image_left, image_dead_right,
                 image_dead_left, platform = None, movement_x = 0, movement_y = 0):
        super().__init__()
        self.image = start_image
        self.rect = self.image.get_rect()
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.direction_of_movement = 'right'
        self.platform = platform
        self.image_right = image_right
        self.image_left = image_left
        self.image_dead_right = image_dead_right
        self.image_dead_left = image_dead_left
        self.lifes = 1
        self.count = 0

        if self.platform:
            self.rect.bottom = self.platform.rect.top
            self.rect.centerx = random.randint(
                self.platform.rect.left + self.rect.width,
                self.platform.rect.right - self.rect.width)


    def update(self):
        if not self.lifes and self.count > 7:
            self.kill()

        # animacje
        if self.lifes:
            if self.movement_x > 0:
                self._move(self.image_right)
            if self.movement_x < 0:
                self._move(self.image_left)
        else:
            if self.direction_of_movement == 'right':
                self._move(self.image_dead_right)
            else:
                self._move(self.image_dead_left)
            

    def _move(self, image_list):
        if self.count < 4:
            self.image = image_list[0]
        elif self.count < 8:
            self.image = image_list[1]

        if self.count >= 8:
            self.count  = 0
        else:
            self.count += 1


class PlatformEnemy(Enemy):
    def update(self):
        super().update()
        self.rect.x += self.movement_x
        if self.rect.left < self.platform.rect.left or\
           self.rect.right > self.platform.rect.right:
            self.movement_x *= -1

        if self.movement_x > 0:
            self.direction_of_movement = 'right'
    
        if self.movement_x < 0:
            self.direction_of_movement = 'left'


class FlyingEnemy(Enemy):
    def __init__(self, start_image, image_right, image_left, image_dead_right,
                 image_dead_left, platform = None, movement_x = 0, movement_y = 0):
        super().__init__(start_image, image_right, image_left, image_dead_right,
                 image_dead_left, platform, movement_x, movement_y)
                
        self.boundary_right  = 0
        self.boundary_left = 0
        self.boundary_bottom  = 0
        self.boundary_top  = 0
        self.level = None
        self.sleep = True

    def update(self):
        if self.sleep:
            if self.rect.left - self.level.player.rect.right < 400:
                self.sleep = False
        else:
            super().update()
            self.rect.x += self.movement_x
            self.rect.y += self.movement_y
            position = self.rect.x - self.level.world_shift
            if  position < self.boundary_left or \
               position + self.rect.width > self.boundary_right:
                self.movement_x *= -1
            if self.rect.top < self.boundary_top or \
               self.rect.bottom > self.boundary_bottom:
                self.movement_y *= -1

            if self.movement_x > 0 and  self.direction_of_movement == 'left':
                self.direction_of_movement = 'right'
        
            if self.movement_x < 0 and  self.direction_of_movement == 'right':
                self.direction_of_movement = 'left'


class ShootingEnemy(Enemy):
    def __init__(self, start_image, image_right, image_left, image_dead_right,
                 image_dead_left, platform = None, movement_x = 0, movement_y = 0):
        super().__init__(start_image, image_right, image_left, image_dead_right,
                 image_dead_left, platform, movement_x, movement_y)
        self._on_platform = False
        self.health = 100

    def jump(self):
        if self._on_platform:
            self.movement_y = -18


    def shoot(self):
        bullet = items.EnemyBullet(consts.SPIDERWEB_R, self.direction_of_movement, 10)
        if self.direction_of_movement == 'left':
            bullet.image = consts.SPIDERWEB_L
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.centery = self.rect.centery + 15
        if pygame.sprite.spritecollide(
            bullet, self.level.set_of_enemy_bullets, False):
            bullet.kill()
        else:
            self.level.set_of_enemy_bullets.add(bullet)

    def update(self):
        super().update()
        self._gravitation()
            
        self.rect.x += self.movement_x
        # sprawdzanie kolizji
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms | self.level.set_of_walls, False)

        for p in colliding_platforms:
            if self.movement_x > 0:
                self.rect.right = p.rect.left
                self.movement_x *= -1
            else: 
                self.movement_x *= -1
                self.rect.left = p.rect.right

        if self.movement_x > 0:
                self.direction_of_movement = 'right'
        
        if self.movement_x < 0:
                self.direction_of_movement = 'left'


        # sprawdzamy czy wróg jest na platformie
        self.rect.y += 4  
        if pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False):
            self._on_platform = True
        else:
            self._on_platform = False
        self.rect.y -= 4

        # zmiana grafiki tylko gdy spada lub skacze       
        if not self._on_platform:
            if self.movement_y > 0:
                if self.direction_of_movement == 'left': 
                    self.image = consts.SPIDER_STAND_L
                else:
                    self.image = consts.SPIDER_STAND_R         
            if self.movement_y < 0:
                if self.direction_of_movement == 'left': 
                    self.image = consts.SPIDER_STAND_L
                else:
                    self.image = consts.SPIDER_STAND_R
                    
        if not random.randint(1,100) % 41:
            self.jump()
        if not random.randint(1,100) % 33:
            self.shoot()
            
        self.rect.y += self.movement_y
        # sprawdzanie kolizji
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms | self.level.set_of_walls, False)
        for p in colliding_platforms:
            if self.movement_y > 0:
                self.rect.bottom = p.rect.top
            if self.movement_y < 0:
                self.rect.top = p.rect.bottom

            self.movement_y = 0
            
            # obiekt jedzie razem z platformą
            if isinstance(p, platforms.MovingPlatform) and self.movement_x == 0:
                self.rect.x += p.movement_x

        
    #metoda prywatna - grawitacja
    def _gravitation(self):
        if self.movement_y == 0:
            self.movement_y = 2
        else:
            self.movement_y += 0.35  

            
        

  
