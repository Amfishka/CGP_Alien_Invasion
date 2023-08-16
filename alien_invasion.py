import pygame as pg
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
import game_functions as gf
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Инициализация игры и создание объекта экрана
    pg.init()
    ai_settings = Settings()
    screen = pg.display.set_mode(ai_settings.screen_size)
    pg.display.set_caption(ai_settings.caption)
    # Создвние кнопки PLAY
    play_button = Button(ai_settings, screen, "Play")
    # Создание экземпляра для хранения статистики игры
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Создание корабля
    ship = Ship(screen, ai_settings)
    # Создание группы для хранения пуль
    bullets = Group()
    # Создание флота пришельцев
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)


    # Запуск основного цикла игры
    while True:
        # Отслеживание событий клавиатуры и мыши
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            # Обновление корабля
            ship.update()
            # Обновление пуль
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # Обновление пришельцев
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        # Перерисовка экрана
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        # Отображение последнего прорисованного экрана
        pg.display.flip()

run_game()
            