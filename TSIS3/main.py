import pygame
import sys

from racer import create_game, update_game, draw_game, WIDTH, HEIGHT
from ui import create_button, draw_button, button_clicked, draw_center_text, draw_text
from persistence import load_settings, save_settings, load_leaderboard, add_score


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BG = (30, 30, 30)
RED = (220, 0, 0)
YELLOW = (255, 220, 0)

font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 16)
big_font = pygame.font.SysFont("Verdana", 38)

settings = load_settings()

state = "menu"
game = None
username = ""
score_saved = False


# Создаёт кнопки главного меню
play_button = create_button(150, 220, 200, 50, "Play")
leaderboard_button = create_button(150, 290, 200, 50, "Leaderboard")
settings_button = create_button(150, 360, 200, 50, "Settings")
quit_button = create_button(150, 430, 200, 50, "Quit")

# Создаёт кнопку Back для экранов Settings и Leaderboard
back_button = create_button(150, 600, 200, 50, "Back")

# Создаёт кнопки экрана Game Over
retry_button = create_button(150, 420, 200, 50, "Retry")
menu_button = create_button(150, 490, 200, 50, "Main Menu")


# Рисует экран главного меню
def draw_menu_screen():
    screen.fill(BG)

    draw_center_text(screen, "TSIS3 RACER", big_font, WHITE, 120)

    draw_button(screen, font, play_button)
    draw_button(screen, font, leaderboard_button)
    draw_button(screen, font, settings_button)
    draw_button(screen, font, quit_button)


# Рисует экран ввода имени игрока
def draw_name_screen():
    screen.fill(BG)

    draw_center_text(screen, "Enter Username", big_font, WHITE, 170)
    draw_center_text(screen, username, font, YELLOW, 260)
    draw_center_text(screen, "Press ENTER to start", small_font, WHITE, 330)


# Рисует экран таблицы лидеров
def draw_leaderboard_screen():
    screen.fill(BG)

    draw_center_text(screen, "TOP 10 LEADERBOARD", big_font, WHITE, 70)

    leaderboard = load_leaderboard()

    y = 140

    if len(leaderboard) == 0:
        draw_center_text(screen, "No scores yet", font, WHITE, 250)

    else:
        for i in range(len(leaderboard)):
            item = leaderboard[i]

            text = (
                str(i + 1)
                + ". "
                + item["name"]
                + " | Score: "
                + str(item["score"])
                + " | Distance: "
                + str(item["distance"])
                + "m"
            )

            draw_text(screen, text, small_font, WHITE, 35, y)

            y += 35

    draw_button(screen, font, back_button)


# Рисует экран настроек
def draw_settings_screen():
    screen.fill(BG)

    draw_center_text(screen, "SETTINGS", big_font, WHITE, 70)

    if settings["sound"]:
        sound_text = "Sound: ON"
    else:
        sound_text = "Sound: OFF"

    car_text = "Car Color: " + settings["car_color"]
    difficulty_text = "Difficulty: " + settings["difficulty"]

    draw_center_text(screen, sound_text, font, WHITE, 170)
    draw_center_text(screen, "Press S to toggle sound", small_font, YELLOW, 205)

    draw_center_text(screen, car_text, font, WHITE, 270)
    draw_center_text(screen, "Press C to change color", small_font, YELLOW, 305)

    draw_center_text(screen, difficulty_text, font, WHITE, 370)
    draw_center_text(screen, "Press D to change difficulty", small_font, YELLOW, 405)

    draw_button(screen, font, back_button)


# Рисует экран после проигрыша
def draw_game_over_screen():
    screen.fill(BG)

    draw_center_text(screen, "GAME OVER", big_font, RED, 110)

    if game is not None:
        draw_center_text(screen, "Player: " + username, font, WHITE, 190)
        draw_center_text(screen, "Score: " + str(game["score"]), font, WHITE, 230)
        draw_center_text(screen, "Distance: " + str(game["distance"]) + "m", font, WHITE, 270)
        draw_center_text(screen, "Coins: " + str(game["coin_count"]), font, WHITE, 310)

    draw_button(screen, font, retry_button)
    draw_button(screen, font, menu_button)


# Меняет цвет машины в settings.json
def change_car_color():
    colors = ["blue", "red", "green", "yellow"]

    current_color = settings["car_color"]
    index = colors.index(current_color)

    index += 1

    if index >= len(colors):
        index = 0

    settings["car_color"] = colors[index]

    save_settings(settings)


# Меняет сложность в settings.json
def change_difficulty():
    difficulties = ["easy", "normal", "hard"]

    current_difficulty = settings["difficulty"]
    index = difficulties.index(current_difficulty)

    index += 1

    if index >= len(difficulties):
        index = 0

    settings["difficulty"] = difficulties[index]

    save_settings(settings)


running = True


# Главный игровой цикл
while running:
    clock.tick(60)

    # Обрабатывает все события: клик мыши, ввод клавиатуры, закрытие окна
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Логика кнопок главного меню
        if state == "menu":

            if button_clicked(play_button, event):
                username = ""
                state = "name"

            elif button_clicked(leaderboard_button, event):
                state = "leaderboard"

            elif button_clicked(settings_button, event):
                state = "settings"

            elif button_clicked(quit_button, event):
                running = False

        # Логика ввода имени перед стартом игры
        elif state == "name":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if username.strip() == "":
                        username = "Player"

                    settings = load_settings()
                    game = create_game(username, settings)
                    score_saved = False

                    state = "game"

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if len(username) < 12:
                        username += event.unicode

        # Логика экрана Leaderboard
        elif state == "leaderboard":

            if button_clicked(back_button, event):
                state = "menu"

        # Логика экрана Settings
        elif state == "settings":

            if button_clicked(back_button, event):
                state = "menu"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                elif event.key == pygame.K_c:
                    change_car_color()

                elif event.key == pygame.K_d:
                    change_difficulty()

        # Логика кнопок экрана Game Over
        elif state == "game_over":

            if button_clicked(retry_button, event):
                settings = load_settings()
                game = create_game(username, settings)
                score_saved = False

                state = "game"

            elif button_clicked(menu_button, event):
                state = "menu"

    # Рисует нужный экран по текущему state
    if state == "menu":
        draw_menu_screen()

    elif state == "name":
        draw_name_screen()

    elif state == "leaderboard":
        draw_leaderboard_screen()

    elif state == "settings":
        draw_settings_screen()

    elif state == "game":

        if game is not None:
            update_game(game)
            draw_game(screen, font, game)

            if game["game_over"]:

                if not score_saved:
                    add_score(username, game["score"], game["distance"])
                    score_saved = True

                state = "game_over"

    elif state == "game_over":
        draw_game_over_screen()

    pygame.display.update()


pygame.quit()
sys.exit()