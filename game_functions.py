import sys
from time import sleep
import pygame as pg
from bullet import Bullet
from alien import Alien



def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ Отслеживание событий """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pg.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
 bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
 bullets, mouse_x, mouse_y):
    """ Запускает новую игру при нажатии кнопки """
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        ai_settings.initialize_dinamic_settings()
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
        

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    pg.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    if event.key == pg.K_RIGHT:
        ship.moving_right = True
    if event.key == pg.K_LEFT:
        ship.moving_left = True
    if event.key == pg.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pg.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
    if event.key == pg.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pg.K_RIGHT:
        ship.moving_right = False
    if event.key == pg.K_LEFT:
        ship.moving_left = False

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """ Обновляет изображения на экране и отображает новый экран """
    # Перерисовка экрана при каждом проходе цикла
    screen.fill(ai_settings.bg_color)
    # Отрисовка пуль
    for bullet in bullets:
        bullet.draw_bullet()
    # Отрисовка корабля
    ship.blitme()
    # Отображение пришельца
    aliens.draw(screen)
    sb.show_score()
    # Кнопка Play
    if not stats.game_active:
        play_button.draw_button()
    # Отображение последнего отрисованного экрана
    pg.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Обновление позиции пуль и Удаление пуль вышедших за край экрана"""
    # Обновление позиции
    bullets.update()
    # Удаление пуль вышедших за край экрана
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
    #Проверка на попадание
    check_bullet_aliens_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    

def check_bullet_aliens_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Обработка коллизии пуль с пришельцами """
    collisions = pg.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += int(ai_settings.alien_point) * len(aliens)
            check_high_score(stats, sb)
            sb.prep_score()
           
    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота
        stats.level += 1
        sb.prep_level()
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """ Создание пули и включение её в группу bullets """
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """ Создаёт флот пришельцев """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    """ Вычисляет количество пришельцев в ряду """
    available_space_x = ai_settings.screen_width - alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """ Определяет количество рядов с пришельцами"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Создаёт пришельца и размещает его в ряду """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
    """ Реагирует на достижение пришеьлцем края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """ Опускает весь флот и меняет напрвление движения"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """ Обработка столкновения корабля с пришельцем"""
    # Уменьшение количества кораблей
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()
        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pg.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """ Проверяет добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """ Обновлениие позиции всех пришельцев во флоте """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка коллизии пришельцев и корабля
    if pg.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

def check_high_score(stats, sb):
    """ Проверяет, появился ли новый рекорд """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
