import pygame
import math

# Initialize pygame
pygame.init()

# Window size
WIDTH, HEIGHT = 800, 600

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Practice 11")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fill background with white color
screen.fill(WHITE)

# Clock controls FPS
clock = pygame.time.Clock()

# Current drawing color
color = BLACK

# Brush radius
radius = 5

# Current drawing mode
mode = "draw"

# Checks if mouse button is pressed
drawing = False

# Start position for shapes
start_pos = None


# Function for filling closed area with selected color
def flood_fill(surface, start_pos, new_color):
    # Get color of the clicked pixel
    old_color = surface.get_at(start_pos)

    # Convert new color to pygame Color
    new_color = pygame.Color(new_color)

    # If clicked area already has this color, do nothing
    if old_color == new_color:
        return

    # List of pixels that we need to check
    pixels = [start_pos]

    while pixels:
        x, y = pixels.pop()

        # Check if pixel is inside the screen
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            continue

        # If current pixel has the old color, change it
        if surface.get_at((x, y)) == old_color:
            surface.set_at((x, y), new_color)

            # Add neighbour pixels
            pixels.append((x + 1, y))
            pixels.append((x - 1, y))
            pixels.append((x, y + 1))
            pixels.append((x, y - 1))


# Main loop variable
running = True

# Main program loop
while running:

    # Check all events
    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            # Color selection
            if event.key == pygame.K_1:
                color = BLACK

            if event.key == pygame.K_2:
                color = RED

            if event.key == pygame.K_3:
                color = GREEN

            if event.key == pygame.K_4:
                color = BLUE

            # Brush mode
            if event.key == pygame.K_d:
                mode = "draw"

            # Eraser mode
            if event.key == pygame.K_e:
                mode = "eraser"

            # Fill mode
            if event.key == pygame.K_f:
                mode = "fill"

            # Circle mode
            if event.key == pygame.K_c:
                mode = "circle"

            # Rectangle mode
            if event.key == pygame.K_r:
                mode = "rect"

            # Square mode
            if event.key == pygame.K_s:
                mode = "square"

            # Right triangle mode
            if event.key == pygame.K_t:
                mode = "right_triangle"

            # Equilateral triangle mode
            if event.key == pygame.K_q:
                mode = "equilateral_triangle"

            # Rhombus mode
            if event.key == pygame.K_h:
                mode = "rhombus"

        # Mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            # If fill mode is selected, fill clicked area immediately
            if mode == "fill":
                flood_fill(screen, event.pos, color)
                drawing = False

        # Mouse button released
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            # Draw circle
            if mode == "circle":
                dx = x2 - x1
                dy = y2 - y1

                # Radius is distance between start point and end point
                radius_circle = int((dx ** 2 + dy ** 2) ** 0.5)

                pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

            # Draw rectangle
            if mode == "rect":
                rect = pygame.Rect(
                    min(x1, x2),
                    min(y1, y2),
                    abs(x2 - x1),
                    abs(y2 - y1)
                )

                pygame.draw.rect(screen, color, rect, 2)

            # Draw square
            if mode == "square":
                # Square has equal width and height
                size = min(abs(x2 - x1), abs(y2 - y1))

                # Choose correct x position
                if x2 < x1:
                    draw_x = x1 - size
                else:
                    draw_x = x1

                # Choose correct y position
                if y2 < y1:
                    draw_y = y1 - size
                else:
                    draw_y = y1

                pygame.draw.rect(screen, color, (draw_x, draw_y, size, size), 2)

            # Draw right triangle
            if mode == "right_triangle":
                # Right triangle has one 90 degree angle
                points = [
                    (x1, y1),
                    (x1, y2),
                    (x2, y2)
                ]

                pygame.draw.polygon(screen, color, points, 2)

            # Draw equilateral triangle
            if mode == "equilateral_triangle":
                # Side length
                side = abs(x2 - x1)

                # Height formula for equilateral triangle
                triangle_height = int(side * math.sqrt(3) / 2)

                # If mouse is dragged down
                if y2 > y1:
                    points = [
                        (x1, y1 + triangle_height),
                        (x1 + side // 2, y1),
                        (x1 + side, y1 + triangle_height)
                    ]

                # If mouse is dragged up
                else:
                    points = [
                        (x1, y1 - triangle_height),
                        (x1 + side // 2, y1),
                        (x1 + side, y1 - triangle_height)
                    ]

                pygame.draw.polygon(screen, color, points, 2)

            # Draw rhombus
            if mode == "rhombus":
                # Center of the selected area
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Rhombus has 4 points: top, right, bottom, left
                points = [
                    (center_x, y1),
                    (x2, center_y),
                    (center_x, y2),
                    (x1, center_y)
                ]

                pygame.draw.polygon(screen, color, points, 2)

        # Mouse movement
        if event.type == pygame.MOUSEMOTION:

            # Draw with brush
            if drawing and mode == "draw":
                pygame.draw.circle(screen, color, event.pos, radius)

            # Eraser draws white circles
            if drawing and mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, radius + 10)

    # Update screen
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

# Quit pygame
pygame.quit()