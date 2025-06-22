import pygame
from config import *
from assets import *

def show_menu(window):  # Функция принимает окно в качестве аргумента
    """Отображение главного меню."""
    menu = True
    while menu:
        window.fill('black')  # Теперь 'window' доступно

        # Отрисовка элементов меню
        title = fontTitle.render('ТАНКИ', True, 'white')  # Заголовок
        question = fontBig.render('Количество игроков?', True, 'white')  # Вопрос
        option1 = fontUI.render('1 - 1 игрок (против ИИ)', True, 'green')  # Вариант 1
        option2 = fontUI.render('2 - 2 игрока', True, 'yellow')  # Вариант 2

        window.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))  # Рисуем заголовок
        window.blit(question, (WIDTH // 2 - question.get_width() // 2, 250))  # Рисуем вопрос
        window.blit(option1, (WIDTH // 2 - option1.get_width() // 2, 350))  # Рисуем вариант 1
        window.blit(option2, (WIDTH // 2 - option2.get_width() // 2, 400))  # Рисуем вариант 2

        pygame.display.flip()  # Обновляем экран

        # Обработка событий меню
        for event in pygame.event.get():  # Получаем события
            if event.type == pygame.QUIT:  # Если нажали на крестик
                pygame.quit()  # Закрываем Pygame
                return False, 0  # Выходим

            if event.type == pygame.KEYDOWN:  # Если нажали клавишу
                if event.key == pygame.K_1:  # Если нажали '1'
                    # Меню выбора сложности
                    return show_difficulty_menu(window)  # Вызываем меню сложности и передаем окно
                elif event.key == pygame.K_2:  # Если нажали '2'
                    return True, 0  # Режим 2 игроков

    return True, 0  # Если что-то пошло не так

def show_difficulty_menu(window):  # Функция принимает окно в качестве аргумента
    """Меню выбора сложности."""
    difficulty_menu = True
    while difficulty_menu:
        window.fill('black')  # Заливаем экран черным

        # Отрисовка элементов меню сложности
        title = fontBig.render('УРОВЕНЬ СЛОЖНОСТИ', True, 'white')  # Заголовок
        easy = fontUI.render('1 - ЛЕГКИЙ', True, 'green')  # Легкий
        medium = fontUI.render('2 - СРЕДНИЙ', True, 'yellow')  # Средний
        hard = fontUI.render('3 - СЛОЖНЫЙ', True, 'red')  # Сложный

        window.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))  # Рисуем заголовок
        window.blit(easy, (WIDTH // 2 - easy.get_width() // 2, 300))  # Рисуем легкий
        window.blit(medium, (WIDTH // 2 - medium.get_width() // 2, 350))  # Рисуем средний
        window.blit(hard, (WIDTH // 2 - hard.get_width() // 2, 400))  # Рисуем сложный

        pygame.display.flip()  # Обновляем экран

        # Обработка выбора сложности
        for event in pygame.event.get():  # Получаем события
            if event.type == pygame.QUIT:  # Если нажали на крестик
                pygame.quit()  # Закрываем Pygame
                return False, 0  # Выходим

            if event.type == pygame.KEYDOWN:  # Если нажали клавишу
                if event.key == pygame.K_1:  # Если нажали '1'
                    return True, 1  # Легкий
                elif event.key == pygame.K_2:  # Если нажали '2'
                    return True, 2  # Средний
                elif event.key == pygame.K_3:  # Если нажали '3'
                    return True, 3  # Сложный