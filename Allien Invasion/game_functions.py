import sys
import pygame
import random
from bomb import Bomb
from bullet import Bullet
from alien import Alien
from time import sleep
from pygame import mixer

def check_bullet_bomb_collisions(ai_settings, screen, stats, sb, bullets, bombs):

    collisions = pygame.sprite.groupcollide(bullets, bombs, True, True)
    if collisions:
        for bombs in collisions.values():
            stats.score += ai_settings.alien_points * len(bombs)
            sb.prep_score()
            explosion_Sound = mixer.Sound('sound/explosion.wav')
            explosion_Sound.play()
        check_high_score(stats, sb)

    if len(bombs) == 0:
        create_bomb_fleet(ai_settings, screen, stats, bombs)

def create_bomb(ai_settings, screen, bombs, bomb_number):
    bomb = Bomb(ai_settings, screen)
    bomb.x = bomb_number *  100 + random.randint(1,800)
    bomb.rect.x = bomb.x
    bomb.y = 100 + random.randint(1,300)
    bomb.rect.y = bomb.y
    bombs.add(bomb)


def create_bomb_fleet(ai_settings, screen, stats, bombs):
    columns_bomb = stats.level + 1
    for bomb_number in range(columns_bomb):
        create_bomb(ai_settings, screen, bombs, bomb_number)

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            stats.reset_stats()
            stats.game_active = True
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
            aliens.empty()
            bullets.empty()
            create_fleet(ai_settings,screen,ship,aliens)
            ship.center_ship()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        laser = mixer.Sound("sound/laser.wav")
        laser.play()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_fleet_edges(ai_settings, aliens, screen, bombs):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens, screen, bombs)
            break


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, gameover):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, gameover)
            break


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            explosion = mixer.Sound("sound/explosion.wav")
            explosion.play()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        grandpa = pygame.image.load('images/grandpa.png')
        screen.blit(grandpa, (700, 50))
        pygame.display.flip()
        sleep(1)
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)




def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
    alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)


def change_fleet_direction(ai_settings, aliens, screen, bombs):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1



def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):

    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
    (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (3 * alien_height))
    return number_rows


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, gameover):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        if stats.ships_left == 0:
            stats.game_active = False

        # print("type sb:", type(sb))
        sb.prep_ships()


        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def ship_bomb_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, bombs, gameover):
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        if stats.ships_left == 0:
            stats.game_active = False
            pygame.mouse.set_visible(True)
        sb.prep_ships()
        aliens.empty()
        bombs.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(1)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, bombs, gameover):
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens, screen, bombs)
    """Update the positions of all aliens in the fleet."""
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, gameover)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, gameover)

def check_bombs_bottom(ai_settings, screen, bombs):
    screen_rect = screen.get_rect()

    for bomb in bombs.sprites():
        if bomb.rect.bottom >= screen_rect.bottom:
            bombs.remove(bomb)

def update_bombs(ai_settings, stats, screen, sb, ship, aliens, bullets, bombs, gameover):
    bombs.update()

    check_bullet_bomb_collisions(ai_settings, screen, stats, sb, bullets, bombs)

    check_bombs_bottom(ai_settings, screen, bombs)

    if pygame.sprite.spritecollideany(ship, bombs):
        ship_bomb_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, bombs, gameover)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # """
    # The sprite.groupcollide() method compares each bullet’s rect with each
    # alien’s rect and returns a dictionary containing the bullets and aliens that have collided
    # """
    # collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # if len(aliens) == 0:
    #     # Destroy existing bullets and create new fleet.
    #     bullets.empty()
    #     create_fleet(ai_settings, screen, ship, aliens)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, bombs, gameover):
    # screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    bombs.draw(screen)
    # sleep(0.001)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
        if stats.ships_left == 0:
            gameover.show_gameover()

    # Make the most recently drawn screen visible.
    pygame.display.flip()