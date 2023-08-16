import pygame as pg
from pygame.sprite import Sprite
from settings import Settings

class Ship(Sprite):
    """ Класс корабля """
    def __init__(self, screen, settings):
        """ Инициализация корабля """
        super().__init__()
        self.screen = screen
        self.ai_settings = settings

        # Загрузка изображения
        self.image_default = pg.image.load(self.ai_settings.ship_name)
        self.image = pg.transform.scale(self.image_default, self.ai_settings.ship_size)
        self.rect = self.image.get_rect()

        self.screen_rect = screen.get_rect()
        # Появление корабля внизу в центре
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Сохранение вещественной кординаты корабля
        self.center = float(self.rect.centerx)

        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def blitme(self):
        """ Рисует корабля в текущей позиции """
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Размещает корабль в центре нижней стороны"""
        self.center = self.screen_rect.centerx
