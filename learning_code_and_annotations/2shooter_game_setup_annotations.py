# Import the pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# Typically, to call on keystrokes, mouse movements, or display attributes, you would need "pygame.K_UP", but if we import them, we can now use "K_UP" directly
# This is done for readability, reduce type in code, and DRY concepts
# See more here: https://www.pygame.org/docs/ref/locals.html
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Build our "canvas/surface"
# This surface represents the inside dimensions of the window
# The screen is going to be what we can control
    # The OS controls the windows borders and title bars
# Creates the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

# Main Loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

    # Background Color
    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Build a surface
    # Create a surface and pass in a tuple containing its length and width
    # Tuple is a python datatype (similar to List, but it is immutable)
    surf = pygame.Surface((50, 50))

    # Surface Color
    # Give the surface a color to separate it from the background
    # Here we filled it in with black
    surf.fill((0, 0, 0))
    # Access the underlying Rect with ".get_rect()"
    # We stored it as variable "rect" for later use
    rect = surf.get_rect()

    # USING A BLIT - PART 1

    # This line says "Draw our variable surf onto the screen at the center"
    # .blit(the_surface_to_draw, location_to_draw_on)

    # screen.blit(surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    # The above code line was commented out because it doesn't quite center the surf variable
    surf_center = (
        (SCREEN_WIDTH-surf.get_width())/2,
        (SCREEN_HEIGHT-surf.get_height())/2
    )
    screen.blit(surf, surf_center)

    # Updates the screen with everything that has been drawn since the last flip
    pygame.display.flip()
