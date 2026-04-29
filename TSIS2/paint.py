import pygame
import sys
from datetime import datetime

from tools import draw_rectangle
from tools import draw_circle
from tools import draw_square
from tools import draw_right_triangle
from tools import draw_equilateral_triangle
from tools import draw_rhombus
from tools import flood_fill


pygame.init()

WIDTH = 1100
HEIGHT = 700
TOOLBAR_HEIGHT = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 18)
small_font = pygame.font.SysFont("arial", 15)
text_font = pygame.font.SysFont("arial", 32)

current_tool = "pencil"
current_color = (0, 0, 0)
brush_size = 5

is_drawing = False
start_pos = None
last_pos = None
current_pos = None

text_active = False
text_pos = None
text_value = ""

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 180, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 140, 0),
    (150, 75, 0),
    (255, 255, 255)
]

buttons = []


def create_buttons():
    global buttons

    buttons = []

    tools = [
        ("Pencil", "pencil"),
        ("Line", "line"),
        ("Rect", "rectangle"),
        ("Circle", "circle"),
        ("Square", "square"),
        ("Right Tri", "right_triangle"),
        ("Equil Tri", "equilateral_triangle"),
        ("Rhombus", "rhombus"),
        ("Eraser", "eraser"),
        ("Fill", "fill"),
        ("Text", "text")
    ]

    x = 10
    y = 10

    for label, tool_name in tools:
        rect = pygame.Rect(x, y, 85, 32)

        buttons.append({
            "type": "tool",
            "label": label,
            "tool": tool_name,
            "rect": rect
        })

        x += 92

        if x > 950:
            x = 10
            y += 38

    sizes = [
        ("Small 2", 2),
        ("Medium 5", 5),
        ("Large 10", 10)
    ]

    x = 10
    y = 50

    for label, size in sizes:
        rect = pygame.Rect(x, y, 95, 30)

        buttons.append({
            "type": "size",
            "label": label,
            "size": size,
            "rect": rect
        })

        x += 105

    x = 340
    y = 50

    for color in colors:
        rect = pygame.Rect(x, y, 30, 30)

        buttons.append({
            "type": "color",
            "color": color,
            "rect": rect
        })

        x += 38

    save_rect = pygame.Rect(760, 50, 150, 30)

    buttons.append({
        "type": "save",
        "label": "Save Ctrl+S",
        "rect": save_rect
    })


def screen_to_canvas(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def is_on_canvas(pos):
    x, y = pos
    return y >= TOOLBAR_HEIGHT


def save_canvas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{timestamp}.png"

    pygame.image.save(canvas, filename)

    print("Saved:", filename)


def draw_shape(surface, tool, color, start, end, size):
    if tool == "line":
        pygame.draw.line(surface, color, start, end, size)

    elif tool == "rectangle":
        draw_rectangle(surface, color, start, end, size)

    elif tool == "circle":
        draw_circle(surface, color, start, end, size)

    elif tool == "square":
        draw_square(surface, color, start, end, size)

    elif tool == "right_triangle":
        draw_right_triangle(surface, color, start, end, size)

    elif tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, color, start, end, size)

    elif tool == "rhombus":
        draw_rhombus(surface, color, start, end, size)


def check_button_click(pos):
    global current_tool
    global current_color
    global brush_size
    global text_active
    global text_value
    global text_pos

    for button in buttons:
        if button["rect"].collidepoint(pos):

            if button["type"] == "tool":
                current_tool = button["tool"]

                if current_tool != "text":
                    text_active = False
                    text_value = ""
                    text_pos = None

            elif button["type"] == "size":
                brush_size = button["size"]

            elif button["type"] == "color":
                current_color = button["color"]

            elif button["type"] == "save":
                save_canvas()

            return True

    return False


def draw_toolbar():
    pygame.draw.rect(screen, (235, 235, 235), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    pygame.draw.line(
        screen,
        (150, 150, 150),
        (0, TOOLBAR_HEIGHT),
        (WIDTH, TOOLBAR_HEIGHT),
        2
    )

    for button in buttons:
        rect = button["rect"]

        if button["type"] == "tool":
            if button["tool"] == current_tool:
                color = (170, 200, 255)
            else:
                color = (220, 220, 220)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 2)

            text = small_font.render(button["label"], True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        elif button["type"] == "size":
            if button["size"] == brush_size:
                color = (170, 255, 180)
            else:
                color = (220, 220, 220)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 2)

            text = small_font.render(button["label"], True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        elif button["type"] == "color":
            pygame.draw.rect(screen, button["color"], rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            if button["color"] == current_color:
                pygame.draw.rect(screen, (255, 0, 0), rect, 4)

        elif button["type"] == "save":
            pygame.draw.rect(screen, (220, 220, 220), rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 2)

            text = small_font.render(button["label"], True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    info = "Tool: " + current_tool + " | Brush: " + str(brush_size) + " px | 1=2px, 2=5px, 3=10px | Ctrl+S=Save | ESC=Exit"
    text = small_font.render(info, True, (40, 40, 40))
    screen.blit(text, (10, 90))


def draw_text_preview(surface):
    if text_active and text_pos is not None:
        text_surface = text_font.render(text_value, True, current_color)
        surface.blit(text_surface, text_pos)

        cursor_x = text_pos[0] + text_surface.get_width() + 2
        cursor_y = text_pos[1]

        pygame.draw.line(
            surface,
            current_color,
            (cursor_x, cursor_y),
            (cursor_x, cursor_y + 32),
            2
        )


def draw_screen():
    screen.fill((255, 255, 255))

    preview = canvas.copy()

    if is_drawing and start_pos is not None and current_pos is not None:
        if current_tool not in ["pencil", "eraser"]:
            draw_shape(preview, current_tool, current_color, start_pos, current_pos, brush_size)

    draw_text_preview(preview)

    screen.blit(preview, (0, TOOLBAR_HEIGHT))

    draw_toolbar()

    pygame.display.flip()


create_buttons()

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if text_active:
                if event.key == pygame.K_RETURN:
                    if text_value != "" and text_pos is not None:
                        text_surface = text_font.render(text_value, True, current_color)
                        canvas.blit(text_surface, text_pos)

                    text_active = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

                elif event.key == pygame.K_1:
                    brush_size = 2

                elif event.key == pygame.K_2:
                    brush_size = 5

                elif event.key == pygame.K_3:
                    brush_size = 10

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if not is_on_canvas(mouse_pos):
                    check_button_click(mouse_pos)

                else:
                    canvas_pos = screen_to_canvas(mouse_pos)

                    if current_tool == "fill":
                        flood_fill(canvas, canvas_pos, current_color)

                    elif current_tool == "text":
                        text_active = True
                        text_pos = canvas_pos
                        text_value = ""

                    else:
                        is_drawing = True
                        start_pos = canvas_pos
                        current_pos = canvas_pos
                        last_pos = canvas_pos

                        if current_tool == "pencil":
                            pygame.draw.line(canvas, current_color, canvas_pos, canvas_pos, brush_size)

                        elif current_tool == "eraser":
                            pygame.draw.line(canvas, (255, 255, 255), canvas_pos, canvas_pos, brush_size)

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

            if is_drawing and is_on_canvas(mouse_pos):
                canvas_pos = screen_to_canvas(mouse_pos)
                current_pos = canvas_pos

                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

                elif current_tool == "eraser":
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pos = event.pos

                if is_drawing and is_on_canvas(mouse_pos):
                    canvas_pos = screen_to_canvas(mouse_pos)
                    current_pos = canvas_pos

                    if current_tool not in ["pencil", "eraser"]:
                        draw_shape(canvas, current_tool, current_color, start_pos, current_pos, brush_size)

                is_drawing = False
                start_pos = None
                current_pos = None
                last_pos = None

    draw_screen()
    clock.tick(60)

pygame.quit()
sys.exit()