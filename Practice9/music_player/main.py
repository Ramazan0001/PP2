import pygame
import os
from player import *

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


base = os.path.dirname(__file__)
music_folder = os.path.join(base, "music")

load_music(music_folder)

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play()
            elif event.key == pygame.K_s:
                stop()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                previous_track()
            elif event.key == pygame.K_q:
                running = False

    
    title = font.render("Music Player", True, BLACK)
    screen.blit(title, (300, 50))

    track = font.render("Track: " + get_current_track(), True, BLACK)
    screen.blit(track, (200, 150))

    controls = font.render("P-Play S-Stop N-Next B-Back Q-Quit", True, BLACK)
    screen.blit(controls, (100, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()