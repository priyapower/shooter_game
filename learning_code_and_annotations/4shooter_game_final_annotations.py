import pygame
import random

from pygame.locals import (
    # RLEACCEL is the flag to denote Surface which is RLE encoded
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Loads an image from the disk
            # From custom file path
            # And converts for optimization for future .blit calls
        self.surf = pygame.image.load("media/jet.png").convert()
        # Sets a color that pygame will render as transparent (in this case white since the jet.png has a white background)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            # ADD SOUND TO PLAYER CLASS
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            # ADD SOUND TO PLAYER CLASS
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # Load missile image
        self.surf = pygame.image.load("media/missile.png").convert()
        # Set transparent background
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
           )
        )
        # RETURNED TO ORIGINAL VALUES
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("media/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 5)

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# INITIALIZE MIXER
# Setup for sounds. Defaults are good.
pygame.mixer.init()

pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, random.randint(250, 750))

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, random.randint(500, 1000))

# Create groups to hold enemy sprites, cloud sprites, and all sprites
player = Player()
enemies = pygame.sprite.Group()
# - clouds is used for position updates
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# LOAD THE MUSIC/SOUNDS
# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("media/Apoxode_-_Electric_1.mp3")
# loops=-1 tells it to loop the music and never end
pygame.mixer.music.play(loops=-1)

# Load all sound files for our effects
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("media/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("media/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("media/Collision.ogg")

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new cloud
        elif event.type == ADDCLOUD:
            # Create a new cloud object from Cloud Class
            new_cloud = Cloud()
            # Add this object to our clouds group
            clouds.add(new_cloud)
            # Add this object to our all_sprites group
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        # ADD COLLISION SOUND
        # Stop any moving sounds
        move_up_sound.stop()
        move_down_sound.stop()
        # And play the collision sound
        collision_sound.play()

        player.kill()
        running = False

    pygame.display.flip()

    # Ensure program maintains a rate of 45 frames per second
    clock.tick(45)

# END ALL SOUND
# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()
