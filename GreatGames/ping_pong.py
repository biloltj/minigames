import pygame
import random
import sys


WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 10
PAD_WIDTH = 10
PAD_HEIGHT = 80
FPS = 60

WHITE = (245, 245, 245)
PURPLE = (170, 90, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 120)
BG = (20, 20, 30)

LEFT = False
RIGHT = True


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 48)

ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]

paddle1 = pygame.Rect(20, HEIGHT // 2 - PAD_HEIGHT // 2, PAD_WIDTH, PAD_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PAD_HEIGHT // 2, PAD_WIDTH, PAD_HEIGHT)

paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0



def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]

    vx = random.randint(4, 6)
    vy = random.choice([-4, -3, 3, 4])

    if direction == LEFT:
        vx = -vx

    ball_vel = [vx, vy]


def new_game():
    global score1, score2
    score1 = score2 = 0
    spawn_ball(random.choice([LEFT, RIGHT]))



def draw():
    screen.fill(BG)

    # Midline
    for y in range(0, HEIGHT, 20):
        pygame.draw.line(screen, PURPLE, (WIDTH // 2, y), (WIDTH // 2, y + 10), 2)

    # Center circle
    pygame.draw.circle(screen, PURPLE, (WIDTH // 2, HEIGHT // 2), 60, 2)

    # Paddles
    pygame.draw.rect(screen, WHITE, paddle1, border_radius=6)
    pygame.draw.rect(screen, WHITE, paddle2, border_radius=6)

    # Ball
    pygame.draw.circle(screen, PURPLE, ball_pos, BALL_RADIUS)
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_RADIUS, 2)

  
    left_text = font.render(str(score1), True, RED)
    right_text = font.render(str(score2), True, GREEN)

    screen.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    screen.blit(right_text, (3 * WIDTH // 4 - right_text.get_width() // 2, 20))



new_game()
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                new_game()

            if event.key == pygame.K_w:
                paddle1_vel = -6
            if event.key == pygame.K_s:
                paddle1_vel = 6
            if event.key == pygame.K_UP:
                paddle2_vel = -6
            if event.key == pygame.K_DOWN:
                paddle2_vel = 6

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle1_vel = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2_vel = 0

    # Paddle movement
    paddle1.y += paddle1_vel
    paddle2.y += paddle2_vel

    paddle1.y = max(0, min(HEIGHT - PAD_HEIGHT, paddle1.y))
    paddle2.y = max(0, min(HEIGHT - PAD_HEIGHT, paddle2.y))

    # Ball movement
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Wall collision
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1

    ball_rect = pygame.Rect(
        ball_pos[0] - BALL_RADIUS,
        ball_pos[1] - BALL_RADIUS,
        BALL_RADIUS * 2,
        BALL_RADIUS * 2,
    )

    # Paddle collision
    if ball_rect.colliderect(paddle1) and ball_vel[0] < 0:
        ball_vel[0] *= -1
        ball_vel[0] += 1

    if ball_rect.colliderect(paddle2) and ball_vel[0] > 0:
        ball_vel[0] *= -1
        ball_vel[0] -= 1

    # Scoring
    if ball_pos[0] < 0:
        score2 += 1
        spawn_ball(RIGHT)

    if ball_pos[0] > WIDTH:
        score1 += 1
        spawn_ball(LEFT)

    draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
