import pygame, random, os
from modules import players, items, enemies, consts, platforms


class Level:
    def __init__(self, player = None):
        self.set_of_platforms = set()
        self.set_of_bullets = pygame.sprite.Group()
        self.set_of_enemy_bullets = pygame.sprite.Group()
        self.set_of_items = pygame.sprite.Group()
        self.set_of_enemies = pygame.sprite.Group()
        self.set_of_moving_enemies = set()
        self.set_of_walls = set()
        self.player = player
        self.world_shift = 0
        self.set_boss = set()
           
    def update(self):
        for platform in self.set_of_platforms:
            platform.update()

        self.set_of_bullets.update()
        self.set_of_enemy_bullets.update()
        self.set_of_enemies.update()

        self._delete_bullets()
            
        # przesunięcie ekranu gdy gracz jest blisko prawej krawędzi
        if self.player.rect.right >= 600:
            diff = self.player.rect.right - 600
            self.player.rect.right = 600
            self._shift_world(-diff)

        # przesunięcie ekranu gdy gracz jest blisko lewej krawędzi
        if self.player.rect.left <= 350:
            diff = 350 - self.player.rect.left
            self.player.rect.left = 350
            self._shift_world(diff)        
         

    def draw(self, surface):
        #surface.fill(LIGHTBLUE)
        for platform in self.set_of_platforms:
            if isinstance(platform, platforms.MovingPlatform):
                platform.draw(surface, consts.METAL_LIST)
            else:
                 platform.draw(surface, consts.GRASS_LIST)

        self.set_of_bullets.draw(surface)
        self.set_of_items.draw(surface)
        self.set_of_enemies.draw(surface)
        self.set_of_enemy_bullets.draw(surface)

        for wall in self.set_of_walls:
            wall.draw(surface, consts.WALL_LIST, consts.WALL_CORNER_LIST)
            

    def _shift_world(self, shift_x):
        self.world_shift += shift_x

        for platform in self.set_of_platforms | self.set_of_walls:
            platform.rect.x += shift_x

        for bullet in self.set_of_bullets:
            bullet.rect.x += shift_x

        for bullet in self.set_of_enemy_bullets:
            bullet.rect.x += shift_x

        for item in self.set_of_items:
            item.rect.x += shift_x

        for enemy in self.set_of_enemies:
            enemy.rect.x += shift_x

    def _delete_bullets(self):
        pygame.sprite.groupcollide(
            self.set_of_bullets, self.set_of_enemy_bullets, True,True)
        pygame.sprite.groupcollide(
            self.set_of_bullets, self.set_of_platforms,True,False)
        pygame.sprite.groupcollide(
            self.set_of_enemy_bullets, self.set_of_platforms,True,False)
        
        bullets = set(self.set_of_bullets) | set(self.set_of_enemy_bullets)
        for bullet in bullets:
##            # sprawdzamy kolizję z platformami i usuwamy pociski
##            if pygame.sprite.spritecollide(bullet, self.set_of_platforms):
##                bullet.kill()
            # sprawdzamy czy pocisk wyleciał poza plnszę i usuwamy go
            if bullet.rect.right > consts.WIDTH or bullet.rect.left < 0:
                bullet.kill()

            # sprawdzamy czy pocisk trafił we wroga i usuwamy obiekty
            if not isinstance(bullet, items.EnemyBullet):
                coliding_enemise = pygame.sprite.spritecollide(bullet,
                                            self.set_of_enemies, False)
                for enemy in coliding_enemise:
                    bullet.kill()
                    if isinstance(enemy, enemies.ShootingEnemy):                        
                        enemy.health-=self.player.damage
                        #enemy.lifes-=0
                        print(enemy.health, '<-zdrowieee')
                        if enemy.health<=0:
                            enemy.count = 0
                            enemy.lifes = 0
                            self.player.lifes = 0
                    elif enemy.lifes:
                        enemy.lifes -= 1
                        if not enemy.lifes:
                            enemy.count = 0
                
                



class Level_1(Level):
    def __init__(self, player = None):
        super().__init__(player)
        ws_platform_static = [[2350,70,0,consts.HEIGHT - 45],
                              [4000,70,3640,consts.HEIGHT - 45],
                              [280,70,0,400],
                              [70,70,1300,630],
                              [210,70,1000,400],
                              [560,70,1900,400],
                              [560,70, 3000,400],
                              [300,70, 4855,550],
                              [300,70, 4855,350],
                              [300,70, 4855,150]]
        #,[280,70,500,550]
        
        # tworzymy platformy
        for el in ws_platform_static:
            object_P = platforms.Platform(*el)
            self.set_of_platforms.add(object_P)

        ws_walls = [[280,800,-280, 0], [4200, 140, 0, -70],
                    [560,560,4200, 0],  [140,800,7000, 0],
                    [4200, 140, 4200, -130]]

        # tworzymy ściany
        for el in ws_walls:
            object_W = platforms.Wall(*el)
            self.set_of_walls.add(object_W)

        

        # tworzymy ruchomą platformę (ruch w poziomie)
        mp_x = platforms.MovingPlatform(210, 40, 1270, 400)
        mp_x.boundary_left = 1270
        mp_x.boundary_right = 1880
        mp_x.movement_x = 2
        mp_x.level = self
        self.set_of_platforms.add(mp_x)

        # tworzymy ruchomą platformę (ruch w pionie)
        mp_y = platforms.MovingPlatform(280, 40, 2630, 600)
        mp_y.boundary_top = 300
        mp_y.boundary_bottom = consts.HEIGHT - 30
        mp_y.movement_y = 2
        mp_y.level = self
        self.set_of_platforms.add(mp_y)


        # tworzymy ruchomą platformę (ruch w pionie)
        mp_y = platforms.MovingPlatform(280, 40, 500, 500)
        mp_y.boundary_top = 400
        mp_y.boundary_bottom = 750
        mp_y.movement_y = 2
        mp_y.level = self
        self.set_of_platforms.add(mp_y)


        # tworzymy przedmiot (broń)
        shotgun = items.Item(consts.SHOTGUN, 'gun')
        shotgun.rect.x = 1000
        shotgun.rect.bottom = consts.HEIGHT - 100
        self.set_of_items.add(shotgun)

        #stworzenie portalu
        portal = items.Item(consts.PORTAL, 'portal')
        portal.rect.x = 3600
        portal.rect.bottom = consts.HEIGHT - 50
        self.set_of_items.add(portal)

        #stworzenie drzwi
        doors = items.Item(consts.DOOR, 'doors')
        doors.rect.x = 4500
        doors.rect.bottom = consts.HEIGHT - 30
        self.set_of_items.add(doors)

        #stworzenie karabinu do kupienia
        rifle = items.Item(consts.KARABIN, 'karabin')
        rifle.rect.x = 4975
        rifle.rect.bottom = 290
        self.set_of_items.add(rifle)

        #stworzenie serca do kupienia
        serce = items.Item(consts.HEART, 'serce')
        serce.rect.x = 4975
        serce.rect.bottom = 90
        self.set_of_items.add(serce)

        #stworzenie ruletki
        slotmachine = items.Item(consts.SLOTMACHINE, 'slotmachine')
        slotmachine.rect.x = 4975
        slotmachine.rect.bottom = 560
        self.set_of_items.add(slotmachine)

        #tworzenie przycisku
        buttonik = items.Item(consts.BUTTONIK, 'buttonik')
        buttonik.rect.x = 6000
        buttonik.rect.bottom = 750
        self.set_of_items.add(buttonik)


        
        
        

        # tworzymy coinsy
        ws_coins = [[0, 340], [0, 310], [0, 280], [0, 250], [0, 220], [50, 250],
                    [1290, 570], [595, 552], [595, 442], [595, 348], [1144, 675],
                    [1027, 675], [1072, 522], [1899, 675], [2025, 675], [2124, 675],
                    [2286, 675], [2376, 535], [1131, 340], [1077, 340], [1005, 340],
                    [748, 140], [676, 140], [586, 140], [514, 140], [433, 140],
                    [199, 340], [199, 122], [1343, 340], [1493, 340], [1694, 340],
                    [1445, 122], [2021, 340], [2156, 340], [2282, 340], [2372, 340],
                    [2165, 122], [2741, 322], [2741, 252], [2741, 460], [2849, 600],
                    [2615, 632], [3037, 122], [3352, 120], [3253, 340], [3100, 340],
                    [3010, 340], [3469, 340], [4120, 423], [4021, 462], [3922, 434]]
        print('ilosc coinsow na mapie: ', len(ws_coins))

        # tworzymy coins
        for el in ws_coins:
            x, y = el
            #print(x, y)
            shotgun = items.Item(consts.COIN, 'coin')
            shotgun.rect.x = x
            shotgun.rect.y = y
            self.set_of_items.add(shotgun)

               
        
        # tworzymy wrógów z platformami (zombie)
        ws_enemy_platform = [[420,70,400,200]]
        for el in ws_enemy_platform:
            object_P = platforms.Platform(*el)
            self.set_of_platforms.add(object_P)
            platform_enemy = enemies.PlatformEnemy(consts.ZOMBIE_STAND_R, consts.ZOMBIE_WALK_R,
                                           consts.ZOMBIE_WALK_L,
                                           consts.ZOMBIE_DEAD_R, consts.ZOMBIE_DEAD_L,
                                           object_P,
                                           random.choice([-3,-2,-1,1,2,3]))
            self.set_of_enemies.add(platform_enemy)

        # tworzymy wroga (nietoperz)
        bat_enemy = enemies.FlyingEnemy(
            consts.BAT_HANG, consts.BAT_FLY_R_LIST, consts.BAT_FLY_L_LIST,
            consts.BAT_DEAD_R_LIST, consts.BAT_DEAD_L_LIST,
            movement_x = random.choice([-4,-3,-2,2,3,4]),
            movement_y = random.choice([-3,-2,-1,1,2,3]))
        bat_enemy.level = self
        bat_enemy.rect.x = 1400
        bat_enemy.rect.top = 70
        bat_enemy.boundary_top = 70
        bat_enemy.boundary_bottom = 370
        bat_enemy.boundary_left = 1150
        bat_enemy.boundary_right = 1900
        self.set_of_enemies.add(bat_enemy)

        # tworzymy wroga (pająk)
        """spider_enemy = enemies.ShootingEnemy(
            consts.SPIDER_STAND_R, consts.SPIDER_WALK_R_LIST, consts.SPIDER_WALK_L_LIST,
            consts.SPIDER_DEAD_R_LIST, consts.SPIDER_DEAD_L_LIST,
            movement_x = random.choice([-4,-3,-2,2,3,4]))
        spider_enemy.level = self
        spider_enemy.rect.x = 800
        spider_enemy.rect.y = 400
        self.set_of_enemies.add(spider_enemy)
        self.set_of_moving_enemies.add(spider_enemy)"""
        
    
    def draw(self,surface):
        surface.blit(consts.BACKGROUND, (self.world_shift//30,0))
               
        super().draw(surface)

