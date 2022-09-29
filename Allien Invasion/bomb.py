import pygame
from pygame.sprite import Sprite

class Bomb(Sprite):
    def __init__(self, ai_settings, screen):
        super(Bomb, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/bomb.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.y = float(self.rect.y)
        self.color = ai_settings.bomb_color

    def update(self):
        self.y += self.ai_settings.bomb_drop_speed_factor
        self.rect.y = self.y

    def draw_bomb(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
