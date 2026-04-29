import pygame
from collections import deque


def get_rect(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos

    x = min(x1, x2)
    y = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return pygame.Rect(x, y, width, height)


def draw_rectangle(surface, color, start_pos, end_pos, brush_size):
    rect = get_rect(start_pos, end_pos)
    pygame.draw.rect(surface, color, rect, brush_size)


def draw_circle(surface, color, start_pos, end_pos, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    radius_x = abs(x2 - x1) // 2
    radius_y = abs(y2 - y1) // 2

    radius = min(radius_x, radius_y)

    if radius > 0:
        pygame.draw.circle(surface, color, (center_x, center_y), radius, brush_size)


def draw_square(surface, color, start_pos, end_pos, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x = x1 - side
    else:
        x = x1

    if y2 < y1:
        y = y1 - side
    else:
        y = y1

    rect = pygame.Rect(x, y, side, side)
    pygame.draw.rect(surface, color, rect, brush_size)


def draw_right_triangle(surface, color, start_pos, end_pos, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, brush_size)


def draw_equilateral_triangle(surface, color, start_pos, end_pos, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    middle_x = (left + right) // 2

    points = [
        (middle_x, top),
        (left, bottom),
        (right, bottom)
    ]

    pygame.draw.polygon(surface, color, points, brush_size)


def draw_rhombus(surface, color, start_pos, end_pos, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    middle_x = (left + right) // 2
    middle_y = (top + bottom) // 2

    points = [
        (middle_x, top),
        (right, middle_y),
        (middle_x, bottom),
        (left, middle_y)
    ]

    pygame.draw.polygon(surface, color, points, brush_size)


def flood_fill(surface, start_pos, new_color):
    width, height = surface.get_size()

    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    old_color = surface.get_at((x, y))
    fill_color = pygame.Color(new_color[0], new_color[1], new_color[2], 255)

    if old_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        cx, cy = queue.popleft()

        if cx < 0 or cx >= width or cy < 0 or cy >= height:
            continue

        if surface.get_at((cx, cy)) != old_color:
            continue

        surface.set_at((cx, cy), fill_color)

        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))