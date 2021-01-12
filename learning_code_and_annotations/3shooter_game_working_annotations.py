import pygame
# Import the random module from Python for random numbers
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define a Player Object
    # It extends from Sprite class with pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of the "player"
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # super (https://www.w3schools.com/python/ref_func_super.asp)
        # This is used for Inheritance
        # In this case,, it is so we can use the method "__init__()" from Sprite Class
        super(Player, self).__init__()
        # Create a variable on self called surf
        # define surf as a Surface with length and width of 75
        self.surf = pygame.Surface((75, 25))
        # Fill the surface object as White
        self.surf.fill((255, 255, 255))
        # Create a rect variable for later use
        self.rect = self.surf.get_rect()

    # This method is defining how the player object moves based on keystrokes
    # This takes in pressed_keys (which is defined in the game loop)
    def update(self, pressed_keys):
        # Every key stroke will go through this method, but only land on 1 if-block
        if pressed_keys[K_UP]:
            # .move_ip is move in place and moves according to the current .rect of the object
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        # This is a safeguard to prevent a player object from exiting the screen
            # Only obstacles should be able to leave the screen
            # It basically checks all the sides (left, right, top, bottom) and either resets them to to 0 or resets them to the variables for screen width and height
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # initialize the class as a Sprite
        super(Enemy, self).__init__()
        # build a surface object
        self.surf = pygame.Surface((20, 10))
        # Color it white
        self.surf.fill((255, 255, 255))
        # Define it's .rect
        self.rect = self.surf.get_rect(
            # Math for creating a random generation of the Enemy
            # you update rect to be a random location along the right edge of the screen. The center of the rectangle is just off the screen. It’s located at some position between 20 and 100 pixels away from the right edge, and somewhere between the top and bottom edges.
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
           )
        )
        # Sets the speed using a randomizer (how fast the enemy moves towards the player)
        self.speed = random.randint(3, 7)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    # This only takes self since the enemies move on their own
    def update(self):
        # Makes the enemy object move left on the screen based on it's set (random) speed
        self.rect.move_ip(-self.speed, 0)
        # If the enemy object moves off screen (the right side of the .rext has gone past the left side of the screen)
        if self.rect.right < 0:
            # .kill will prevent this enemy object from being processed further
            self.kill()

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
# Pygame defines events using integers, so the following code calls on the last pygame event saved (USEREVENT) and adds 1 to ensure a unique id
ADDENEMY = pygame.USEREVENT + 1
# This inserts the new event at regular intervals (250 milliseconds, or 4 times in a second)
pygame.time.set_timer(ADDENEMY, random.randint(250, 600)) # What would this look like if randomized?

# Instantiate a player from the Player Class
    # For now, the player is just a white rectangle
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
enemies = pygame.sprite.Group()
# - all_sprites is used for rendering
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        # UPDATE EVENT LOOP WITH CUSTOM EVENT
        # Add a new enemy
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position for the enemies group
    enemies.update()

    # Filling the window screen as Black
    screen.fill((0, 0, 0))

    # Draw the player on the screen
    # Copy the player surface onto the screen
        # screen.blit(player.surf, player.rect)
        # screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # ADD COLLIDER LOGIC
    # Check if any enemies have collided with the player
        # our .spritecollideany is taking on 2 args: player and enemies
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False

    pygame.display.flip()
