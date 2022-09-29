import pygame.font
from pygame.sprite import Group

class Gameover():
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.text_color = (255, 0, 00)
        self.font = pygame.font.SysFont(None, 96)
        self.prep_gameover()

    def prep_gameover(self):
        self.gameover_image = self.font.render("Game over", True, self.text_color, None)
        self.score_rect = self.gameover_image.get_rect()
        self.gameover_rect = self.gameover_image.get_rect()
        self.gameover_rect.centerx = self.screen_rect.centerx
        self.gameover_rect.top = self.screen_rect.top + 400

    def show_gameover(self):
        self.screen.blit(self.gameover_image, self.gameover_rect)

