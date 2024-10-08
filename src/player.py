# src/player.py

import pygame

class Dinosaur:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = image
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collision_box = pygame.Rect(x, y, self.width * 0.6, self.height * 0.8)
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_charging_jump = False
        self.is_in_air = False
        self.jump_start_time = 0
        self.max_hold_time = 1000  # milliseconds
        self.min_hold_time = 100   # milliseconds
        self.max_jump_power = 25   # Adjust as needed

    def handle_input(self, event, current_time):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.is_in_air:
                self.is_charging_jump = True
                self.jump_start_time = current_time
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.is_charging_jump:
                self.initiate_jump(current_time)

    def initiate_jump(self, current_time):
        jump_duration = current_time - self.jump_start_time
        jump_duration = max(self.min_hold_time, min(jump_duration, self.max_hold_time))
        jump_power = (jump_duration - self.min_hold_time) / (self.max_hold_time - self.min_hold_time)
        self.velocity_y = -jump_power * self.max_jump_power
        self.velocity_x = jump_power * 10  # Adjust horizontal speed
        self.is_charging_jump = False
        self.is_in_air = True

    def apply_gravity(self, gravity):
        if self.is_in_air:
            self.velocity_y += gravity

    def update_position(self, ground_y):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Apply friction to horizontal movement
        if self.velocity_x > 0:
            self.velocity_x *= 0.9  # Adjust friction coefficient
            if self.velocity_x < 0.1:
                self.velocity_x = 0

        # Collision with ground
        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.velocity_y = 0
            self.is_in_air = False

        # Update rect and collision box positions
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.collision_box.x = int(self.x + (self.width * 0.2))
        self.collision_box.y = int(self.y + (self.height * 0.1))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        # Uncomment the line below to visualize the collision box (for debugging)
        # pygame.draw.rect(surface, (255, 0, 0), self.collision_box, 2)