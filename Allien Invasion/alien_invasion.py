import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf
from pygame import mixer
from gameover import Gameover

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    background = pygame.image.load('images/background.png')
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)


    go = Gameover(ai_settings, screen)
    bg_color = (230, 230, 230)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    bombs = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    gf.create_bomb_fleet(ai_settings, screen, stats, bombs)

    # Sound
    mixer.music.load("sound/background.wav")
    mixer.music.play(-1)


    while True:
        screen.blit(background, (0, 0))
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, bombs, go)
            gf.update_bombs(ai_settings, stats, screen, sb, ship, aliens, bullets, bombs, go)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, bombs, go)

        pygame.display.flip()

run_game()