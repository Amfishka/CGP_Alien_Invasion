""" Модуль для хранения всех настроек """
class Settings():
    """ Класс для хранения настроек в игре """
    def __init__(self):
        # Размеры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_size = (self.screen_width, self.screen_height)
        # Цвет основного фона
        self.bg_color = (230, 230, 230)
        # Название окна
        self.caption = "Alien Invasion"
        # Корабль
        self.ship_name = "assets/ship/spaceShips_001.png"
        self.ship_size = (66, 66)
        self.ship_limit = 3
        # Параметры выстрела
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3
        # Пришелец
        self.alien_name = "assets/aliens/alien.png"
        self.alien_size = (80, 80)
        self.fleet_drop_speed = 10
        # Темп ускорения игры
        self.speedup_scale = 1.1
        self.initialize_dinamic_settings()

    def initialize_dinamic_settings(self):
        """ Инициализирует настройки меняющиеся в ходе игры """
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction = 1 обозначает движение вправо, -1 влево
        self.fleet_direction = 1
        self.alien_point = 50
    
    def increase_speed(self):
        """ Увеличение настроек скорости """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_point *= self.speedup_scale