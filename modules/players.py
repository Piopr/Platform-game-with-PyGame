import pygame, random, os
from modules import consts, platforms, items, enemies, text
from random import randint



## klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self, file_image):
        super().__init__()
        self.image = file_image#pierwszy obrazek
        self.rect = self.image.get_rect()#rozmiary gracza
        self.items = set()#zbior itemow
        self.movement_x = 0
        self.movement_y = 0
        self._count = 0
        self.lifes = 3
        self.damage = 1
        self.level = None #aktualny lvl
        self.direction_of_movement = 'right'#kierunek poczatkowy
        self._on_platform = False#czy na platformie
        self.running = False#do obslugi biegania
        self.coins_number=200
        self.is_boss = False
        

    def turn_right(self):#ruch w prawo       
        if self.running == True:            
            self.movement_x = 9
            self.direction_of_movement = 'right'
        else:
            self.movement_x = 6
            self.direction_of_movement = 'right'
            

    def turn_left(self):
        if self.running == True:
            self.movement_x = -9
            self.direction_of_movement = 'left'
        else:
            self.movement_x = -6
            self.direction_of_movement = 'left'

    # metoda odpowiadając za skok 
    def jump(self):
        if self.running == True:
            if self._on_platform:
                self.movement_y = -13
        else:
            if self._on_platform:
                self.movement_y = -12
            
    
    def shoot(self):
        if 'gun' in self.items and len(self.level.set_of_bullets) < 2: 
            bullet = items.Bullet(consts.BULLET_R, self.direction_of_movement, 15)
            shotsound = pygame.mixer.Sound('shot.wav')
            shotsound.play()
            if self.direction_of_movement == 'left':
                bullet.image = consts.BULLET_L
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.centery = self.rect.centery + 15
            if pygame.sprite.spritecollide(
                bullet, self.level.set_of_bullets, False):
                bullet.kill()
            else:
                self.level.set_of_bullets.add(bullet)

    #metoda prywatna - grawitacja
    def _gravitation(self):
        if self.movement_y == 0:
            self.movement_y = 2
        else:
            self.movement_y += 0.35

    def stop_x(self):
        self.movement_x = 0
    #rysowanie postaci
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    #animacja ruchu
    def _move(self, image_list):
        if self._count < 4:
            self.image = image_list[0]
        elif self._count < 8:
            self.image = image_list[1]

        if self._count >= 8:
            self._count  = 0
        else:
            self._count += 1

    def buy(self):
        colliding_items = pygame.sprite.spritecollide(
            self, self.level.set_of_items, False)
        for item in colliding_items:
            if item.name == 'karabin':
                if self.coins_number-15>=0:
                    self.damage+=1
                    self.coins_number-=15
                    pick = pygame.mixer.Sound('pick.wav')
                    pick.play()
                    #item.kill()
            elif item.name == 'serce':
                if self.coins_number-15>=0:
                    self.lifes+=1
                    self.coins_number-=15
                    #item.kill()
                    heal = pygame.mixer.Sound('heal.wav')
                    heal.play()
            elif item.name == 'slotmachine':                
                self.coins_number = randint(0, 60)
                item.kill()
                sms = pygame.mixer.Sound('slotm.wav')
                sms.play()
            elif item.name == 'buttonik':               
                self.is_boss = True ##flaga walki z bossem
                #tworzenie sciany przed ucieczka
                sciana = [210,800,0, 0]
                object_W = platforms.Wall(*sciana)
                self.level.set_of_walls.add(object_W)                
                object_W.draw(consts.screen, consts.WALL_LIST, consts.WALL_CORNER_LIST)
                self.level.draw(consts.screen)
                
                item.kill()
                #przywolanie bossa
                spider_enemy = enemies.ShootingEnemy(
                consts.SPIDER_STAND_R, consts.SPIDER_WALK_R_LIST, consts.SPIDER_WALK_L_LIST,
                consts.SPIDER_DEAD_R_LIST, consts.SPIDER_DEAD_L_LIST,
                movement_x = random.choice([-4,-3,-2,2,3,4]))
                spider_enemy.level = self.level
                spider_enemy.rect.x = 800
                spider_enemy.rect.y = 200
                self.level.set_of_enemies.add(spider_enemy)
                self.level.set_of_moving_enemies.add(spider_enemy)
                self.level.set_boss.add(spider_enemy)
                

    def update(self):
        self._gravitation()
        #--------------ruch w poziomie---------------
        self.rect.x += self.movement_x

        # sprawdzanie kolizji
        #gracz z platformami
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms | self.level.set_of_walls, False)

        for p in colliding_platforms:
            if self.movement_x > 0:
                self.rect.right = p.rect.left
            if self.movement_x < 0:
                self.rect.left = p.rect.right
        
        # animacje
        if self.movement_x > 0:
            self._move(consts.PLAYER_RIGHT)
        if self.movement_x < 0:
            self._move(consts.PLAYER_LEFT)
        #--------------ruch w poziomie---------------

        #--------------ruch w pionie---------------
        self.rect.y += self.movement_y
        # sprawdzanie kolizji
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms | self.level.set_of_walls, False)
        for p in colliding_platforms:
            if self.movement_y > 0:
                self.rect.bottom = p.rect.top
                if self.direction_of_movement == 'left' and self.movement_x == 0: 
                    self.image = consts.PLAYER_STAND_L
                if self.direction_of_movement == 'right' and self.movement_x == 0:
                    self.image = consts.PLAYER_STAND_R
            if self.movement_y < 0:
                self.rect.top = p.rect.bottom
            #stop podczas kolizji
            self.movement_y = 0
            
            # gracz jedzie razem z platformą
            if isinstance(p, platforms.MovingPlatform) and self.movement_x == 0:
                self.rect.x += p.movement_x

        # sprawdzamy czy gracz jest na platformie
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
                    self.image = consts.PLAYER_FALL_L
                else:
                    self.image = consts.PLAYER_FALL_R         
            if self.movement_y < 0:
                if self.direction_of_movement == 'left': 
                    self.image = consts.PLAYER_JUMP_L
                else:
                    self.image = consts.PLAYER_JUMP_R

        # sprawdzamy kolizję z wrogami i pociskami wrogów lub spadek w przepaść
        enemies_bullets = set(self.level.set_of_enemy_bullets) | set(self.level.set_of_enemies)
        colliding_enmies_bullets = pygame.sprite.spritecollide(
            self, enemies_bullets, False)

        for eb in colliding_enmies_bullets:
            #kolizja z wrogiem
            if isinstance(eb, enemies.Enemy):
                if eb.lifes:
                    self.lifes -= 1
                    pygame.time.delay(500)
                    if self.is_boss:
                        self.rect.left = 300
                        self.rect.bottom = consts.HEIGHT - 150
                    else:
                        self.rect.left = 150 + self.level.world_shift
                        self.rect.bottom = consts.HEIGHT - 70
            #kolizja z pociskiem, pocisk znika
            else:
                eb.kill()
                self.lifes -= 1
                pygame.time.delay(500)
                if self.is_boss:
                        self.rect.left = 300
                        self.rect.bottom = consts.HEIGHT - 150
                else:
                    self.rect.left = 150 + self.level.world_shift
                    self.rect.bottom = consts.HEIGHT - 70
        #spadniecie w przepasc
        if self.rect.top > consts.HEIGHT:
            self.lifes -= 1
            pygame.time.delay(500)
            self.rect.left = 150 + self.level.world_shift
            self.rect.bottom = consts.HEIGHT - 70 

        # sprawdzenie kolizji z przedmiotami
        # dodanie przedmiotu do ekwipunku
        coinpick = pygame.mixer.Sound('coinpick.wav')
        colliding_items = pygame.sprite.spritecollide(
            self, self.level.set_of_items, False)
        for item in colliding_items:
            if item.name == 'gun':
                self.items.add('gun')
                item.kill()
            elif item.name == 'coin':
                self.coins_number+=1
                item.kill()
                coinpick.play()
            elif item.name == 'portal':
                teleport = pygame.mixer.Sound('teleport.wav')
                teleport.play()
                self.rect.left = 250 + self.level.world_shift
                self.rect.bottom = 400
            elif item.name == 'doors':
                if self.coins_number >= 30:
                    self.coins_number -= 30
                    item.kill()
                else:
                    self.movement_x = 0
                    #komunikat o cenie otwarcia drzwi
                    pygame.draw.rect(consts.screen, consts.BROWN,  (consts.WIDTH//2-100, 10, 400, 25))
                    komunikat = text.Text('30 coins aby otworzyc', consts.WHITE, 20)
                    komunikat.rect.x = consts.WIDTH//2
                    komunikat.rect.y = 14
                    komunikat.draw(consts.screen)
            elif item.name == 'slotmachine':
                pygame.draw.rect(consts.screen, consts.BROWN,  (consts.WIDTH//2-100, 10, 400, 25))
                komunikat = text.Text('Uzyj wszustkie monety i sproboj szczescia! Uzyj: E', consts.WHITE, 20)
                komunikat.rect.x = consts.WIDTH//2-100
                komunikat.rect.y = 14
                komunikat.draw(consts.screen)
            elif item.name == 'serce':
                pygame.draw.rect(consts.screen, consts.BROWN,  (consts.WIDTH//2-100, 10, 400, 25))
                komunikat = text.Text('Cena: 15g. Nagroda: +1 życie Kup: E', consts.WHITE, 20)
                komunikat.rect.x = consts.WIDTH//2-50
                komunikat.rect.y = 14
                komunikat.draw(consts.screen)
            elif item.name == 'karabin':
                pygame.draw.rect(consts.screen, consts.BROWN,  (consts.WIDTH//2-100, 10, 400, 25))
                komunikat = text.Text('Cena: 15g. Nagroda: +1 obrazen. Kup: E', consts.WHITE, 20)
                komunikat.rect.x = consts.WIDTH//2-50
                komunikat.rect.y = 14
                komunikat.draw(consts.screen)
            elif item.name == 'buttonik':
                pygame.draw.rect(consts.screen, consts.BROWN,  (consts.WIDTH//2-100, 10, 400, 25))
                komunikat = text.Text('Kliknij E aby rozpoczac walke z bossem', consts.WHITE, 20)
                komunikat.rect.x = consts.WIDTH//2-50
                komunikat.rect.y = 14
                komunikat.draw(consts.screen)
                
                
                        

        tmpcoins = text.Text(self.coins_number, consts.BLACK, 42)
        tmpcoins.rect.x = consts.WIDTH-90
        tmpcoins.rect.y = 20
        tmpcoins.draw(consts.screen)

        
        # rysowanie żyć na ekranie
        if self.lifes:
            for i in range(self.lifes):
                consts.screen.blit(consts.HEART, [40 * i - 40, 15])

        #rysowanie paska zdrowia bossa
        if self.is_boss:
            boss = list(self.level.set_boss)[0]
            pygame.draw.rect(consts.screen, consts.DARKRED,  (consts.WIDTH//2-100, 10, 400, 26))
            pygame.draw.rect(consts.screen, consts.DARKGREEN,  (consts.WIDTH//2-100, 13, boss.health*4, 20))
            hp = text.Text(boss.health, consts.WHITE, 20)
            hp.rect.x = consts.WIDTH//2+100
            hp.rect.y = 14
            hp.draw(consts.screen)
        

            
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:                
                self.turn_right()
            if event.key == pygame.K_a:                
                self.turn_left()
            if event.key == pygame.K_w:                
                self.jump()
            if event.key == pygame.K_SPACE:
                self.shoot()
            if event.key == pygame.K_LSHIFT:
                    self.running = True
            if event.key == pygame.K_p:
                pozycja = 'Pozycja [{}, {}]'.format(self.rect.x+(-self.level.world_shift), self.rect.y+50)
                print(pozycja)
            if event.key == pygame.K_e:
                self.buy()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.movement_x > 0:
                self.stop_x()
                self.image = consts.PLAYER_STAND_R
            if event.key == pygame.K_a and self.movement_x < 0:
                self.stop_x()
                self.image = consts.PLAYER_STAND_L
            if event.key == pygame.K_LSHIFT:
                self.running = False
