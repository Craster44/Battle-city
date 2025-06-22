import pygame
from random import randint, choice
from config import *
from assets import *
from menu import show_menu
from tank import Tank
from block import Block
from bonus import Bonus
from bullet import Bullet
from bang import Bang
from ice_particles import IceParticles
from game_state import GameState  # Импортируем GameState

def create_blocks(game_state):
    #Создание блоков на карте.
    block_types = ['brick', 'armor', 'bushes', 'ice']
    for _ in range(150):
        attempts = 0
        while attempts < 100:
            x = randint(0, WIDTH // TILE - 1) * TILE
            y = randint(1, HEIGHT // TILE - 1) * TILE
            rect = pygame.Rect(x, y, TILE, TILE)

            collision = False
            for obj in game_state.objects:  # Используем game_state.objects
                if (obj.type == 'tank' or obj.type == 'block') and rect.colliderect(obj.rect):
                    collision = True
                    break

            if not collision:
                block_type = choice(block_types)
                if block_type == 'brick' and randint(1, 100) > 70: continue
                elif block_type == 'armor' and randint(1, 100) > 90: continue
                Block(x, y, TILE, block_type, game_state=game_state)  # Передаем game_state
                break
            attempts += 1


def draw_objects(game_state):
    """Отрисовка всех игровых объектов."""
    game_state.window.fill('black')

    for obj in game_state.objects:
        if obj.type == 'block' and obj.block_type not in ['ice', 'bushes']:
            obj.draw(game_state)  # Передаем game_state

    for obj in game_state.objects:
        if obj.type == 'block' and obj.block_type == 'bushes':
            obj.draw(game_state)  # Передаем game_state

    for obj in game_state.objects:
        if obj.type == 'tank':
            obj.draw()

    for obj in game_state.objects:
        if obj.type == 'block' and obj.block_type == 'ice':
            obj.draw(game_state)  # Передаем game_state

    for obj in game_state.objects:
        if obj.type == 'bonus':
            obj.draw()

    for bullet in game_state.bullets:  # Используем game_state.bullets
        bullet.draw()

    i = 0
    for obj in game_state.objects:
        if obj.type == 'tank':
            pygame.draw.rect(game_state.window, obj.color, (5 + i * 70, 5, 22, 22))
            text = fontUI.render(str(obj.rank), 1, 'black')
            rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
            game_state.window.blit(text, rect)
            text = fontUI.render(str(obj.hp), 1, obj.color)
            rect = text.get_rect(center=(5 + i * 70 + TILE, 5 + 11))
            game_state.window.blit(text, rect)
            i += 1


def check_win_condition(game_state):
    """Проверка условий победы."""
    tanks = [obj for obj in game_state.objects if obj.type == 'tank']  # Используем game_state.objects
    if len(tanks) == 1:
        return tanks[0]
    return None

def main():
    """Основная функция игры."""

    # Pygame Init
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('TANKS')
    clock = pygame.time.Clock()

    #Sound init
    pygame.mixer.music.load('sounds/level_start.mp3')
    pygame.mixer.music.play()

    # Создаем экземпляр GameState
    game_state = GameState()
    game_state.window = window # передаем окно в game_state

    #Show Menu
    play, difficulty = show_menu(game_state.window)
    if not play:
        pygame.quit()
        return


    # Теперь передаем game_state при создании объектов
    tank1 = Tank('blue', 50, 50, 1, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), game_state=game_state)

    if difficulty == 1:
        Tank('red', 700, 500, randint(0, 3), is_ai=True, rank=0, hp=5, game_state=game_state)
    elif difficulty == 2:
        Tank('red', 700, 500, randint(0, 3), is_ai=True, rank=1, hp=7, game_state=game_state)
        Tank('darkgreen', 700, 100, randint(0, 3), is_ai=True, rank=3, hp=7, game_state=game_state)
    elif difficulty == 3:
        Tank('red', 700, 500, randint(0, 3), is_ai=True, rank=7, hp=10, game_state=game_state)
        Tank('purple', 700, 100, randint(0, 3), is_ai=True, rank=5, hp=10, game_state=game_state)
        Tank('darkblue', 100, 500, randint(0, 3), is_ai=True, rank=0, hp=10, game_state=game_state)
    else:
        tank2 = Tank('red', 700, 500, 3, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN), game_state=game_state)

    create_blocks(game_state)

    bonusTimer = 180
    timer = 0
    isMove = False
    isWin = False
    winner = None
    y = 0  # Menu Animation

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        game_state.keys = keys # передаем keys в game_state

        timer += 1

        if timer >= 260 and not isWin:
            oldIsMove = isMove
            isMove = any(obj.isMove for obj in game_state.objects if obj.type == 'tank')
            if oldIsMove != isMove:
                if isMove:
                    sndMove.play()
                    sndEngine.stop()
                else:
                    sndMove.stop()
                    sndEngine.play(-1)

        if bonusTimer > 0:
            bonusTimer -= 1
        else:
            # Считаем количество бонусов на экране
            bonus_count = sum(1 for obj in game_state.objects if obj.type == 'bonus')
            if bonus_count < 5:
                Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(imgBonuses) - 1), game_state=game_state)
            bonusTimer = randint(120, 240)

        for bullet in game_state.bullets[:]: bullet.update()
        for obj in game_state.objects[:]: obj.update(game_state)

        if not isWin:
            winner = check_win_condition(game_state)
            if winner:
                isWin = True
                timer = 1000
                pygame.mixer.music.load('sounds/level_finish.mp3')
                pygame.mixer.music.play()
                sndMove.stop()
                sndEngine.stop()

        draw_objects(game_state)

        if timer < 260:
            y += 2
            pygame.draw.rect(game_state.window, 'black', (WIDTH // 2 - 300, HEIGHT // 2 - 200 + y, 600, 250))
            pygame.draw.rect(game_state.window, 'orange', (WIDTH // 2 - 300, HEIGHT // 2 - 200 + y, 600, 250), 3)
            text = fontTitle.render('Т А Н К И', 1, 'white')
            game_state.window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100 + y))
            text = fontBig.render('ОДИН НА ОДИН', 1, 'white')
            game_state.window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20 + y))

        if isWin and winner:
            text = fontBig.render('ПОБЕДИЛ', 1, 'white')
            game_state.window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
            pygame.draw.rect(game_state.window, winner.color, (WIDTH // 2 - 100, HEIGHT // 2, 200, 200))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()