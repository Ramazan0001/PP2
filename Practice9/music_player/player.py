import pygame
import os

playlist = []
current_index = 0
is_playing = False


def load_music(folder):
    global playlist
    for file in os.listdir(folder):
        if file.endswith(".mp3") or file.endswith(".wav"):
            playlist.append(os.path.join(folder, file))
    playlist.sort()


def play():
    global is_playing
    if len(playlist) == 0:
        return
    pygame.mixer.music.load(playlist[current_index])
    pygame.mixer.music.play()
    is_playing = True


def stop():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False


def next_track():
    global current_index
    if len(playlist) == 0:
        return
    current_index += 1
    if current_index >= len(playlist):
        current_index = 0
    play()


def previous_track():
    global current_index
    if len(playlist) == 0:
        return
    current_index -= 1
    if current_index < 0:
        current_index = len(playlist) - 1
    play()


def get_current_track():
    if len(playlist) == 0:
        return "No music"
    return os.path.basename(playlist[current_index])