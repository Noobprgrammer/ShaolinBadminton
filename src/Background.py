import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game Window")

# Load and scale background
background = pygame.image.load(r"C:\Users\User\Downloads\Assignment Y2S2\ISE Assignment\ISE Git\ShaolinBadminton\Assests\Background\Background1\Background1.jpg")  # Use your actual file path
background = pygame.transform.scale(background, (screen_width, screen_height))  # Fit the window size

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.blit(background, (0, 0))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()