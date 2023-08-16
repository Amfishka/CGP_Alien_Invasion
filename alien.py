import pygame as pg
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Класс представляющий одного пришельца"""

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения пришельца
        self.image_default = pg.image.load(self.ai_settings.alien_name)
        self.image = pg.transform.scale(self.image_default, self.ai_settings.alien_size)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в верхнем левом углу экрана
        self.rect.x = self.rect.width // 2
        self.rect.y = self.rect.height // 2

        # Сохранение точной позиции пришельца
        self.x = float(self.rect.x)

    def blitme(self):
        """ Выводит пришельца в текущем положении """
        self.screen.blit(self.image, self.rect)
    
    def check_edges(self):
        """ Возвращает True если пришелец находится у края экрана """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    def update(self):
        """ Перемещает пришеьлца """
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x