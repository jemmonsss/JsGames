import pygame
import random
import sys
import os

# Initialize mixer with low latency settings
pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BG_COLOR = (20, 20, 20)

# Paddle and ball dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15

# Audio setup
AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), "pong")

def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join(AUDIO_FOLDER, name))
    except pygame.error:
        return None

SOUND_HIT = load_sound("hit.wav")
SOUND_SCORE = load_sound("score.wav")
SOUND_WIN = load_sound("win.wav")
SOUND_WALL = load_sound("wall.wav")

# Fonts and clock
font = pygame.font.SysFont("consolas", 32)
clock = pygame.time.Clock()

# Utility drawing function
def draw_text(text, y, win, color=WHITE, center=True):
    render = font.render(text, True, color)
    rect = render.get_rect(midtop=(WIDTH // 2, y)) if center else render.get_rect(topleft=(20, y))
    win.blit(render, rect)

# Pause screen
def pause_screen(win):
    draw_text("Paused - P to Resume | ESC to Menu", HEIGHT // 2, win)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "resume"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"

# Start ball with random direction and velocity
def ball_start():
    dir_x = random.choice([-1, 1])
    dir_y = random.uniform(-1, 1)
    return [WIDTH / 2, HEIGHT / 2], [dir_x * random.uniform(4, 5), dir_y * random.uniform(3, 4)]

# Menu for selecting number of players
def choose_mode(win):
    options = ["1 Player", "2 Player"]
    selected = 0
    while True:
        win.fill(BG_COLOR)
        draw_text("Select Mode", 80, win)
        for i, opt in enumerate(options):
            color = (0, 200, 200) if i == selected else WHITE
            draw_text(opt, 180 + i * 60, win, color)
        draw_text("ESC to Quit", HEIGHT - 40, win, center=False)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN:
                    return options[selected]
                elif e.key == pygame.K_ESCAPE:
                    return None

# Menu for selecting difficulty (1P)
def choose_difficulty(win):
    levels = [("Easy", 5, 6), ("Medium", 7, 7.5), ("Hard", 9, 9)]
    selected = 0
    while True:
        win.fill(BG_COLOR)
        draw_text("Select Difficulty", 80, win)
        for i, (label, _, _) in enumerate(levels):
            color = (0, 200, 200) if i == selected else WHITE
            draw_text(label, 180 + i * 60, win, color)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                elif e.key == pygame.K_RETURN:
                    return levels[selected]
                elif e.key == pygame.K_ESCAPE:
                    return None

# Menu for selecting score limit (2P)
def choose_win_score(win):
    scores = [10, 15, 20]
    selected = 0
    while True:
        win.fill(BG_COLOR)
        draw_text("Select Win Score", 80, win)
        for i, score in enumerate(scores):
            color = (0, 200, 200) if i == selected else WHITE
            draw_text(f"First to {score}", 180 + i * 60, win, color)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(scores)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(scores)
                elif e.key == pygame.K_RETURN:
                    return scores[selected]
                elif e.key == pygame.K_ESCAPE:
                    return None

# Main game loop
def game_loop(mode, paddle_speed, ball_speed, win_score, is_ai, win):
    paddle1 = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_pos, ball_vel = ball_start()
    score1 = score2 = 0

    while True:
        dt = clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if pause_screen(win) == "menu":
                    return

        # Player 1 control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1.top > 0:
            paddle1.y -= paddle_speed
        if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
            paddle1.y += paddle_speed

        # Player 2 or AI control
        if is_ai:
            if abs(paddle2.centery - ball_pos[1]) > 10:
                if paddle2.centery < ball_pos[1] and paddle2.bottom < HEIGHT:
                    paddle2.y += paddle_speed
                elif paddle2.centery > ball_pos[1] and paddle2.top > 0:
                    paddle2.y -= paddle_speed
        else:
            if keys[pygame.K_UP] and paddle2.top > 0:
                paddle2.y -= paddle_speed
            if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
                paddle2.y += paddle_speed

        # Clamp paddles
        paddle1.y = max(0, min(paddle1.y, HEIGHT - PADDLE_HEIGHT))
        paddle2.y = max(0, min(paddle2.y, HEIGHT - PADDLE_HEIGHT))

        # Ball movement
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        ball = pygame.Rect(int(ball_pos[0]), int(ball_pos[1]), BALL_SIZE, BALL_SIZE)

        # Wall bounce
        if ball.top <= 0:
            ball.top = 0
            ball_vel[1] *= -1
            if SOUND_WALL: SOUND_WALL.play()
        elif ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_vel[1] *= -1
            if SOUND_WALL: SOUND_WALL.play()

        # Paddle collisions
        if ball.colliderect(paddle1) and ball_vel[0] < 0:
            offset = (ball.centery - paddle1.centery) / (PADDLE_HEIGHT / 2)
            ball_vel[0] *= -1.05
            ball_vel[1] = offset * ball_speed
            if SOUND_HIT: SOUND_HIT.play()

        if ball.colliderect(paddle2) and ball_vel[0] > 0:
            offset = (ball.centery - paddle2.centery) / (PADDLE_HEIGHT / 2)
            ball_vel[0] *= -1.05
            ball_vel[1] = offset * ball_speed
            if SOUND_HIT: SOUND_HIT.play()

        # Scoring
        if ball.left <= 0:
            score2 += 1
            if SOUND_SCORE: SOUND_SCORE.play()
            ball_pos, ball_vel = ball_start()

        if ball.right >= WIDTH:
            score1 += 1
            if SOUND_SCORE: SOUND_SCORE.play()
            ball_pos, ball_vel = ball_start()

        # Drawing
        win.fill(BG_COLOR)
        pygame.draw.rect(win, WHITE, paddle1)
        pygame.draw.rect(win, WHITE, paddle2)
        pygame.draw.ellipse(win, WHITE, ball)
        pygame.draw.aaline(win, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        draw_text(f"{score1} : {score2}", 20, win)

        # Win condition
        if score1 >= win_score:
            draw_text("Player 1 Wins!", HEIGHT // 2, win)
            if SOUND_WIN: SOUND_WIN.play()
            pygame.display.flip()
            pygame.time.wait(2000)
            return
        elif score2 >= win_score:
            winner = "Player 2" if not is_ai else "AI"
            draw_text(f"{winner} Wins!", HEIGHT // 2, win)
            if SOUND_WIN: SOUND_WIN.play()
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        pygame.display.flip()

# Entry point
def launch():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    while True:
        mode = choose_mode(win)
        if mode is None:
            break

        if mode == "1 Player":
            diff = choose_difficulty(win)
            if not diff:
                continue
            _, paddle_speed, ball_speed = diff
            game_loop(mode, paddle_speed, ball_speed, 10, is_ai=True, win=win)

        elif mode == "2 Player":
            win_score = choose_win_score(win)
            if not win_score:
                continue
            game_loop(mode, 7, 6, win_score, is_ai=False, win=win)

if __name__ == "__main__":
    launch()
