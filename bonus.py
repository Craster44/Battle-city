import pygame
from random import randint
from config import *
from assets import *

class Bonus:
    def __init__(self, px, py, bonusNum, game_state=None):
        # Инициализация бонуса
        if game_state is None:
            raise ValueError("game_state must be provided")

        game_state.objects.append(self)
        self.game_state = game_state
        self.type = 'bonus'
        
        # Позиция бонуса
        self.px, self.py = px, py
        # Тип бонуса (0 - улучшение танка, 1 - дополнительная жизнь)
        self.bonusNum = bonusNum
        # Таймер жизни бонуса (исчезнет через 600 кадров)
        self.timer = 600

        # Загрузка изображения бонуса
        self.image = imgBonuses[self.bonusNum]
        # Прямоугольник для коллизий
        self.rect = self.image.get_rect(center=(self.px, self.py))

    def update(self, game_state):
        # Уменьшаем таймер каждый кадр
        if self.timer > 0: 
            self.timer -= 1
        else: 
            self.game_state.objects.remove(self)  # Удаляем бонус по истечении времени

        # Проверяем столкновение с танками
        for obj in self.game_state.objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:  # Бонус звезды (улучшение танка)
                    if obj.rank < len(imgTanks) - 1:  # Проверяем, не максимальный ли уже уровень
                        obj.rank += 1  # Повышаем уровень танка
                        sndStar.play()  # Звук получения бонуса
                        self.game_state.objects.remove(self)  # Удаляем бонус
                        break
                elif self.bonusNum == 1:  # Бонус танка (дополнительная жизнь)
                    obj.hp += 1  # Увеличиваем здоровье
                    sndLive.play()  # Звук получения жизни
                    self.game_state.objects.remove(self)  # Удаляем бонус
                    break

    def draw(self):
        # Мигающий эффект - отрисовываем только каждые 15 кадров
        if self.timer % 30 < 15:
            self.game_state.window.blit(self.image, self.rect)