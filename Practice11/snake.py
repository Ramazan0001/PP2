import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 600, 600

# Size of one cell in the grid
CELL = 20


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")

# Clock controls the game speed
clock = pygame.time.Clock()


font = pygame.font.SysFont("Verdana", 20)


snake = [(100, 100)]


dx, dy = CELL, 0


score = 0


level = 1


speed = 10


POINTS_FOR_NEXT_LEVEL = 4


FOOD_LIFETIME = 5000


food_weight = 1

# Time when food appeared
food_spawn_time = pygame.time.get_ticks()



def generate_food():
    global food_weight, food_spawn_time

    while True:
        # Generate random x and y position according to the grid
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        
        if (x, y) not in snake:

           
            food_weight = random.choice([1, 2, 3])

           
            food_spawn_time = pygame.time.get_ticks()

            return (x, y)



def get_food_color(weight):
    # Weight 1 food gives 1 point
    if weight == 1:
        return (255, 0, 0)       # red

    # Weight 2 food gives 2 points
    if weight == 2:
        return (255, 255, 0)     # yellow

    # Weight 3 food gives 3 points
    return (0, 150, 255)         # blue



food = generate_food()

# Main game variable
running = True


while running:

    
    for event in pygame.event.get():

      
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:

            # Move up only if snake is not moving vertically
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL

           
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL

            
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0

            
            if event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0

    # Current time in milliseconds
    current_time = pygame.time.get_ticks()

    
    if current_time - food_spawn_time > FOOD_LIFETIME:
        food = generate_food()

    # Get current snake head
    head = snake[0]

    # Create new head position
    new_head = (head[0] + dx, head[1] + dy)

    
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False
        continue

    # Check collision with itself
    if new_head in snake:
        running = False
        continue

    # Add new head to the beginning of the snake
    snake.insert(0, new_head)

   
    if new_head == food:

        
        score += food_weight

        # Generate new food
        food = generate_food()

        
        new_level = score // POINTS_FOR_NEXT_LEVEL + 1

        
        if new_level > level:
            level = new_level
            speed += 2

    else:
        # If snake did not eat food, remove the tail
        snake.pop()

    # Fill background
    screen.fill((30, 30, 30))

    # Draw vertical grid lines
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))

    
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))

    # Draw snake
    for i, segment in enumerate(snake):
        
        green_value = max(80, 255 - i * 5)
        snake_color = (0, green_value, 0)

        pygame.draw.rect(
            screen,
            snake_color,
            (segment[0], segment[1], CELL, CELL),
            border_radius=5
        )

    # Draw food with color depending on weight
    pygame.draw.rect(
        screen,
        get_food_color(food_weight),
        (food[0], food[1], CELL, CELL),
        border_radius=5
    )

    # Show food weight number on food
    weight_text = font.render(str(food_weight), True, (255, 255, 255))
    screen.blit(weight_text, (food[0] + 4, food[1] - 2))

    # Calculate time left before food disappears
    time_left = (FOOD_LIFETIME - (current_time - food_spawn_time)) // 1000 + 1

    
    if time_left < 0:
        time_left = 0

    # Create score text
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))

    # Create level text
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))

    # Create food weight text
    food_text = font.render("Food weight: " + str(food_weight), True, (255, 255, 255))

    # Create timer text
    timer_text = font.render("Time: " + str(time_left), True, (255, 255, 255))

    
    screen.blit(score_text, (10, 10))

   
    screen.blit(level_text, (10, 40))

   
    screen.blit(food_text, (10, 70))

    # Draw timer on the screen
    screen.blit(timer_text, (10, 100))

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(speed)


pygame.quit()