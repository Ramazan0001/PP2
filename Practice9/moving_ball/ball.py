import pygame

def draw_ball(screen, x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius)


def move_left(x, radius, step):
    if x - radius - step >= 0:
        x -= step
    return x


def move_right(x, radius, step, WIDTH):
    if x + radius + step <= WIDTH:
        x += step
    return x


def move_up(y, radius, step):
    if y - radius - step >= 0:
        y -= step
    return y


def move_down(y, radius, step, HEIGHT):
    if y + radius + step <= HEIGHT:
        y += step
    return y