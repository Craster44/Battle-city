import pygame
from config import *
from assets import *

class Bang:
    def __init__(self, px, py, game_state=None):
        # Инициализация взрыва
        if game_state is None:
            raise ValueError("game_state must be provided")

        game_state.objects.append(self)
        self.game_state = game_state
        self.type = 'bang'
        self.px, self.py = px, py  # Позиция
        self.frame = 0  # Текущий кадр анимации

    def update(self, game_state):
        # Обновление анимации
        self.frame += 0.2
        if self.frame >= 5:  # Удаление после завершения анимации
            self.game_state.objects.remove(self)

    def draw(self):
        # Отрисовка текущего кадра анимации
        img = imgBangs[int(self.frame)]
        rect = img.get_rect(center = (self.px, self.py))
        window.blit(img, rect)