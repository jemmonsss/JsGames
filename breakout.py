import pygame
import random
import sys
import os

# Constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 80, 10
BALL_RADIUS = 8
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
ROWS, COLS = 5, 9
FPS = 60
BG_COLOR = (20, 20, 20)
WHITE = (255, 255, 255)
HIGHLIGHT = (0, 200, 200)
POWERUP_COLORS = {
    'life': (255, 100, 100),
    'big_paddle': (100, 255, 100),
    'sticky': (100, 200, 255),
    'slow': (255, 255, 100),
}

BRICK_COLOR = (200, 100, 200)

# Sound setup
SOUND_FOLDER = os.path.join(os.path.dirname(__file__), "breakout")
def load_sound(name):
    path = os.path.join(SOUND_FOLDER, name)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None

def reset_bricks():
    bricks = []
    total_width = COLS * BRICK_WIDTH + (COLS - 1) * 5
    offset_x = (WIDTH - total_width) // 2
    for row in range(ROWS):
        for col in range(COLS):
            brick = pygame.Rect(offset_x + col * (BRICK_WIDTH + 5), row * (BRICK_HEIGHT + 5) + 40, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick)
    return bricks

def draw_text(win, text, font, color, x, y):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y))
    win.blit(txt, rect)

def show_instructions(win, font):
    instructions = [
        "← → Move paddle",
        "SPACE Launch ball",
        "P Pause/Unpause",
        "ESC Return to menu",
        "Press SPACE to start..."
    ]
    for i, line in enumerate(instructions):
        draw_text(win, line, font, WHITE, WIDTH // 2, HEIGHT // 2 - 60 + i * 24)

def launch():
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout 🥱")
    font = pygame.font.SysFont("consolas", 24)
    clock = pygame.time.Clock()

    # Load sounds
    hit_sound = load_sound("brick_hit.wav")
    paddle_sound = load_sound("paddle_hit.wav")
    powerup_sound = load_sound("powerup.wav")
    lose_life_sound = load_sound("life_lost.wav")
    game_over_sound = load_sound("game_over.wav")

    while True:
        paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = pygame.Rect(paddle.centerx - BALL_RADIUS, paddle.top - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        ball_speed = [0, 0]
        bricks = reset_bricks()
        lives = 3
        score = 0
        playing = False
        sticky_mode = False
        powerups = []
        active_powerups = {}
        level = 1
        show_instructions_once = True

        run = True
        while run:
            clock.tick(FPS)
            win.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_p:
                        paused = True
                        draw_text(win, "Paused", font, HIGHLIGHT, WIDTH // 2, HEIGHT // 2)
                        pygame.display.update()
                        while paused:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif e.type == pygame.KEYDOWN:
                                    if e.key == pygame.K_p:
                                        paused = False
                                    elif e.key == pygame.K_ESCAPE:
                                        return
                    elif event.key == pygame.K_SPACE and not playing:
                        playing = True
                        show_instructions_once = False
                        if ball_speed == [0, 0]:
                            ball_speed = [random.choice([-4, 4]), -4]

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.x -= 6
            if keys[pygame.K_RIGHT]:
                paddle.x += 6
            paddle.x = max(0, min(WIDTH - paddle.width, paddle.x))

            if not playing:
                ball.x = paddle.centerx - BALL_RADIUS
                ball.y = paddle.top - BALL_RADIUS * 2
            else:
                ball.x += ball_speed[0]
                ball.y += ball_speed[1]

            if ball.left <= 0 or ball.right >= WIDTH:
                ball_speed[0] *= -1
            if ball.top <= 0:
                ball_speed[1] *= -1

            if ball.colliderect(paddle):
                if paddle_sound:
                    paddle_sound.play()
                if not sticky_mode:
                    offset = (ball.centerx - paddle.centerx) / (paddle.width / 2)
                    ball_speed[0] += offset * 2
                    ball_speed[0] = max(-6, min(6, ball_speed[0]))
                    ball_speed[1] = -abs(ball_speed[1])
                else:
                    playing = False
                    sticky_mode = False
                    del active_powerups['sticky']
                    ball_speed = [0, 0]
                    ball.x = paddle.centerx - BALL_RADIUS
                    ball.y = paddle.top - BALL_RADIUS * 2

            hit_index = ball.collidelist(bricks)
            if hit_index != -1:
                if hit_sound:
                    hit_sound.play()
                hit_brick = bricks.pop(hit_index)
                score += 1
                if abs(ball.bottom - hit_brick.top) < 10 or abs(ball.top - hit_brick.bottom) < 10:
                    ball_speed[1] *= -1
                else:
                    ball_speed[0] *= -1
                if random.random() < 0.15:
                    ptype = random.choice(list(POWERUP_COLORS.keys()))
                    speed = random.randint(2, 5)
                    powerups.append([hit_brick.centerx, hit_brick.centery, ptype, speed])

            new_powerups = []
            for px, py, ptype, speed in powerups:
                py += speed
                prect = pygame.Rect(px - 10, py - 10, 20, 20)
                pygame.draw.circle(win, POWERUP_COLORS[ptype], prect.center, 10)
                if prect.colliderect(paddle):
                    if powerup_sound:
                        powerup_sound.play()
                    if ptype == 'life':
                        lives += 1
                    elif ptype == 'big_paddle':
                        prev_center = paddle.centerx
                        paddle.width = min(WIDTH, paddle.width + 40)
                        paddle.x = max(0, min(WIDTH - paddle.width, prev_center - paddle.width // 2))
                        active_powerups['big_paddle'] = pygame.time.get_ticks()
                    elif ptype == 'sticky':
                        sticky_mode = True
                        active_powerups['sticky'] = pygame.time.get_ticks()
                    elif ptype == 'slow':
                        ball_speed[0] *= 0.75
                        ball_speed[1] *= 0.75
                        active_powerups['slow'] = pygame.time.get_ticks()
                    continue
                elif py > HEIGHT:
                    continue
                new_powerups.append([px, py, ptype, speed])
            powerups = new_powerups

            # Handle powerup expiration
            now = pygame.time.get_ticks()
            expired = []
            for ptype, start_time in active_powerups.items():
                if now - start_time > 7000:  # 7 seconds duration
                    expired.append(ptype)
            for ptype in expired:
                if ptype == 'big_paddle':
                    paddle.width = max(PADDLE_WIDTH, paddle.width - 40)
                    paddle.x = max(0, min(WIDTH - paddle.width, paddle.x))
                elif ptype == 'slow':
                    ball_speed[0] *= 1.33
                    ball_speed[1] *= 1.33
                del active_powerups[ptype]

            if ball.bottom >= HEIGHT:
                if lose_life_sound:
                    lose_life_sound.play()
                lives -= 1
                if lives == 0:
                    if game_over_sound:
                        game_over_sound.play()
                    draw_text(win, "Game Over", font, (255, 50, 50), WIDTH // 2, HEIGHT // 2)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    return
                else:
                    playing = False
                    ball.x = paddle.centerx - BALL_RADIUS
                    ball.y = paddle.top - BALL_RADIUS * 2
                    ball_speed = [0, 0]

            if not bricks:
                level += 1
                bricks = reset_bricks()
                playing = False
                ball.x = paddle.centerx - BALL_RADIUS
                ball.y = paddle.top - BALL_RADIUS * 2
                ball_speed = [0, 0]

            pygame.draw.rect(win, WHITE, paddle)
            pygame.draw.circle(win, HIGHLIGHT, ball.center, BALL_RADIUS)
            for brick in bricks:
                pygame.draw.rect(win, BRICK_COLOR, brick)
            for px, py, ptype, _ in powerups:
                pygame.draw.circle(win, POWERUP_COLORS[ptype], (px, py), 10)
            draw_text(win, f"Score: {score}  Lives: {lives}  Level: {level}", font, WHITE, WIDTH // 2, 20)
            if not playing and show_instructions_once:
                show_instructions(win, font)
            pygame.display.update()

if __name__ == "__main__":
    while True:
        launch()
