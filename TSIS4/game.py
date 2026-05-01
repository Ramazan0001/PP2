import pygame
import random
import json
import os


WIDTH = 800
HEIGHT = 600
CELL = 20
TOP_BAR = 60

GRID_WIDTH = WIDTH // CELL
GRID_HEIGHT = (HEIGHT - TOP_BAR) // CELL

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (45, 45, 45)
DARK_GRAY = (25, 25, 25)

RED = (220, 50, 50)
DARK_RED = (120, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 120, 255)
YELLOW = (255, 220, 0)
PURPLE = (170, 80, 255)
ORANGE = (255, 150, 0)

SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        settings = {
            "snake_color": [0, 255, 0],
            "grid": True,
            "sound": True
        }
        save_settings(settings)
        return settings

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont("arial", size)
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def grid_to_pixel(pos):
    x = pos[0] * CELL
    y = TOP_BAR + pos[1] * CELL
    return x, y


def random_empty_cell(snake, normal_food, poison_food, power_up, obstacles):
    while True:
        pos = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

        if pos in snake:
            continue

        if normal_food is not None and pos == normal_food["pos"]:
            continue

        if poison_food is not None and pos == poison_food["pos"]:
            continue

        if power_up is not None and pos == power_up["pos"]:
            continue

        if pos in obstacles:
            continue

        return pos


def create_normal_food(snake, poison_food, power_up, obstacles):
    food_types = [
        {"value": 1, "color": RED},
        {"value": 2, "color": YELLOW},
        {"value": 3, "color": BLUE}
    ]

    food = random.choice(food_types)

    return {
        "pos": random_empty_cell(snake, None, poison_food, power_up, obstacles),
        "value": food["value"],
        "color": food["color"],
        "spawn_time": pygame.time.get_ticks(),
        "life_time": 6000
    }


def create_poison_food(snake, normal_food, power_up, obstacles):
    return {
        "pos": random_empty_cell(snake, normal_food, None, power_up, obstacles),
        "spawn_time": pygame.time.get_ticks(),
        "life_time": 7000
    }


def create_power_up(snake, normal_food, poison_food, obstacles):
    power_types = ["speed", "slow", "shield"]

    return {
        "pos": random_empty_cell(snake, normal_food, poison_food, None, obstacles),
        "type": random.choice(power_types),
        "spawn_time": pygame.time.get_ticks(),
        "life_time": 8000
    }


def create_obstacles(level, snake, normal_food, poison_food, power_up):
    obstacles = []

    if level < 3:
        return obstacles

    count = level + 2
    head = snake[0]

    safe_area = [
        head,
        (head[0] + 1, head[1]),
        (head[0] - 1, head[1]),
        (head[0], head[1] + 1),
        (head[0], head[1] - 1)
    ]

    while len(obstacles) < count:
        pos = (
            random.randint(2, GRID_WIDTH - 3),
            random.randint(2, GRID_HEIGHT - 3)
        )

        if pos in snake:
            continue

        if pos in safe_area:
            continue

        if normal_food is not None and pos == normal_food["pos"]:
            continue

        if poison_food is not None and pos == poison_food["pos"]:
            continue

        if power_up is not None and pos == power_up["pos"]:
            continue

        if pos in obstacles:
            continue

        obstacles.append(pos)

    return obstacles


def draw_grid(screen):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, TOP_BAR), (x, HEIGHT))

    for y in range(TOP_BAR, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_snake(screen, snake, snake_color):
    for part in snake:
        x, y = grid_to_pixel(part)
        pygame.draw.rect(screen, snake_color, (x, y, CELL, CELL))


def draw_food(screen, normal_food):
    if normal_food is None:
        return

    x, y = grid_to_pixel(normal_food["pos"])
    pygame.draw.rect(screen, normal_food["color"], (x, y, CELL, CELL))


def draw_poison(screen, poison_food):
    if poison_food is None:
        return

    x, y = grid_to_pixel(poison_food["pos"])
    pygame.draw.rect(screen, DARK_RED, (x, y, CELL, CELL))


def draw_power_up(screen, power_up):
    if power_up is None:
        return

    x, y = grid_to_pixel(power_up["pos"])

    if power_up["type"] == "speed":
        color = ORANGE
    elif power_up["type"] == "slow":
        color = BLUE
    else:
        color = PURPLE

    pygame.draw.rect(screen, color, (x, y, CELL, CELL))


def draw_obstacles(screen, obstacles):
    for block in obstacles:
        x, y = grid_to_pixel(block)
        pygame.draw.rect(screen, WHITE, (x, y, CELL, CELL))


def get_current_speed(base_speed, active_power):
    if active_power["type"] == "speed":
        return base_speed + 5

    if active_power["type"] == "slow":
        speed = base_speed - 4

        if speed < 4:
            speed = 4

        return speed

    return base_speed


def check_wall_collision(pos):
    x = pos[0]
    y = pos[1]

    if x < 0 or x >= GRID_WIDTH:
        return True

    if y < 0 or y >= GRID_HEIGHT:
        return True

    return False


def opposite_direction(direction):
    if direction == (1, 0):
        return (-1, 0)

    if direction == (-1, 0):
        return (1, 0)

    if direction == (0, 1):
        return (0, -1)

    if direction == (0, -1):
        return (0, 1)

    return direction


def run_game(screen, username, personal_best):
    settings = load_settings()
    snake_color = tuple(settings["snake_color"])

    clock = pygame.time.Clock()

    snake = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)
    ]

    direction = (1, 0)
    next_direction = direction

    score = 0
    level = 1
    food_eaten = 0
    base_speed = 8

    active_power = {
        "type": None,
        "end_time": 0
    }

    shield = False
    obstacles = []
    power_up = None

    normal_food = create_normal_food(snake, None, power_up, obstacles)
    poison_food = create_poison_food(snake, normal_food, power_up, obstacles)

    while True:
        now = pygame.time.get_ticks()
        current_speed = get_current_speed(base_speed, active_power)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, level, True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)

                if event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)

                if event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)

                if event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

                if event.key == pygame.K_ESCAPE:
                    return score, level, False

        direction = next_direction

        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        wall_collision = check_wall_collision(new_head)
        self_collision = new_head in snake
        obstacle_collision = new_head in obstacles

        if wall_collision or self_collision:
            if shield:
                shield = False
                direction = opposite_direction(direction)
                next_direction = direction
                new_head = head
            else:
                return score, level, False

        if obstacle_collision:
            return score, level, False

        if new_head != head:
            snake.insert(0, new_head)

        ate_food = False

        if normal_food is not None and new_head == normal_food["pos"]:
            score += normal_food["value"] * 10
            food_eaten += 1
            ate_food = True
            normal_food = create_normal_food(snake, poison_food, power_up, obstacles)

        if not ate_food and new_head != head:
            snake.pop()

        if poison_food is not None and new_head == poison_food["pos"]:
            for i in range(2):
                if len(snake) > 0:
                    snake.pop()

            poison_food = create_poison_food(snake, normal_food, power_up, obstacles)

            if len(snake) <= 1:
                return score, level, False

        if power_up is not None and new_head == power_up["pos"]:
            if power_up["type"] == "speed":
                active_power["type"] = "speed"
                active_power["end_time"] = now + 5000

            elif power_up["type"] == "slow":
                active_power["type"] = "slow"
                active_power["end_time"] = now + 5000

            elif power_up["type"] == "shield":
                shield = True

            power_up = None

        if active_power["type"] is not None and now > active_power["end_time"]:
            active_power["type"] = None
            active_power["end_time"] = 0

        if normal_food is not None:
            if now - normal_food["spawn_time"] > normal_food["life_time"]:
                normal_food = create_normal_food(snake, poison_food, power_up, obstacles)

        if poison_food is not None:
            if now - poison_food["spawn_time"] > poison_food["life_time"]:
                poison_food = create_poison_food(snake, normal_food, power_up, obstacles)

        if power_up is None:
            chance = random.randint(1, 100)

            if chance == 1:
                power_up = create_power_up(snake, normal_food, poison_food, obstacles)
        else:
            if now - power_up["spawn_time"] > power_up["life_time"]:
                power_up = None

        if food_eaten >= 4:
            food_eaten = 0
            level += 1
            base_speed += 1
            obstacles = create_obstacles(level, snake, normal_food, poison_food, power_up)

        screen.fill(DARK_GRAY)
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, TOP_BAR))

        draw_text(screen, "Player: " + username, 24, WHITE, 20, 15)
        draw_text(screen, "Score: " + str(score), 24, WHITE, 210, 15)
        draw_text(screen, "Level: " + str(level), 24, WHITE, 350, 15)
        draw_text(screen, "Best: " + str(personal_best), 24, WHITE, 470, 15)

        if shield:
            draw_text(screen, "Shield: ON", 22, PURPLE, 620, 15)
        elif active_power["type"] is not None:
            time_left = (active_power["end_time"] - now) // 1000
            draw_text(screen, active_power["type"] + ": " + str(time_left), 22, YELLOW, 620, 15)

        if settings["grid"]:
            draw_grid(screen)

        draw_food(screen, normal_food)
        draw_poison(screen, poison_food)
        draw_power_up(screen, power_up)
        draw_obstacles(screen, obstacles)
        draw_snake(screen, snake, snake_color)

        pygame.display.update()
        clock.tick(current_speed)