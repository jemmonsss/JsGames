import pygame
import sys
import snake
import pong  
import tfe  
import breakout 


# Constants
WIDTH, HEIGHT = 600, 400
BG_COLOR = (20, 20, 20)
WHITE = (255, 255, 255)
HIGHLIGHT = (0, 200, 200)

pygame.init()

def init_display():
    global win, font, small_font
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Menu")
    font = pygame.font.SysFont("consolas", 28)
    small_font = pygame.font.SysFont("consolas", 18)

menu_options = [
    {"label": "Play Snake", "action": snake.launch},
    {"label": "Play Pong", "action": pong.launch},
    {"label": "Play 2048", "action": tfe.launch},
    {"label": "Play Breakout", "action": breakout.launch},
]

selected = 0

def draw_menu():
    if not pygame.display.get_init():
        return
    win.fill(BG_COLOR)
    title = font.render("Game Launcher", True, WHITE)
    win.blit(title, [WIDTH // 2 - title.get_width() // 2, 40])

    for idx, option in enumerate(menu_options):
        color = HIGHLIGHT if idx == selected else WHITE
        txt = font.render(option["label"], True, color)
        win.blit(txt, [WIDTH // 2 - txt.get_width() // 2, 140 + idx * 50])

    credit = small_font.render("Made by J_emmons_07", True, (100, 100, 100))
    win.blit(credit, [10, HEIGHT - 30])

    pygame.display.update()

def main_menu():
    global selected
    clock = pygame.time.Clock()
    running = True

    while running:
        init_display()  # Reset window size each time the menu opens
        draw_menu()
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        try:
                            menu_options[selected]["action"]()
                        except pygame.error:
                            running = False  # Likely due to window closure
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        waiting = False

            draw_menu()
            clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main_menu()
