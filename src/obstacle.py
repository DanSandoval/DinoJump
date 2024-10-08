# src/obstacle.py

import pygame
import random

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (139, 69, 19)  # Brown color for obstacles
        self.speed = 3  # Pixels per frame

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

def generate_obstacle(screen_width, ground_level):
    width = random.randint(20, 50)
    height = random.randint(30, 50)
    x = screen_width
    y = ground_level - height
    return Obstacle(x, y, width, height)