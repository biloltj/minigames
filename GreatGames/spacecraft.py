import pygame
import random
import math
import sys

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 900, 600
FPS = 60

FRICTION = 0.99
SHIP_ACCEL = 0.2
MISSILE_SPEED = 7
ASTEROID_SPEED = 2

# Colors
BG = (10, 15, 30)
WHITE = (240, 240, 240)
ACCENT = (255, 200, 80)
RED = (255, 80, 80)
ORANGE = (255, 140, 0)

# ---------------- INIT ----------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids — ML Ready")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 24)
BIG_FONT = pygame.font.SysFont("consolas", 60)

# ---------------- HELPERS ----------------
def angle_to_vector(a):
    return math.cos(a), math.sin(a)

def wrap(pos):
    return [pos[0] % WIDTH, pos[1] % HEIGHT]

def distance(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])

# ---------------- CLASSES ----------------
class Ship:
    def __init__(self):
        self.pos = [WIDTH / 2, HEIGHT / 2]
        self.vel = [0, 0]
        self.angle = 0
        self.thrust = False
        self.radius = 15

    def update(self):
        if self.thrust:
            fx, fy = angle_to_vector(self.angle)
            self.vel[0] += fx * SHIP_ACCEL
            self.vel[1] += fy * SHIP_ACCEL

        self.vel[0] *= FRICTION
        self.vel[1] *= FRICTION

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[:] = wrap(self.pos)

    def draw(self):
        fx, fy = angle_to_vector(self.angle)
        rx, ry = angle_to_vector(self.angle + math.pi / 2)

        tip = (self.pos[0] + fx * 20, self.pos[1] + fy * 20)
        left = (self.pos[0] - fx * 15 + rx * 10,
                self.pos[1] - fy * 15 + ry * 10)
        right = (self.pos[0] - fx * 15 - rx * 10,
                 self.pos[1] - fy * 15 - ry * 10)

        pygame.draw.polygon(screen, WHITE, [tip, left, right], 2)

        if self.thrust:
            flame = (self.pos[0] - fx * 25, self.pos[1] - fy * 25)
            pygame.draw.circle(screen, ACCENT, flame, 5)

    def rotate(self, d):
        self.angle += d * 0.08

    def shoot(self):
        fx, fy = angle_to_vector(self.angle)
        pos = [self.pos[0] + fx * 20, self.pos[1] + fy * 20]
        vel = [self.vel[0] + fx * MISSILE_SPEED,
               self.vel[1] + fy * MISSILE_SPEED]
        return Missile(pos, vel)


class Missile:
    def __init__(self, pos, vel):
        self.pos = pos[:]
        self.vel = vel[:]
        self.life = 60
        self.radius = 3

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[:] = wrap(self.pos)
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen, RED, self.pos, self.radius)


class Asteroid:
    def __init__(self):
        self.pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        ang = random.random() * 2 * math.pi
        self.vel = [math.cos(ang) * ASTEROID_SPEED,
                    math.sin(ang) * ASTEROID_SPEED]
        self.radius = random.randint(20, 40)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[:] = wrap(self.pos)

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.pos, self.radius, 2)


class Explosion:
    def __init__(self, pos):
        self.pos = pos[:]
        self.life = 20
        self.radius = 5

    def update(self):
        self.radius += 3
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen, ORANGE, self.pos, self.radius, 2)

# ---------------- GAME RESET ----------------
def reset_game():
    global ship, missiles, asteroids, explosions, score, lives, game_over
    ship = Ship()
    missiles = []
    asteroids = [Asteroid() for _ in range(6)]
    explosions = []
    score = 0
    lives = 3
    game_over = False

reset_game()

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(FPS)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                missiles.append(ship.shoot())
            if event.key == pygame.K_r and game_over:
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            ship.rotate(-1)
        if keys[pygame.K_RIGHT]:
            ship.rotate(1)
        ship.thrust = keys[pygame.K_UP]

    # UPDATE
    if not game_over:
        ship.update()

        for m in missiles[:]:
            m.update()
            if m.life <= 0:
                missiles.remove(m)

        for a in asteroids:
            a.update()

        for e in explosions[:]:
            e.update()
            if e.life <= 0:
                explosions.remove(e)

        # COLLISIONS — missile vs asteroid
        for m in missiles[:]:
            for a in asteroids[:]:
                if distance(m.pos, a.pos) < a.radius:
                    missiles.remove(m)
                    asteroids.remove(a)
                    explosions.append(Explosion(a.pos))
                    score += 10
                    asteroids.append(Asteroid())
                    break

        # COLLISIONS — ship vs asteroid
        for a in asteroids:
            if distance(ship.pos, a.pos) < a.radius + ship.radius:
                explosions.append(Explosion(ship.pos))
                lives -= 1
                ship = Ship()
                if lives <= 0:
                    game_over = True
                break

    # DRAW
    ship.draw()
    for m in missiles:
        m.draw()
    for a in asteroids:
        a.draw()
    for e in explosions:
        e.draw()

    hud = FONT.render(f"Score: {score}   Lives: {lives}", True, WHITE)
    screen.blit(hud, (20, 20))

    if game_over:
        txt = BIG_FONT.render("GAME OVER", True, RED)
        sub = FONT.render("Press R to Restart", True, WHITE)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()
