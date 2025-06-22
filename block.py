import pygame
from random import choice, randint
from config import *
from assets import *
from ice_particles import IceParticles

class Block:
    def __init__(self, px, py, size, block_type='brick', game_state=None):
        # Создаем прямоугольник для блока
        self.rect = pygame.Rect(px, py, size, size)
        self.game_state = game_state
        if game_state is None:
            raise ValueError("game_state must be provided")
        # Проверяем, не пересекается ли блок с другими объектами
        for obj in game_state.objects:
            if hasattr(obj, 'rect') and self.rect.colliderect(obj.rect):
                return  # Не создаем блок, если есть пересечение
                
        # Добавляем блок в список объектов
        game_state.objects.append(self)
        self.type = 'block'
        self.block_type = block_type
        
        # Настраиваем свойства в зависимости от типа блока
        if block_type == 'brick':
            self.image = imgBrick
            self.hp = 1  # Кирпич можно разрушить одним попаданием
        elif block_type == 'armor':
            self.image = imgArmor
            self.hp = float('inf')  # Броня неразрушима
        elif block_type == 'bushes':
            self.image = imgBushes
            self.hp = 0  # Кусты не имеют прочности, просто маскируют
        elif block_type == 'ice':
            self.image = imgIce
            self.hp = 1  # Лед можно разрушить
            self.image.set_alpha(180)  # Делаем лед полупрозрачным
            self.speed_boost = 1.5  # Коэффициент ускорения на льду
            
        # Масштабируем изображение под нужный размер
        self.image = pygame.transform.scale(self.image, (size, size))

    def update(self, game_state):
        # Для ледяных блоков проверяем столкновение с танком
        if self.block_type == 'ice':
            for obj in game_state.objects:
                if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                    # Увеличиваем скорость танка на льду
                    obj.moveSpeed = MOVE_SPEED[obj.rank] * self.speed_boost

    def draw(self, game_state):
    # Не рисуем кусты под танками (они должны быть под ними)
        if self.block_type != 'bushes':
            game_state.window.blit(self.image, self.rect)

    def damage(self, value):
    #"""Обработка получения урона блоком"""
        if self.block_type in ['brick', 'ice']:  # Только эти блоки можно разрушить
            self.hp -= value
        if self.hp <= 0:
            self.game_state.objects.remove(self)
            # Создаем эффект разрушения для льда
            if self.block_type == 'ice':
                self.game_state.particles.append(
                    IceParticles(
                        self.rect.centerx, 
                        self.rect.centery, 
                        game_state=self.game_state  # Передаем game_state
                    )
                )