# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
# .display is a pygame module that lets you control the display window and screen
# .set_mode is a pygame function that initializes a window/screen for display
# We have a size argument [500, 500]. A size argument is a pair of numbers representing the width and height.
screen = pygame.display.set_mode([500, 500])

# This following sets up a GAME LOOP
# Run until the user asks to quit
running = True
while running:

    # This "for" section scans and handles events
    # Did the user click the window close button?
    # event is a pygame module that interacts with events and queues
    # .get will get events from the queue
    for event in pygame.event.get():
        # is a user triggers the quit event
        if event.type == pygame.QUIT:
            # stop running the program
            running = False

    # Fill the background with white
    # (255, 255, 255) = White for RGB
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    # (255, 255, 255) = Dark Blue for RGB
    # .draw is a pygame module for drawing shapes
    # .circle draws a circle
    # .circle(a, b, c, d)
    # a = screen = surface to draw on
    # b = (0, 0, 250) = color to draw with
    # c = (250, 250) = center (since our screen is 500, 500, this means our center of the circle is the center of the screen)
    # d = 75 = width of the circle
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Without this code, nothing would appear in our window
    # Flip the display
    # .flip = Update the full display Surface to the screen
    pygame.display.flip()

# This happens once the loop is completed
# Done! Time to quit.
pygame.quit()
