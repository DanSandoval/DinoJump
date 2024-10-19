# src/main.py

import pygame
import sys
import os
from player import Dinosaur
from ground import Ground
from obstacle import Obstacle, generate_obstacle

def load_image(name):
    fullname = os.path.join('assets', 'images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f'Cannot load image: {fullname}')
        raise SystemExit(message)
    return image.convert_alpha()

def game_over_popup(screen):
    font = pygame.font.Font(None, 74)
    restart_text = font.render("Press R to Restart", True, (255, 0, 0))
    quit_text = font.render("Press Q to Quit", True, (255, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))
        screen.blit(restart_text, (500, 150))
        screen.blit(quit_text, (500, 250))
        pygame.display.flip()

def reset_game(dinosaur, obstacles):
    dinosaur.reset()
    obstacles.clear()

def main():
    while True:
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        WIDTH, HEIGHT = 1500, 400
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simple Dinosaur Platformer")

        # Clock for controlling frame rate
        clock = pygame.time.Clock()
        FPS = 60

        # Load assets
        dinosaur_image = load_image('dinosaur.png')
        ground_image = load_image('ground.png')

        # Create game objects
        ground = Ground(HEIGHT, ground_image)
        
        dinosaur_start_x = WIDTH * 0.1
        dinosaur_start_y = HEIGHT * 0.75

        dinosaur = Dinosaur(
            int(dinosaur_start_x),
            int(dinosaur_start_y),
            dinosaur_image
        )

        # Obstacle management
        obstacles = []
        obstacle_spawn_timer = 0
        obstacle_spawn_delay = 2700  # milliseconds

        # Game loop
        running = True
        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                dinosaur.handle_input(event, current_time)

            # Apply gravity
            gravity = 0.5
            dinosaur.apply_gravity(gravity)

            # Update dinosaur position
            dinosaur.update_position(ground.ground_level)

            # Spawn obstacles
            obstacle_spawn_timer += clock.get_time()
            if obstacle_spawn_timer > obstacle_spawn_delay:
                obstacles.append(generate_obstacle(WIDTH, ground.ground_level))
                obstacle_spawn_timer = 0

            # Update obstacles
            for obstacle in obstacles:
                obstacle.update()
                if dinosaur.collision_box.colliderect(obstacle.rect):
                    action = game_over_popup(screen)
                    if action == "restart":
                        running = False
                        break

            # Draw everything
            screen.fill((135, 206, 235))  # Light blue background
            ground.draw(screen)
            dinosaur.draw(screen)
            for obstacle in obstacles:
                obstacle.draw(screen)

            # Update display
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
