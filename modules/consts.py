import pygame, random, os

## STAŁE
## kolory
DARKRED = pygame.color.THECOLORS['darkred']
DARKGREEN = pygame.color.THECOLORS['darkgreen']
BLACK = pygame.color.THECOLORS['black']
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']
LIGHTBLUE = pygame.color.THECOLORS['lightblue']
DARKRED = pygame.color.THECOLORS['darkred']
LIGHTRED = pygame.color.THECOLORS['palevioletred']
BROWN = pygame.color.THECOLORS['brown']
WHITE = pygame.color.THECOLORS['white']


## ustawienia ekranu i gry
SIZESCREEN= 1100, 780 #1280/960
WIDTH, HEIGHT = 1100, 780
screen = pygame.display.set_mode(SIZESCREEN)
#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#SIZESCREEN = WIDTH, HEIGHT = screen.get_width(),screen.get_height()
pygame.display.set_caption('Prosta gra platformowa...')
clock = pygame.time.Clock()

# grafika  - wczytywanie znaków
file_names = sorted(os.listdir('png'))
file_names.remove('background.png')
BACKGROUND = pygame.image.load(os.path.join('png', 'background.png')).convert()
for file_name in file_names:  
    image_name = file_name[:-4]
    if '_L' in image_name or '_R' in image_name:
        image_name = image_name.upper()
    elif 'L' in image_name:
        image_name = image_name.replace('L', '_L').upper()
    elif 'R' in image_name:
        image_name = image_name.replace('R', '_R').upper()
    else:
       image_name = image_name.upper()
    globals().__setitem__(image_name, pygame.image.load(
        os.path.join('png', file_name)).convert_alpha(BACKGROUND))

 
PLAYER_RIGHT = [PLAYER_WALK_R1, PLAYER_WALK_R2]
PLAYER_LEFT = [PLAYER_WALK_L1, PLAYER_WALK_L2]

GRASS_LIST = [GRASS_SINGLE, GRASS_L, GRASS_C, GRASS_R]
METAL_LIST = [METAL_SINGLE, METAL_L, METAL_C, METAL_R]
WALL_LIST = [WALL, WALL_LEFT, WALL_TOP, WALL_RIGHT, WALL_BOTTOM]
WALL_CORNER_LIST = [WALL_TOP_L, WALL_TOP_R, WALL_BOTTOM_R, WALL_BOTTOM_L]
ZOMBIE_WALK_R = [ZOMBIE_WALK_R1, ZOMBIE_WALK_R2]
ZOMBIE_WALK_L = [ZOMBIE_WALK_L1, ZOMBIE_WALK_L2]
ZOMBIE_DEAD_R = [ZOMBIE_DEAD_R, ZOMBIE_DEAD_R]
ZOMBIE_DEAD_L = [ZOMBIE_DEAD_L, ZOMBIE_DEAD_L]
BAT_FLY_R_LIST = [BAT_FLY_R1, BAT_FLY_R2]
BAT_FLY_L_LIST = [BAT_FLY_L1, BAT_FLY_L2]
BAT_DEAD_R_LIST = [BAT_DEAD_R, BAT_DEAD_R]
BAT_DEAD_L_LIST = [BAT_DEAD_L, BAT_DEAD_L]
SPIDER_WALK_R_LIST = [SPIDER_WALK_R1, SPIDER_WALK_R2]
SPIDER_WALK_L_LIST = [SPIDER_WALK_L1, SPIDER_WALK_L2]
SPIDER_DEAD_R_LIST = [SPIDER_DEAD_R, SPIDER_DEAD_R]
SPIDER_DEAD_L_LIST = [SPIDER_DEAD_L, SPIDER_DEAD_L]


#MUZYKA i dzwieki
#test = pygame.mixer.Sound('music.mp3')
#pygame.mixer.music.load('coinpick.wav')
#pygame.mixer.music.play(-1)


