import pygame
import sys
import os

from game import WIDTH, HEIGHT, load_settings, save_settings, run_game
from db import setup_database, save_game_session, get_top_10, get_personal_best


pygame.init()

try:
    pygame.mixer.init()
except Exception as e:
    print("Mixer init error:", e)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 Snake Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
LIGHT_GRAY = (100, 100, 100)

GREEN = (0, 255, 0)
RED = (220, 50, 50)
BLUE = (50, 120, 255)
YELLOW = (255, 220, 0)


def play_music():
    try:
        settings = load_settings()

        if not settings["sound"]:
            return

        music_path = os.path.join("assets", "music.mp3")

        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
        else:
            print("Music file not found:", music_path)

    except Exception as e:
        print("Music error:", e)


def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print("Stop music error:", e)


def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("arial", size)
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def draw_center_text(text, size, color, y):
    font = pygame.font.SysFont("arial", size)
    image = font.render(text, True, color)
    rect = image.get_rect(center=(WIDTH // 2, y))
    screen.blit(image, rect)


def draw_button(text, rect, mouse_pos):
    color = GRAY

    if rect.collidepoint(mouse_pos):
        color = LIGHT_GRAY

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)

    font = pygame.font.SysFont("arial", 28)
    image = font.render(text, True, WHITE)
    image_rect = image.get_rect(center=rect.center)
    screen.blit(image, image_rect)


def main_menu():
    username = ""

    play_button = pygame.Rect(300, 230, 200, 50)
    leaderboard_button = pygame.Rect(300, 300, 200, 50)
    settings_button = pygame.Rect(300, 370, 200, 50)
    quit_button = pygame.Rect(300, 440, 200, 50)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BLACK)

        draw_center_text("TSIS 4 SNAKE GAME", 42, GREEN, 80)
        draw_center_text("Enter username:", 28, WHITE, 140)

        pygame.draw.rect(screen, GRAY, (250, 170, 300, 40))
        pygame.draw.rect(screen, WHITE, (250, 170, 300, 40), 2)

        draw_text(username, 26, WHITE, 260, 175)

        draw_button("Play", play_button, mouse_pos)
        draw_button("Leaderboard", leaderboard_button, mouse_pos)
        draw_button("Settings", settings_button, mouse_pos)
        draw_button("Quit", quit_button, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.key == pygame.K_RETURN:
                    if username.strip() != "":
                        return "play", username.strip()

                else:
                    if len(username) < 12:
                        username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    if username.strip() != "":
                        return "play", username.strip()

                if leaderboard_button.collidepoint(mouse_pos):
                    return "leaderboard", username.strip()

                if settings_button.collidepoint(mouse_pos):
                    return "settings", username.strip()

                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen():
    back_button = pygame.Rect(300, 520, 200, 50)

    try:
        results = get_top_10()
    except Exception as e:
        print("Leaderboard error:", e)
        results = []

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BLACK)

        draw_center_text("LEADERBOARD", 42, YELLOW, 60)

        draw_text("Rank", 24, WHITE, 80, 120)
        draw_text("Username", 24, WHITE, 160, 120)
        draw_text("Score", 24, WHITE, 340, 120)
        draw_text("Level", 24, WHITE, 460, 120)
        draw_text("Date", 24, WHITE, 560, 120)

        if len(results) == 0:
            draw_center_text("No results yet.", 28, RED, 260)
        else:
            y = 160
            rank = 1

            for row in results:
                username = row[0]
                score = row[1]
                level = row[2]
                date = row[3].strftime("%Y-%m-%d")

                draw_text(str(rank), 22, WHITE, 90, y)
                draw_text(username, 22, WHITE, 160, y)
                draw_text(str(score), 22, WHITE, 350, y)
                draw_text(str(level), 22, WHITE, 470, y)
                draw_text(date, 22, WHITE, 560, y)

                y += 35
                rank += 1

        draw_button("Back", back_button, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(mouse_pos):
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()
        clock.tick(60)


def settings_screen():
    settings = load_settings()

    grid_button = pygame.Rect(270, 180, 260, 50)
    sound_button = pygame.Rect(270, 250, 260, 50)
    color_button = pygame.Rect(270, 320, 260, 50)
    save_button = pygame.Rect(270, 430, 260, 50)

    colors = [
        [0, 255, 0],
        [50, 120, 255],
        [255, 220, 0],
        [220, 50, 50],
        [170, 80, 255]
    ]

    color_index = 0

    if settings["snake_color"] in colors:
        color_index = colors.index(settings["snake_color"])

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BLACK)

        draw_center_text("SETTINGS", 42, BLUE, 70)

        if settings["grid"]:
            grid_text = "Grid: ON"
        else:
            grid_text = "Grid: OFF"

        if settings["sound"]:
            sound_text = "Sound: ON"
        else:
            sound_text = "Sound: OFF"

        draw_button(grid_text, grid_button, mouse_pos)
        draw_button(sound_text, sound_button, mouse_pos)
        draw_button("Change Snake Color", color_button, mouse_pos)
        draw_button("Save & Back", save_button, mouse_pos)

        draw_text("Current color:", 26, WHITE, 280, 390)
        pygame.draw.rect(screen, tuple(settings["snake_color"]), (460, 390, 40, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_button.collidepoint(mouse_pos):
                    settings["grid"] = not settings["grid"]

                if sound_button.collidepoint(mouse_pos):
                    settings["sound"] = not settings["sound"]

                if color_button.collidepoint(mouse_pos):
                    color_index += 1

                    if color_index >= len(colors):
                        color_index = 0

                    settings["snake_color"] = colors[color_index]

                if save_button.collidepoint(mouse_pos):
                    save_settings(settings)
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return

        pygame.display.update()
        clock.tick(60)


def game_over_screen(username, score, level, personal_best):
    retry_button = pygame.Rect(300, 350, 200, 50)
    menu_button = pygame.Rect(300, 420, 200, 50)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BLACK)

        draw_center_text("GAME OVER", 50, RED, 100)

        draw_center_text("Player: " + username, 30, WHITE, 180)
        draw_center_text("Score: " + str(score), 30, WHITE, 230)
        draw_center_text("Level: " + str(level), 30, WHITE, 280)
        draw_center_text("Personal Best: " + str(personal_best), 30, YELLOW, 320)

        draw_button("Retry", retry_button, mouse_pos)
        draw_button("Main Menu", menu_button, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(mouse_pos):
                    return "retry"

                if menu_button.collidepoint(mouse_pos):
                    return "menu"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "retry"

                if event.key == pygame.K_ESCAPE:
                    return "menu"

        pygame.display.update()
        clock.tick(60)


def main():
    try:
        setup_database()
    except Exception as e:
        print("Database setup error:", e)

    while True:
        action, username = main_menu()

        if action == "leaderboard":
            leaderboard_screen()

        elif action == "settings":
            settings_screen()

        elif action == "play":
            playing = True

            while playing:
                try:
                    personal_best = get_personal_best(username)
                except Exception as e:
                    print("Personal best error:", e)
                    personal_best = 0

                play_music()

                score, level, quit_game = run_game(screen, username, personal_best)

                stop_music()

                if quit_game:
                    pygame.quit()
                    sys.exit()

                try:
                    save_game_session(username, score, level)
                except Exception as e:
                    print("Save result error:", e)

                if score > personal_best:
                    personal_best = score

                result = game_over_screen(username, score, level, personal_best)

                if result == "retry":
                    playing = True

                if result == "menu":
                    playing = False


main()