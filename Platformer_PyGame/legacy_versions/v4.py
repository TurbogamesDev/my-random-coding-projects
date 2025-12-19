# Initialization stuff
import pygame
pygame.init()

## fix other windows resizing
# video_info = pygame.display.Info()
# print(video_info.current_w, video_info.current_h)
surface = pygame.display.set_mode((640, 360), pygame.RESIZABLE)
surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
fullscreen = True
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()
running = True

# Define the classes
# Platform class
class platform_class(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        pygame.Rect.__init__(self, x, y, width, height)

    def draw(self, screen, cam):
        pygame.draw.rect(screen, self.color, (self.x - (cam.x - cam.x_off), self.y - (cam.y - cam.y_off), self.width, self.height))

# Player class
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

    def draw(self, screen, cam):
        pygame.draw.rect(screen, self.color, (self.x - (cam.x - cam.x_off), self.y - (cam.y - cam.y_off), self.width, self.height))

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

# Camera class
class camera_class():
    def __init__(self, x, y, x_off, y_off):
        self.x = x
        self.y = y
        self.x_off = x_off
        self.y_off = y_off

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
platforms_rect = []
platforms_rect.append(platform_class(0, 600, 1280, 120, [0, 192, 0])) # Ground
# platforms_rect.append(platform_class(320, 360, 240, 60, [0, 0, 0]))
# platforms_rect.append(platform_class(320, 140, 320, 60, [0, 0, 0]))
for i in range(10):
    platforms_rect.append(platform_class(320, 360 - (240 * i), 240, 60, [0, 0, 0]))

# Define the player
player = player_class(608, 88, 64, 64, [255, 0, 0], 0, 0, 8, 0.65, -22.5)

# Define the camera
camera = camera_class(0, 0, 608, 328)

# World variables
gravity = 0.75

while running:
    # Check for user quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                if fullscreen:
                    pygame.display.toggle_fullscreen()
                    surface = pygame.display.set_mode((640, 360), pygame.RESIZABLE)
                    fullscreen = False
                else:
                    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    fullscreen = True

    
    camera.x_off = (surface.get_width() - player.width) / 2
    camera.y_off = (surface.get_height() - player.height) / 2

    check_key_input(player)

    # Fill the screen with a background color
    surface.fill((128, 255, 255))  # Light blue background

    # Render game objects
    # Draw the platforms
    for i in platforms_rect:
        i.draw(surface, camera)
    # Draw the player rectangle
    player.draw(surface, camera)
    
    # Update player position based on velocity and gravity and collisions
    player.x += player.x_vel
    player.adjust_for_collision("x")
    player.y += player.y_vel
    player.adjust_for_collision("y")
    player.y_vel += gravity
    
    # Make camera follow the player
    camera.x = player.x
    camera.y = player.y
    if camera.y > camera.y_off - ((surface.get_height() - 720)):
        camera.y = camera.y_off - ((surface.get_height() - 720))

    # print(camera.x, camera.y, camera.x_off, camera.y_off)

    # Update the display with all drawn objects
    pygame.display.flip()

    # Limit the game loop to 60 FPS
    ## make lowering this not slow down the game
    clock.tick(60)

# Quit Pygame when done
pygame.quit()