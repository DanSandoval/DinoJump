# src/ground.py

import pygame

class Ground:
    def __init__(self, screen_height, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottom = screen_height
        self.ground_level = int(screen_height * 0.86)  # 80% down the screen

    def draw(self, surface):
        surface.blit(self.image, self.rect)