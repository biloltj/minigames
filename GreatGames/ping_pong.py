import pygame
import random
import sys
import math

# -------------------------------
# Config
# -------------------------------
WIDTH, HEIGHT = 700, 450
BALL_RADIUS = 10
PAD_WIDTH = 12
PAD_HEIGHT = 90
FPS = 60
WIN_SCORE = 7

# Colors
BG = (10, 10, 25)
WHITE = (245, 245, 245)
NEON_PURPLE = (180, 90, 255)
NEON_BLUE = (80, 180, 255)
NEON_RED = (255, 90, 90)

# -------------------------------
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Pong")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("consolas", 64)
font_small = pygame.font.SysFont("consolas", 24)

# -------------------------------
# Sounds
# -------------------------------
bounce_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x00'*1000))
score_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x00'*3000))

# -------------------------------
# Game Objects
# -------------------------------
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]

player = pygame.Rect(30, HEIGHT // 2 - PAD_HEIGHT // 2, PAD_WIDTH, PAD_HEIGHT)
ai = pygame.Rect(WIDTH - 42, HEIGHT // 2 - PAD_HEIGHT // 2, PAD_WIDTH, PAD_HEIGHT)

player_vel = 0
player_score = 0
ai_score = 0

game_over = False


# -------------------------------
def spawn_ball():
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_vel = [
        random.choice([-1, 1]) * random.randint(4, 6),
        random.choice([-4, -3, 3, 4])
    ]


def reset_game():
    global player_score, ai_score, game_over
    player_score = ai_score = 0
    game_over = False
    spawn_ball()


# -------------------------------
def draw_glow_circle(pos, radius, color):
    for i in range(8, 0, -1):
        alpha = 20 * i
        surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(
            surf, (*color, alpha),
            (radius * 2, radius * 2),
            radius + i * 2
        )
        screen.blit(surf, (pos[0] - radius * 2, pos[1] - radius * 2))


def draw_glow_rect(rect, color):
    for i in range(6, 0, -1):
        glow = pygame.Surface((rect.width + i * 6, rect.height + i * 6), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*color, 20), glow.get_rect(), border_radius=8)
        screen.blit(glow, (rect.x - i * 3, rect.y - i * 3))


# -------------------------------
reset_game()
running = True

while running:
    clock.tick(FPS)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                reset_game()

            if event.key == pygame.K_w:
                player_vel = -7
            if event.key == pygame.K_s:
                player_vel = 7

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                player_vel = 0

    if not game_over:
        # Player movement
        player.y += player_vel
        player.y = max(0, min(HEIGHT - PAD_HEIGHT, player.y))

        # AI movement (smart but beatable)
        ai_speed = 5 + (player_score + ai_score) * 0.3
        if ai.centery < ball_pos[1]:
            ai.y += ai_speed
        elif ai.centery > ball_pos[1]:
            ai.y -= ai_speed
        ai.y = max(0, min(HEIGHT - PAD_HEIGHT, ai.y))

        # Ball movement
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
            ball_vel[1] *= -1
            bounce_sound.play()

        ball_rect = pygame.Rect(
            ball_pos[0] - BALL_RADIUS,
            ball_pos[1] - BALL_RADIUS,
            BALL_RADIUS * 2,
            BALL_RADIUS * 2
        )

        if ball_rect.colliderect(player) and ball_vel[0] < 0:
            ball_vel[0] *= -1.1
            bounce_sound.play()

        if ball_rect.colliderect(ai) and ball_vel[0] > 0:
            ball_vel[0] *= -1.1
            bounce_sound.play()

        # Scoring
        if ball_pos[0] < 0:
            ai_score += 1
            score_sound.play()
            spawn_ball()

        if ball_pos[0] > WIDTH:
            player_score += 1
            score_sound.play()
            spawn_ball()

        if player_score >= WIN_SCORE or ai_score >= WIN_SCORE:
            game_over = True

    # -------------------------------
    # Draw
    # -------------------------------
    for y in range(0, HEIGHT, 25):
        pygame.draw.line(screen, NEON_PURPLE, (WIDTH // 2, y), (WIDTH // 2, y + 12), 2)

    draw_glow_rect(player, NEON_BLUE)
    draw_glow_rect(ai, NEON_RED)

    pygame.draw.rect(screen, WHITE, player, border_radius=6)
    pygame.draw.rect(screen, WHITE, ai, border_radius=6)

    draw_glow_circle(ball_pos, BALL_RADIUS, NEON_PURPLE)
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_RADIUS)

    score_text = font_big.render(f"{player_score}   {ai_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    if game_over:
        winner = "YOU WIN!" if player_score > ai_score else "AI WINS!"
        win_text = font_big.render(winner, True, NEON_PURPLE)
        hint = font_small.render("Press R to Restart", True, WHITE)

        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
