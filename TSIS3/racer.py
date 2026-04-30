import pygame
import random
import os


WIDTH = 500
HEIGHT = 700

ROAD_LEFT = 80
ROAD_RIGHT = 420

LANES = [125, 205, 285, 365]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 80)
BLUE = (60, 150, 255)
ORANGE = (255, 150, 0)
PURPLE = (170, 80, 255)

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

IMAGES = {}


# Загружает картинку из assets и меняет размер
def load_image(name, size):
    path = os.path.join(ASSETS_DIR, name)

    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, size)

    return image


# Загружает все картинки один раз, чтобы игра не лагала
def load_all_images():
    if len(IMAGES) > 0:
        return

    IMAGES["road"] = load_image("AnimatedStreet.png", (WIDTH, HEIGHT))
    IMAGES["player"] = load_image("Player.png", (45, 80))
    IMAGES["enemy"] = load_image("Enemy.png", (45, 80))
    IMAGES["barrier"] = load_image("Barrier.png", (75, 50))
    IMAGES["oil"] = load_image("Oil.png", (75, 50))
    IMAGES["nitro"] = load_image("Nitro.png", (45, 45))


# Создаёт игрока
def create_player():
    player = {
        "rect": pygame.Rect(WIDTH // 2 - 45 // 2, HEIGHT - 120, 45, 80),
        "speed": 6,
        "image": IMAGES["player"]
    }

    return player


# Двигает игрока по стрелкам и не даёт выйти за дорогу
def move_player(player):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player["rect"].left > ROAD_LEFT:
        player["rect"].x -= player["speed"]

    if keys[pygame.K_RIGHT] and player["rect"].right < ROAD_RIGHT:
        player["rect"].x += player["speed"]

    if keys[pygame.K_UP] and player["rect"].top > 0:
        player["rect"].y -= player["speed"]

    if keys[pygame.K_DOWN] and player["rect"].bottom < HEIGHT:
        player["rect"].y += player["speed"]


def draw_player(screen, player):
    screen.blit(player["image"], player["rect"])


# Создаёт вражескую машину сверху на случайной полосе
def create_enemy(speed):
    w = 45
    h = 80

    enemy = {
        "rect": pygame.Rect(random.choice(LANES) - w // 2, -100, w, h),
        "speed": speed,
        "image": IMAGES["enemy"]
    }

    return enemy


# Двигает вражескую машину вниз
def update_enemy(enemy):
    enemy["rect"].y += enemy["speed"]


def draw_enemy(screen, enemy):
    screen.blit(enemy["image"], enemy["rect"])


# Создаёт монету с разной ценностью
def create_coin():
    radius = 14
    x = random.choice(LANES)
    y = -50

    chance = random.randint(1, 100)

    if chance <= 60:
        value = 1
        color = YELLOW
    elif chance <= 90:
        value = 3
        color = ORANGE
    else:
        value = 5
        color = PURPLE

    coin = {
        "x": x,
        "y": y,
        "radius": radius,
        "value": value,
        "color": color,
        "rect": pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
    }

    return coin


# Двигает монету вниз вместе с дорогой
def update_coin(coin, speed):
    coin["y"] += speed
    coin["rect"].y = coin["y"] - coin["radius"]


def draw_coin(screen, coin):
    pygame.draw.circle(screen, coin["color"], (coin["x"], coin["y"]), coin["radius"])
    pygame.draw.circle(screen, WHITE, (coin["x"], coin["y"]), coin["radius"], 2)


# Создаёт obstacle: barrier, oil или pothole
def create_obstacle(obstacle_type, speed):
    w = 75
    h = 50

    image = None

    if obstacle_type == "barrier":
        image = IMAGES["barrier"]

    elif obstacle_type == "oil":
        image = IMAGES["oil"]

    obstacle = {
        "type": obstacle_type,
        "rect": pygame.Rect(random.choice(LANES) - w // 2, -80, w, h),
        "speed": speed,
        "image": image
    }

    return obstacle


# Двигает obstacle вниз
def update_obstacle(obstacle):
    obstacle["rect"].y += obstacle["speed"]


def draw_obstacle(screen, obstacle):
    if obstacle["image"] is not None:
        screen.blit(obstacle["image"], obstacle["rect"])

    else:
        pygame.draw.ellipse(screen, BLACK, obstacle["rect"])
        pygame.draw.rect(screen, WHITE, obstacle["rect"], 2)


# Создаёт power-up: nitro, shield или repair
def create_powerup(power_type):
    size = 45

    image = None

    if power_type == "nitro":
        image = IMAGES["nitro"]

    powerup = {
        "type": power_type,
        "rect": pygame.Rect(random.choice(LANES) - size // 2, -80, size, size),
        "spawn_time": pygame.time.get_ticks(),
        "life_time": 6000,
        "image": image
    }

    return powerup


def update_powerup(powerup, speed):
    powerup["rect"].y += speed


# Проверяет, не исчез ли power-up через 6 секунд
def powerup_expired(powerup):
    now = pygame.time.get_ticks()

    if now - powerup["spawn_time"] > powerup["life_time"]:
        return True

    return False


def draw_powerup(screen, powerup):
    if powerup["image"] is not None:
        screen.blit(powerup["image"], powerup["rect"])

    else:
        if powerup["type"] == "shield":
            color = GREEN
            letter = "S"

        else:
            color = RED
            letter = "R"

        pygame.draw.rect(screen, color, powerup["rect"], border_radius=8)
        pygame.draw.rect(screen, WHITE, powerup["rect"], 2, border_radius=8)

        font = pygame.font.SysFont("Verdana", 20)
        text = font.render(letter, True, WHITE)
        text_rect = text.get_rect(center=powerup["rect"].center)
        screen.blit(text, text_rect)


# Создаёт nitro strip на дороге
def create_nitro_strip(speed):
    w = 80
    h = 25

    event = {
        "rect": pygame.Rect(random.choice(LANES) - w // 2, -70, w, h),
        "speed": speed
    }

    return event


def update_nitro_strip(event):
    event["rect"].y += event["speed"]


def draw_nitro_strip(screen, event):
    pygame.draw.rect(screen, BLUE, event["rect"], border_radius=5)
    pygame.draw.rect(screen, WHITE, event["rect"], 2, border_radius=5)


# Создаёт весь game dictionary со всеми данными игры
def create_game(username, settings):
    load_all_images()

    game = {
        "username": username,
        "settings": settings,

        "player": create_player(),

        "road_image": IMAGES["road"],
        "road_y1": 0,
        "road_y2": -HEIGHT,

        "enemies": [],
        "coins": [],
        "obstacles": [],
        "powerups": [],
        "road_events": [],

        "coin_count": 0,
        "score": 0,
        "distance": 0,

        "game_over": False,

        "active_power": None,
        "power_start_time": 0,
        "power_duration": 0,
        "shield_active": False,

        "oil_slow_active": False,
        "oil_slow_start": 0,
        "oil_slow_duration": 2000,

        "spawn_enemy_timer": 0,
        "spawn_coin_timer": 0,
        "spawn_obstacle_timer": 0,
        "spawn_powerup_timer": 0,
        "spawn_event_timer": 0,

        "base_speed": 5,
        "enemy_spawn_delay": 1600,
        "obstacle_spawn_delay": 2100
    }

    set_difficulty(game)

    return game


# Настраивает сложность: easy, normal, hard
def set_difficulty(game):
    difficulty = game["settings"]["difficulty"]

    if difficulty == "easy":
        game["base_speed"] = 4
        game["enemy_spawn_delay"] = 2000
        game["obstacle_spawn_delay"] = 2600

    elif difficulty == "hard":
        game["base_speed"] = 6
        game["enemy_spawn_delay"] = 1200
        game["obstacle_spawn_delay"] = 1600

    else:
        game["base_speed"] = 5
        game["enemy_spawn_delay"] = 1600
        game["obstacle_spawn_delay"] = 2100


# Возвращает текущую скорость дороги с учётом nitro
def get_current_speed(game):
    speed = game["base_speed"]

    if game["active_power"] == "nitro":
        speed += 3

    return speed


# Активирует nitro, shield или repair
def activate_powerup(game, power_type):
    if power_type == "nitro":
        if game["active_power"] is None:
            game["active_power"] = "nitro"
            game["power_duration"] = 4000
            game["power_start_time"] = pygame.time.get_ticks()

    elif power_type == "shield":
        if game["active_power"] is None:
            game["active_power"] = "shield"
            game["shield_active"] = True
            game["power_duration"] = 999999
            game["power_start_time"] = pygame.time.get_ticks()

    elif power_type == "repair":
        if len(game["obstacles"]) > 0:
            game["obstacles"].pop(0)

        game["score"] += 50


# Выключает nitro после 4 секунд
def update_powerup_timer(game):
    if game["active_power"] is None:
        return

    if game["active_power"] == "shield":
        return

    now = pygame.time.get_ticks()

    if now - game["power_start_time"] > game["power_duration"]:
        game["active_power"] = None
        game["power_duration"] = 0


# Возвращает оставшееся время nitro
def get_power_time_left(game):
    if game["active_power"] is None:
        return 0

    if game["active_power"] == "shield":
        return 999

    now = pygame.time.get_ticks()

    left = game["power_duration"] - (now - game["power_start_time"])

    if left < 0:
        left = 0

    return left // 1000


# Замедляет игрока после oil на 2 секунды
def update_oil_slow(game):
    if game["oil_slow_active"]:
        game["player"]["speed"] = 3

        now = pygame.time.get_ticks()

        if now - game["oil_slow_start"] > game["oil_slow_duration"]:
            game["oil_slow_active"] = False
            game["player"]["speed"] = 6

    else:
        game["player"]["speed"] = 6


# Проверяет, чтобы объект не появился на игроке или другом объекте
def safe_spawn(game, new_rect):
    player_zone = game["player"]["rect"].inflate(70, 120)

    if new_rect.colliderect(player_zone):
        return False

    for enemy in game["enemies"]:
        if new_rect.colliderect(enemy["rect"].inflate(35, 70)):
            return False

    for obstacle in game["obstacles"]:
        if new_rect.colliderect(obstacle["rect"].inflate(35, 70)):
            return False

    for powerup in game["powerups"]:
        if new_rect.colliderect(powerup["rect"].inflate(35, 70)):
            return False

    return True


# Создаёт и добавляет врага в список enemies
def spawn_enemy(game):
    enemy_speed = get_current_speed(game) + 1 + game["coin_count"] // 15

    enemy = create_enemy(enemy_speed)

    if safe_spawn(game, enemy["rect"]):
        game["enemies"].append(enemy)


# Создаёт и добавляет монету в список coins
def spawn_coin(game):
    coin = create_coin()

    if safe_spawn(game, coin["rect"]):
        game["coins"].append(coin)


# Создаёт случайный obstacle: barrier, oil или pothole
def spawn_obstacle(game):
    obstacle_types = ["barrier", "oil", "pothole"]

    obstacle_type = random.choice(obstacle_types)

    obstacle = create_obstacle(obstacle_type, get_current_speed(game))

    if safe_spawn(game, obstacle["rect"]):
        game["obstacles"].append(obstacle)


# Создаёт случайный power-up
def spawn_powerup(game):
    power_types = ["nitro", "shield", "repair"]

    power_type = random.choice(power_types)

    powerup = create_powerup(power_type)

    if safe_spawn(game, powerup["rect"]):
        game["powerups"].append(powerup)


# Создаёт road event — nitro strip
def spawn_road_event(game):
    event = create_nitro_strip(get_current_speed(game))

    if safe_spawn(game, event["rect"]):
        game["road_events"].append(event)


# Управляет таймерами появления enemies, coins, obstacles и power-ups
def update_spawning(game):
    now = pygame.time.get_ticks()

    density_bonus = game["distance"] // 800

    enemy_delay = game["enemy_spawn_delay"] - density_bonus * 80
    obstacle_delay = game["obstacle_spawn_delay"] - density_bonus * 80

    if enemy_delay < 700:
        enemy_delay = 700

    if obstacle_delay < 900:
        obstacle_delay = 900

    if now - game["spawn_enemy_timer"] > enemy_delay:
        spawn_enemy(game)
        game["spawn_enemy_timer"] = now

    if now - game["spawn_coin_timer"] > 1400:
        spawn_coin(game)
        game["spawn_coin_timer"] = now

    if now - game["spawn_obstacle_timer"] > obstacle_delay:
        spawn_obstacle(game)
        game["spawn_obstacle_timer"] = now

    if now - game["spawn_powerup_timer"] > 9000:
        spawn_powerup(game)
        game["spawn_powerup_timer"] = now

    if now - game["spawn_event_timer"] > 12000:
        spawn_road_event(game)
        game["spawn_event_timer"] = now


# Проверяет все столкновения игрока с объектами
def handle_collisions(game):
    player_rect = game["player"]["rect"]

    for enemy in game["enemies"][:]:
        if player_rect.colliderect(enemy["rect"]):
            if game["shield_active"]:
                game["enemies"].remove(enemy)
                game["shield_active"] = False
                game["active_power"] = None

            else:
                game["game_over"] = True

    for coin in game["coins"][:]:
        if player_rect.colliderect(coin["rect"]):
            game["coin_count"] += coin["value"]
            game["score"] += coin["value"] * 10
            game["coins"].remove(coin)

    for obstacle in game["obstacles"][:]:
        if player_rect.colliderect(obstacle["rect"]):

            if obstacle["type"] == "oil":
                game["oil_slow_active"] = True
                game["oil_slow_start"] = pygame.time.get_ticks()
                game["obstacles"].remove(obstacle)

            elif obstacle["type"] == "pothole":
                game["score"] -= 20
                game["obstacles"].remove(obstacle)

            elif obstacle["type"] == "barrier":
                if game["shield_active"]:
                    game["obstacles"].remove(obstacle)
                    game["shield_active"] = False
                    game["active_power"] = None

                else:
                    game["game_over"] = True

    for powerup in game["powerups"][:]:
        if player_rect.colliderect(powerup["rect"]):
            activate_powerup(game, powerup["type"])
            game["powerups"].remove(powerup)

    for event in game["road_events"][:]:
        if player_rect.colliderect(event["rect"]):
            activate_powerup(game, "nitro")
            game["road_events"].remove(event)


# Ограничивает количество объектов на экране, чтобы не было лагов
def limit_objects(game):
    if len(game["enemies"]) > 6:
        game["enemies"] = game["enemies"][-6:]

    if len(game["coins"]) > 8:
        game["coins"] = game["coins"][-8:]

    if len(game["obstacles"]) > 6:
        game["obstacles"] = game["obstacles"][-6:]

    if len(game["powerups"]) > 3:
        game["powerups"] = game["powerups"][-3:]

    if len(game["road_events"]) > 2:
        game["road_events"] = game["road_events"][-2:]


# Главная функция обновления игры каждый кадр
def update_game(game):
    update_oil_slow(game)

    move_player(game["player"])

    update_powerup_timer(game)

    road_speed = get_current_speed(game)

    game["distance"] += road_speed // 2
    game["score"] += 1

    update_spawning(game)

    for enemy in game["enemies"][:]:
        update_enemy(enemy)

        if enemy["rect"].top > HEIGHT:
            game["enemies"].remove(enemy)

    for coin in game["coins"][:]:
        update_coin(coin, road_speed)

        if coin["rect"].top > HEIGHT:
            game["coins"].remove(coin)

    for obstacle in game["obstacles"][:]:
        obstacle["speed"] = road_speed
        update_obstacle(obstacle)

        if obstacle["rect"].top > HEIGHT:
            game["obstacles"].remove(obstacle)

    for powerup in game["powerups"][:]:
        update_powerup(powerup, road_speed)

        if powerup["rect"].top > HEIGHT or powerup_expired(powerup):
            game["powerups"].remove(powerup)

    for event in game["road_events"][:]:
        event["speed"] = road_speed
        update_nitro_strip(event)

        if event["rect"].top > HEIGHT:
            game["road_events"].remove(event)

    limit_objects(game)
    handle_collisions(game)


# Рисует и двигает фон дороги
def draw_road(screen, game):
    speed = get_current_speed(game)

    game["road_y1"] += speed
    game["road_y2"] += speed

    if game["road_y1"] >= HEIGHT:
        game["road_y1"] = -HEIGHT

    if game["road_y2"] >= HEIGHT:
        game["road_y2"] = -HEIGHT

    screen.blit(game["road_image"], (0, game["road_y1"]))
    screen.blit(game["road_image"], (0, game["road_y2"]))


# Рисует score, coins, distance и active power
def draw_game_ui(screen, font, game):
    score_text = font.render("Score: " + str(game["score"]), True, WHITE)
    coins_text = font.render("Coins: " + str(game["coin_count"]), True, WHITE)
    distance_text = font.render("Distance: " + str(game["distance"]) + "m", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 40))
    screen.blit(distance_text, (10, 70))

    y = 100

    if game["active_power"] is not None:
        if game["active_power"] == "shield":
            power_text = "Power: Shield"

        else:
            power_text = "Power: Nitro " + str(get_power_time_left(game)) + "s"

        surface = font.render(power_text, True, YELLOW)
        screen.blit(surface, (10, y))
        y += 30

    if game["oil_slow_active"]:
        slow_text = font.render("Oil: slowed", True, RED)
        screen.blit(slow_text, (10, y))


# Главная функция рисования всей игры
def draw_game(screen, font, game):
    draw_road(screen, game)

    for event in game["road_events"]:
        draw_nitro_strip(screen, event)

    for coin in game["coins"]:
        draw_coin(screen, coin)

    for powerup in game["powerups"]:
        draw_powerup(screen, powerup)

    for obstacle in game["obstacles"]:
        draw_obstacle(screen, obstacle)

    for enemy in game["enemies"]:
        draw_enemy(screen, enemy)

    draw_player(screen, game["player"])

    draw_game_ui(screen, font, game)