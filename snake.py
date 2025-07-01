import pygame
import random
import os
import sys

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10

# Colors
BG_COLOR = (20, 20, 20)
WHITE = (255, 255, 255)
HIGHLIGHT = (0, 200, 200)
RED = (255, 50, 50)
GREEN = (0, 255, 0)
DARK_GREEN = (10, 40, 10)
GRID_COLOR = (30, 30, 30)
SUBTLE = (150, 150, 150)

# Game modes
MODES = {
    "Classic": True,
    "No Walls": False
}

EAT_SOUND = None
GAME_OVER_SOUND = None
AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), "snake")

def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join(AUDIO_FOLDER, name))
    except pygame.error:
        return None

def setup_audio():
    global EAT_SOUND, GAME_OVER_SOUND
    try:
        pygame.mixer.init()
        EAT_SOUND = load_sound("eat.wav")
        GAME_OVER_SOUND = load_sound("game_over.wav")
    except pygame.error as e:
        print("Sound error:", e)
        EAT_SOUND = None
        GAME_OVER_SOUND = None

def draw_text(text, font, color, surface, x, y):
    if not pygame.display.get_init():
        return
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    surface.blit(render, rect)

def draw_grid(win):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(win, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(win, GRID_COLOR, (0, y), (WIDTH, y))

def random_position(snake):
    while True:
        pos = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
        if pos not in snake:
            return pos

def draw_snake(win, snake):
    for pos in snake:
        rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(win, GREEN, rect)
        pygame.draw.rect(win, DARK_GREEN, rect, 2)

def draw_food(win, pos):
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(win, RED, rect)

def game_over(win, big_font):
    if not pygame.display.get_init():
        return
    if GAME_OVER_SOUND:
        GAME_OVER_SOUND.play()
    win.fill(BG_COLOR)
    draw_text("Game Over", big_font, RED, win, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)

def pause_screen(win, font, clock):
    win.fill(BG_COLOR)
    draw_text("Paused", font, HIGHLIGHT, win, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text("Press P to resume or ESC to menu", font, WHITE, win, WIDTH // 2, HEIGHT // 2 + 20)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "resume"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
        clock.tick(5)

def choose_mode(win, font, big_font):
    selected = 0
    mode_keys = list(MODES.keys())
    while True:
        if not pygame.display.get_init():
            return None
        win.fill(BG_COLOR)
        draw_text("Select Game Mode", big_font, WHITE, win, WIDTH // 2, 50)
        for i, mode in enumerate(mode_keys):
            color = HIGHLIGHT if i == selected else WHITE
            draw_text(mode, font, color, win, WIDTH // 2, 130 + i * 40)
        draw_text("ESC to return", font, SUBTLE, win, WIDTH // 2, HEIGHT - 30)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(mode_keys)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(mode_keys)
                elif event.key == pygame.K_RETURN:
                    return mode_keys[selected]
                elif event.key == pygame.K_ESCAPE:
                    return None

def main(win, mode_name, font, big_font, clock):
    wall_collision = MODES[mode_name]
    snake = [[5, 5]]
    direction = [1, 0]
    food = random_position(snake)

    while True:
        clock.tick(FPS)
        keys_pressed = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys_pressed.append(event.key)
                if event.key == pygame.K_p:
                    state = pause_screen(win, font, clock)
                    if state == "menu":
                        return

        # Apply last valid key in reverse order
        for key in reversed(keys_pressed):
            if key == pygame.K_UP and direction != [0, 1]:
                direction = [0, -1]
                break
            elif key == pygame.K_DOWN and direction != [0, -1]:
                direction = [0, 1]
                break
            elif key == pygame.K_LEFT and direction != [1, 0]:
                direction = [-1, 0]
                break
            elif key == pygame.K_RIGHT and direction != [-1, 0]:
                direction = [1, 0]
                break

        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

        if not wall_collision:
            new_head[0] %= GRID_WIDTH
            new_head[1] %= GRID_HEIGHT
        elif not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            game_over(win, big_font)
            return

        if new_head in snake[:-1]:  # ignore tail only if it's moving
            game_over(win, big_font)
            return

        snake.insert(0, new_head)
        if new_head == food:
            if EAT_SOUND:
                EAT_SOUND.play()
            food = random_position(snake)
        else:
            snake.pop()

        if not pygame.display.get_init():
            return

        win.fill(BG_COLOR)
        draw_grid(win)
        draw_snake(win, snake)
        draw_food(win, food)
        draw_text(f"Score: {len(snake) - 1}", font, HIGHLIGHT, win, 60, 20)
        pygame.display.flip()

def launch():
    pygame.init()
    setup_audio()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake 🐍")
    font = pygame.font.SysFont("consolas", 24)
    big_font = pygame.font.SysFont("consolas", 36)
    clock = pygame.time.Clock()

    while True:
        selected_mode = choose_mode(win, font, big_font)
        if selected_mode:
            main(win, selected_mode, font, big_font, clock)
        else:
            break

    pygame.display.quit()

if __name__ == "__main__":
    launch()
