import pygame


WHITE = (255, 255, 255)
GRAY = (80, 80, 80)


def create_button(x, y, w, h, text):
    button = {
        "rect": pygame.Rect(x, y, w, h),
        "text": text
    }

    return button


def draw_button(screen, font, button):
    pygame.draw.rect(screen, GRAY, button["rect"], border_radius=10)
    pygame.draw.rect(screen, WHITE, button["rect"], 2, border_radius=10)

    text_surface = font.render(button["text"], True, WHITE)
    text_rect = text_surface.get_rect(center=button["rect"].center)

    screen.blit(text_surface, text_rect)


def button_clicked(button, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if button["rect"].collidepoint(event.pos):
                return True

    return False


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_center_text(screen, text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(text_surface, text_rect)