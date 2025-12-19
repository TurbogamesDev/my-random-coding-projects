# Example file showing a basic platformer game loop with Pygame
import pygame

from clock import clock
from screen import screen

# Initialize Pygame modules
pygame.init()

pygame.display.set_caption("Platformer Game")

# Boolean to keep the game running
running = True

# Get all currently pressed keys (not used in this example)
keys = pygame.key.get_pressed()

# Define the platform rectangle (position and dimensions) 
ground_rect = pygame.Rect(0, 600, 1280, 120)

# Define the player rectangle's starting position and side length
player_side_length = 64
player_rect = pygame.Rect(608, 88, player_side_length, player_side_length)

# Define starting vertical velocity, gravity, and speed
player_y_velocity = 0
player_x_velocity = 0
gravity = 0.5
speed = 5
movement_acceleration = 0.35

while running:
    # Check for user quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Check for collisions and stop movement if colliding
    # With ground
    if player_rect.colliderect(ground_rect):
        player_rect.y = ground_rect.y - player_side_length
        player_y_velocity = 0  # Reset velocity on collision
    
    # Check for key input
    keys = pygame.key.get_pressed()
    # Handle jumping with space key only when on ground/platform
    if keys[pygame.K_SPACE] and player_rect.y == ground_rect.y - player_side_length:
        player_y_velocity = -15
        print("Jump!")  # Print jump message for debugging
    # Handle left/right movement
    direction = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    # Make the player move if stationary
    if direction == 1 and player_x_velocity < speed:
        player_x_velocity += movement_acceleration
        if player_x_velocity > speed:
            player_x_velocity = speed
    if direction == -1 and player_x_velocity > -speed:
        player_x_velocity -= movement_acceleration
        if player_x_velocity < -speed:
            player_x_velocity = -speed
    # Make the player stop if moving
    if direction == 0:
        if player_x_velocity > 0:
            player_x_velocity -= movement_acceleration
            if player_x_velocity < 0:
                player_x_velocity = 0
        elif player_x_velocity < 0:
            player_x_velocity += movement_acceleration
            if player_x_velocity > 0:
                player_x_velocity = 0
    
    # Fill the screen with a background color
    screen.fill((128, 255, 255))  # Light blue background

    # Render game objects
    # Draw the platform rectangle
    pygame.draw.rect(screen, (0, 192, 0), ground_rect)
    # Draw the player rectangle
    pygame.draw.rect(screen, (255, 0, 0), player_rect)

    # Update player position based on velocity and gravity
    player_rect.x += player_x_velocity
    player_rect.y += player_y_velocity
    player_y_velocity += gravity
    
    # Update the display with all drawn objects
    pygame.display.flip()

    # Limit the game loop to 60 FPS
    clock.tick(60)

# Quit Pygame when done
pygame.quit()