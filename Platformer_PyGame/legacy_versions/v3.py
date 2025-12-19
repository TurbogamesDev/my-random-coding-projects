# Initialization stuff
import pygame
pygame.init()

## add fullscreen support
surface = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()
running = True

# Define the classes
class platform_class(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        pygame.Rect.__init__(self, x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class player_class(pygame.Rect):
    def __init__(self, x, y, width, height, color, x_vel, y_vel, speed, move_acc, jump_power):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.speed = speed
        self.move_acc = move_acc
        self.jump_power = jump_power
        pygame.Rect.__init__(self, x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def adjust_for_collision(self, direction):
        keys = pygame.key.get_pressed()
        if direction == "x":
            if self.collidelist(platforms_rect) > -1:
                if self.x_vel > 0:
                    while self.collidelist(platforms_rect) > -1:
                        self.x -= 1
                elif self.x_vel < 0:
                    while self.collidelist(platforms_rect) > -1:
                        self.x += 1
        elif direction == "y":
            if self.collidelist(platforms_rect) > -1:
                if self.y_vel > 0:
                    self.y_vel = 0
                    if keys[pygame.K_SPACE]:
                        self.y_vel = self.jump_power
                        print("Jump!")  # Print jump message for debugging
                    while self.collidelist(platforms_rect) > -1:
                        self.y -= 1
                elif self.y_vel < 0:
                    self.y_vel *= -0.8
                    while self.collidelist(platforms_rect) > -1:
                        self.y += 1

## make a camera class

# Define the functions
# Check for key input
def check_key_input(plr):
    keys = pygame.key.get_pressed()
    # Handle left/right movement
    direction = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    # Make the player move if stationary
    if direction == 1 and plr.x_vel < plr.speed:
        plr.x_vel += plr.move_acc
        if plr.x_vel > plr.speed:
            plr.x_vel = plr.speed
    if direction == -1 and plr.x_vel > -plr.speed:
        plr.x_vel -= plr.move_acc
        if plr.x_vel < -plr.speed:
            plr.x_vel = -plr.speed
    # Make the player stop if moving
    if direction == 0:
        if plr.x_vel > 0:
            plr.x_vel -= plr.move_acc
            if plr.x_vel < 0:
                plr.x_vel = 0
        elif plr.x_vel < 0:
            plr.x_vel += plr.move_acc
            if plr.x_vel > 0:
                plr.x_vel = 0

# Define the platforms
## add scaling whenever fullscreen supports get added
platforms_rect = []
platforms_rect.append(platform_class(0, 600, 1280, 120, [0, 192, 0])) # Ground
platforms_rect.append(platform_class(320, 360, 240, 60, [0, 0, 0]))
platforms_rect.append(platform_class(320, 140, 320, 60, [0, 0, 0]))

# Define the player
player = player_class(608, 88, 64, 64, [255, 0, 0], 0, 0, 8, 0.65, -22.5)

# World variables
gravity = 0.75

while running:
    # Check for user quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    check_key_input(player)

    # Fill the screen with a background color
    surface.fill((128, 255, 255))  # Light blue background

    # Render game objects
    # Draw the platforms
    for i in platforms_rect:
        i.draw(surface)
    # Draw the player rectangle
    player.draw(surface)
    
    # Update player position based on velocity and gravity and collisions
    player.x += player.x_vel
    player.adjust_for_collision("x")
    player.y += player.y_vel
    player.adjust_for_collision("y")
    player.y_vel += gravity
    
    # Update the display with all drawn objects
    pygame.display.flip()

    # Limit the game loop to 60 FPS
    ## make lowering this not slow down the game
    clock.tick(60)

# Quit Pygame when done
pygame.quit()