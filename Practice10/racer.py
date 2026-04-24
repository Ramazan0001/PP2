import pygame
import sys
import random

pygame.init()

# FPS means how many frames per second the game will run
FPS = 60
clock = pygame.time.Clock()

# Colors in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Practice 10 Racer")

# Game speed
SPEED = 5

# Score and collected coins
SCORE = 0
COINS = 0

# Fonts for text
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# Load images
background = pygame.image.load("PP/Practice10/images/AnimatedStreet.png")
player_img = pygame.image.load("PP/Practice10/images/Player.png")
enemy_img = pygame.image.load("PP/Practice10/images/Enemy.png")

# Load crash sound
crash_sound = pygame.mixer.Sound("PP/Practice10/images/crash.wav")

# Game Over text
game_over_text = font.render("Game Over", True, BLACK)

# Player position
player_rect = player_img.get_rect()
player_rect.center = (160, 520)

# Enemy position
enemy_rect = enemy_img.get_rect()
enemy_rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Coin
coin_size = 20
coin_rect = pygame.Rect(0, 0, coin_size, coin_size)
coin_rect.center = (random.randint(40, SCREEN_WIDTH - 40), -20)

# This variable shows whether the game is over or not
game_over = False


# Function for resetting enemy position
def reset_enemy():
    global enemy_rect

    enemy_rect.top = 0
    enemy_rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Function for resetting coin position
def reset_coin():
    global coin_rect

    coin_rect.top = -20
    coin_rect.center = (random.randint(40, SCREEN_WIDTH - 40), -20)


# Function for restarting the whole game
def reset_game():
    global SPEED, SCORE, COINS, game_over
    global player_rect, enemy_rect, coin_rect

    SPEED = 5
    SCORE = 0
    COINS = 0
    game_over = False

    # Reset player position
    player_rect.center = (160, 520)

    # Reset enemy and coin
    reset_enemy()
    reset_coin()


# Main game loop
while True:

    # Check all events
    for event in pygame.event.get():

        # If player closes the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # If game is over, press R to restart
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

    # Draw background
    screen.blit(background, (0, 0))

    # If game is not over, update the game
    if not game_over:

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Move player left
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.move_ip(-5, 0)

        # Move player right
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.move_ip(5, 0)

        # Move enemy down
        enemy_rect.move_ip(0, SPEED)

        # If enemy goes below the screen, reset it
        if enemy_rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            reset_enemy()

        # Move coin down
        coin_rect.move_ip(0, SPEED)

        # If coin goes below the screen, reset it
        if coin_rect.top > SCREEN_HEIGHT:
            reset_coin()

        # Check collision between player and enemy
        if player_rect.colliderect(enemy_rect):
            crash_sound.play()
            game_over = True

        # Check collision between player and coin
        if player_rect.colliderect(coin_rect):
            COINS += 1
            reset_coin()

        # Draw player car
        screen.blit(player_img, player_rect)

        # Draw enemy car
        screen.blit(enemy_img, enemy_rect)

        # Draw coin as yellow circle
        pygame.draw.circle(screen, YELLOW, coin_rect.center, coin_size // 2)

    # If game is over
    else:
        screen.fill(RED)

        # Draw Game Over text
        screen.blit(game_over_text, (30, 250))

        # Draw restart instruction
        restart_text = font_small.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (100, 320))

    # Create score text
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)

    # Create coin text
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)

    # Draw score in the top-left corner
    screen.blit(score_text, (10, 10))

    # Draw coins in the top-right corner
    screen.blit(coin_text, (280, 10))

    # Update display
    pygame.display.update()

    # Limit game speed to 60 FPS
    clock.tick(FPS)