import pygame
from ball import *

pygame.init()

WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
RED = (255, 0, 0)

x = WIDTH // 2
y = HEIGHT // 2
radius = 25
step = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x = move_left(x, radius, step)

            elif event.key == pygame.K_RIGHT:
                x = move_right(x, radius, step, WIDTH)

            elif event.key == pygame.K_UP:
                y = move_up(y, radius, step)

            elif event.key == pygame.K_DOWN:
                y = move_down(y, radius, step, HEIGHT)

    draw_ball(screen, x, y, radius, RED)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()