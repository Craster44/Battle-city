import pygame
from config import *

# Загрузка изображений блоков
imgBrick = pygame.image.load('image/block_brick.png')
imgArmor = pygame.image.load('image/block_armor.png')
imgBushes = pygame.image.load('image/block_bushes.png')
imgIce = pygame.image.load('image/block_ice.png')

# Загрузка изображений танков
imgTanks = [
    pygame.image.load('image/tank1.png'),
    pygame.image.load('image/tank2.png'),
    pygame.image.load('image/tank3.png'),
    pygame.image.load('image/tank4.png'),
    pygame.image.load('image/tank5.png'),
    pygame.image.load('image/tank6.png'),
    pygame.image.load('image/tank7.png'),
    pygame.image.load('image/tank8.png'),
]

# Загрузка изображений взрывов
imgBangs = [
    pygame.image.load('image/bang1.png'),
    pygame.image.load('image/bang2.png'),
    pygame.image.load('image/bang3.png'),
    pygame.image.load('image/bang2.png'),
    pygame.image.load('image/bang1.png'),
]

# Загрузка изображений бонусов
imgBonuses = [
    pygame.image.load('image/bonus_star.png'),
    pygame.image.load('image/bonus_tank.png'),
]

# Загрузка звуков
sndShot = pygame.mixer.Sound('sounds/shot.wav')
sndDestroy = pygame.mixer.Sound('sounds/destroy.wav')
sndDead = pygame.mixer.Sound('sounds/dead.wav')
sndLive = pygame.mixer.Sound('sounds/live.wav')
sndStar = pygame.mixer.Sound('sounds/star.wav')
sndEngine = pygame.mixer.Sound('sounds/engine.wav')
sndEngine.set_volume(0.5)
sndMove = pygame.mixer.Sound('sounds/move.wav')
sndMove.set_volume(0.5)

# Загрузка шрифтов
fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)
fontTitle = pygame.font.Font(None, 140)