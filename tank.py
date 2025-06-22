import pygame
from random import randint, choice
from config import *
from assets import *
from bullet import Bullet

class Tank:
    def __init__(self, color, px, py, direct, keysList=None, is_ai=False, rank=0, hp=5, game_state=None):
        """Инициализация танка"""
        if game_state is None:
            raise ValueError("game_state must be provided")

        game_state.objects.append(self) # добавляем в список объектов game_state
        self.game_state = game_state
        self.type = 'tank'
        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = MOVE_SPEED[rank]
        self.is_ai = is_ai
        self.ai_timer = 0
        self.ai_direction = 0
        self.ai_shot_delay = randint(30, 90)
        self.hidden = False
        self.on_ice = False
        self.isMove = False

        self.shotTimer = 0
        self.shotDelay = SHOT_DELAY[rank]
        self.bulletSpeed = BULLET_SPEED[rank]
        self.bulletDamage = BULLET_DAMAGE[rank]

        self.hp = hp
        self.rank = rank

        if not is_ai:
            self.keyLEFT = keysList[0]
            self.keyRIGHT = keysList[1]
            self.keyUP = keysList[2]
            self.keyDOWN = keysList[3]
            self.keySHOT = keysList[4]

        self.update_image()

    def update_image(self):
        """Обновление изображения танка с учетом направления"""
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self):
        """Отрисовка танка с учетом прозрачности при скрытии"""
        if not self.hidden:
            self.game_state.window.blit(self.image, self.rect)  # Используем window из game_state
        else:
            temp_img = self.image.copy()
            temp_img.set_alpha(128)
            self.game_state.window.blit(temp_img, self.rect)

    def damage(self, value):
        """Получение урона"""
        self.hp -= value
        if self.hp <= 0:
            self.game_state.objects.remove(self)
            sndDead.play()
            print(self.color, 'уничтожен')

    def ai_control(self):
        """Управление для ИИ"""
        self.ai_timer -= 1
        if self.ai_timer <= 0:
            self.ai_timer = randint(30, 120)
            self.ai_direction = randint(0, 3)
            self.ai_shot_delay = randint(10, 60)

        if self.ai_direction == 0:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            self.isMove = True
        elif self.ai_direction == 1:
            self.rect.x += self.moveSpeed
            self.direct = 1
            self.isMove = True
        elif self.ai_direction == 2:
            self.rect.y += self.moveSpeed
            self.direct = 2
            self.isMove = True
        elif self.ai_direction == 3:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            self.isMove = True

        if randint(0, 100) < 3 and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage, game_state=self.game_state) # передаем game_state
            self.shotTimer = self.shotDelay

    def update(self, game_state):
        """Основное обновление состояния танка"""
        self.update_image()

        self.moveSpeed = MOVE_SPEED[self.rank] * (1.5 if self.on_ice else 1)
        self.bulletDamage = BULLET_DAMAGE[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]

        oldX, oldY = self.rect.topleft
        self.on_ice = False
        self.hidden = False

        if self.is_ai:
            self.ai_control()
        else:
            if self.game_state.keys[self.keyUP]:
                self.rect.y -= self.moveSpeed
                self.direct = 0
                self.isMove = True
            elif self.game_state.keys[self.keyRIGHT]:
                self.rect.x += self.moveSpeed
                self.direct = 1
                self.isMove = True
            elif self.game_state.keys[self.keyDOWN]:
                self.rect.y += self.moveSpeed
                self.direct = 2
                self.isMove = True
            elif self.game_state.keys[self.keyLEFT]:
                self.rect.x -= self.moveSpeed
                self.direct = 3
                self.isMove = True
            else:
                self.isMove = False

            if self.game_state.keys[self.keySHOT] and self.shotTimer == 0:
                dx = DIRECTS[self.direct][0] * self.bulletSpeed
                dy = DIRECTS[self.direct][1] * self.bulletSpeed
                Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage, game_state=self.game_state)
                self.shotTimer = self.shotDelay
                sndShot.play()

        if self.shotTimer > 0:
            self.shotTimer -= 1

        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.rect.topleft = oldX, oldY

        for obj in game_state.objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                if obj.block_type in ['brick', 'armor']:
                    self.rect.topleft = oldX, oldY
                elif obj.block_type == 'bushes':
                    self.hidden = True
                elif obj.block_type == 'ice':
                    self.on_ice = True