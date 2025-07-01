import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 4
CELL_SIZE = 80
CELL_PADDING = 10
BG_COLOR = (30, 30, 30)
CELL_COLOR = {
    0: (50, 50, 50),
    2: (240, 228, 217),
    4: (236, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)

pygame.init()
FONT = pygame.font.SysFont("consolas", 28)
BIG_FONT = pygame.font.SysFont("consolas", 40)
clock = pygame.time.Clock()

def new_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    spawn_tile(board)
    spawn_tile(board)
    return board

def spawn_tile(board):
    empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]
    if not empty:
        return
    r, c = random.choice(empty)
    board[r][c] = 4 if random.random() < 0.1 else 2

def draw_board(win, board, score):
    win.fill(BG_COLOR)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = board[r][c]
            rect = pygame.Rect(c * (CELL_SIZE + CELL_PADDING) + 50, r * (CELL_SIZE + CELL_PADDING) + 50, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(win, CELL_COLOR.get(value, (200, 200, 200)), rect)
            if value:
                text = FONT.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                win.blit(text, text_rect)

    score_text = FONT.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))
    pygame.display.update()

def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (GRID_SIZE - len(new_row))
    return new_row

def merge(row):
    score = 0
    for i in range(GRID_SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            score += row[i]
            row[i + 1] = 0
    return row, score

def move_left(board):
    new_board = []
    total_score = 0
    for row in board:
        row = compress(row)
        row, score = merge(row)
        row = compress(row)
        new_board.append(row)
        total_score += score
    return new_board, total_score

def move_right(board):
    reversed_board = [list(reversed(row)) for row in board]
    moved_board, score = move_left(reversed_board)
    return [list(reversed(row)) for row in moved_board], score

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_up(board):
    transposed = transpose(board)
    moved, score = move_left(transposed)
    return transpose(moved), score

def move_down(board):
    transposed = transpose(board)
    moved, score = move_right(transposed)
    return transpose(moved), score

def boards_equal(b1, b2):
    return all(b1[r][c] == b2[r][c] for r in range(GRID_SIZE) for c in range(GRID_SIZE))

def is_game_over(board):
    for move_func in (move_left, move_right, move_up, move_down):
        moved, _ = move_func(board)
        if not boards_equal(board, moved):
            return False
    return True

def launch():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    board = new_board()
    score = 0
    running = True

    while running:
        draw_board(win, board, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                moved = False
                prev_board = [row[:] for row in board]
                if event.key == pygame.K_LEFT:
                    board, gained = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    board, gained = move_right(board)
                elif event.key == pygame.K_UP:
                    board, gained = move_up(board)
                elif event.key == pygame.K_DOWN:
                    board, gained = move_down(board)
                elif event.key == pygame.K_ESCAPE:
                    return
                else:
                    continue

                if not boards_equal(prev_board, board):
                    spawn_tile(board)
                    score += gained

                if is_game_over(board):
                    draw_board(win, board, score)
                    over_text = BIG_FONT.render("Game Over", True, WHITE)
                    win.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    return

        clock.tick(15)

# Optional: run independently
if __name__ == "__main__":
    launch()
