# Example file showing a basic platformer game loop with Pygame
import pygame

# Initialize Pygame modules
pygame.init()

# Set the screen size and caption
surface = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Platformer Game")

# Create a clock object to control FPS
clock = pygame.time.Clock()

# Boolean to keep the game running
running = True

# Define the platforms
class platform(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        pygame.Rect.__init__(self, x, y, width, height)
    def draw_platform(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

platforms_rect = []
platforms_rect.append(platform(0, 600, 1280, 120, [0, 192, 0])) # Ground
platforms_rect.append(platform(320, 360, 240, 60, [0, 0, 0]))
platforms_rect.append(platform(640, 180, 320, 60, [0, 0, 0]))

# Define the player rectangle's starting position and side length
player_side_length = 64
player_rect = pygame.Rect(608, 88, player_side_length, player_side_length)

# Define starting vertical velocity, gravity, and speed
player_y_velocity = 0
player_x_velocity = 0
gravity = 0.65
speed = 8
movement_acceleration = 0.35

while running:
    # Check for user quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Check for key input
    keys = pygame.key.get_pressed()
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
    surface.fill((128, 255, 255))  # Light blue background

    # Render game objects
    # Draw the platforms
    for i in platforms_rect:
        i.draw_platform(surface)
    # Draw the player rectangle
    pygame.draw.rect(surface, (255, 0, 0), player_rect)
    
    # Update player position based on velocity and gravity and collisions
    ## also make this work with lists/tuples
    player_rect.x += player_x_velocity
    if player_rect.collidelist(platforms_rect) > -1:
        if player_x_velocity > 0:
            while player_rect.collidelist(platforms_rect) > -1:
                player_rect.x -= 1
        elif player_x_velocity < 0:
            while player_rect.collidelist(platforms_rect) > -1:
                player_rect.x += 1
    player_rect.y += player_y_velocity
    if player_rect.collidelist(platforms_rect) > -1:
        if player_y_velocity > 0:
            player_y_velocity = 0
            if keys[pygame.K_SPACE]:
                player_y_velocity = -20
                print("Jump!")  # Print jump message for debugging
            while player_rect.collidelist(platforms_rect) > -1:
                player_rect.y -= 1
        elif player_y_velocity < 0:
            player_y_velocity *= -0.8
            while player_rect.collidelist(platforms_rect) > -1:
                player_rect.y += 1
    player_y_velocity += gravity
    
    # Update the display with all drawn objects
    pygame.display.flip()

    # Limit the game loop to 60 FPS
    clock.tick(60)

# Quit Pygame when done
pygame.quit()