import pygame
from random import random, randint
from config import *

class IceParticles:
    def __init__(self, x, y, game_state=None):
        if game_state is None:
            raise ValueError("game_state must be provided")
        self.game_state = game_state


    def update(self):
        # Обновление позиций частиц
        for p in self.particles:
            p[0] += p[2] * 2  # Движение по X
            p[1] += p[3] * 2  # Движение по Y
            p[4] -= 1         # Уменьшение времени жизни
        # Удаление "мертвых" частиц
        self.particles = [p for p in self.particles if p[4] > 0]
        
    def draw(self):
        for p in self.particles:
            alpha = min(255, p[4] * 15)
            s = pygame.Surface((3, 3), pygame.SRCALPHA)
            s.fill((150, 200, 255, alpha))
            self.game_state.window.blit(s, (p[0], p[1]))