import pygame
from config import *
from assets import *
from bang import Bang

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage, game_state=None):
        # Инициализация пули
        if game_state is None:
            raise ValueError("game_state must be provided")
        self.game_state = game_state
        self.parent = parent  # Кто выпустил пулю
        self.px, self.py = px, py  # Позиция
        self.dx, self.dy = dx, dy  # Направление
        self.damage = damage  # Урон

        game_state.bullets.append(self)
        sndShot.play()  # Звук выстрела

    def update(self):
        # Обновление позиции пули
        self.px += self.dx
        self.py += self.dy

        # Проверка выхода за границы экрана
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            self.game_state.bullets.remove(self)
        else:
            # Проверка столкновений с объектами
            for obj in self.game_state.objects:
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)  # Нанесение урона
                        self.game_state.bullets.remove(self)
                        Bang(self.px, self.py, game_state=self.game_state)  # Создание взрыва
                        sndDestroy.play()  # Звук разрушения
                        break

    def draw(self):
    # Отрисовка пули
        pygame.draw.circle(self.game_state.window, 'yellow', (self.px, self.py), 2)
