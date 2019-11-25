import pygame, random, os
from modules import players, consts, levels, platforms, enemies, items



os.environ['SDL_VIDEO_CENTERED'] = '1'          # centrowanie okna
pygame.init()




      
# klasa tekst
class Text:
    def __init__(self, text, text_colour, size = 74):
        self.text = text
        self.text_colour = text_colour
        self.font = pygame.font.SysFont(None, size)
        self.image = self.font.render(str(self.text), 1, self.text_colour)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Button:
    def __init__(self, text, width, height, background_colour, text_colour):
        self.text = text
        self.width = width
        self.height = height
        self.background_colour =  background_colour
        self.text_colour = text_colour
        self.font = pygame.font.SysFont(None, 72)
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = [consts.WIDTH//2, consts.HEIGHT//2]
        self.set()

    def set(self):
        self.image = self.font.render(
            self.text,1, self.text_colour, self.background_colour)
        self.rect_image = self.image.get_rect()
        self.rect_image.center = self.rect.center

    def draw(self, surface):
        surface.fill(self.background_colour, self.rect)
        surface.blit(self.image, self.rect_image)



# konkretyzacja obiektów
player = players.Player(consts.PLAYER_STAND_R)
current_level = levels.Level_1(player)
player.level = current_level
player.rect.x = 100
player.rect.bottom = consts.HEIGHT - 70
finish_text = Text('KONIEC GRY', consts.DARKRED)
button = Button("START", 400, 150, consts.DARKGREEN, consts.BLACK)
controls_keys = Text("Sterowanie:     W/A/D -skok/lewo/prawo     SPACE - strzal",
                     consts.DARKRED, 26)




# zmienne 
window_open = True
active_game = False
# głowna pętla gry
pygame.mixer.music.load('maintheme.mp3')
pygame.mixer.music.set_volume(0.2)
#pygame.mixer.music.play(-1)
while window_open:
    #screen.fill(LIGHTBLUE)
    # pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
                break
        elif event.type == pygame.QUIT:
            window_open = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                active_game = True
                pygame.mouse.set_visible(False)
                pygame.time.delay(500)    
        if active_game:    
        #po kliknieciu button start, w trakcie gry
            #sprawdzanie eventow playera
            player.get_event(event)

    if active_game:
        if not player.lifes:
        #gdy  koniec zyc, koniec gry
            window_open = False

        #rysowanie i aktualizacja obiektów
        #w trakcie gry
        current_level.draw(consts.screen)
        player.update()
        player.draw(consts.screen)
        consts.screen.blit(consts.COIN, [consts.WIDTH-60, 0])        
        current_level.update()
    else:
        #ekran startowy
        consts.screen.fill(consts.LIGHTGREEN)
        button.draw(consts.screen)
        controls_keys.rect.center = consts.WIDTH//2, consts.HEIGHT//2+100
        controls_keys.draw(consts.screen)
        pygame.display.flip()
    
    #aktualizacja okna pygame
    pygame.display.flip()
    consts.clock.tick(30)

#ekran koncowy
pygame.time.delay(500)
pygame.mixer.music.stop()
pygame.mixer.music.load('gameover.wav')
pygame.mixer.music.play(0)
consts.screen.fill(consts.LIGHTRED)
finish_text.rect.center = consts.WIDTH//2, consts.HEIGHT//2
finish_text.draw(consts.screen)
pygame.display.flip()
pygame.time.delay(2000)

pygame.quit()
