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
BG_COLOR = (10, 15, 30)
WHITE = (240, 240, 240)
ACCENT = (255, 200, 80)
RED = (255, 80, 80)

# ---------------- INIT ----------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids — Spaceship")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 24)

# ---------------- HELPERS ----------------
def angle_to_vector(angle):
    return math.cos(angle), math.sin(angle)

def wrap_position(pos):
    return pos[0] % WIDTH, pos[1] % HEIGHT

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
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * SHIP_ACCEL
            self.vel[1] += forward[1] * SHIP_ACCEL

        self.vel[0] *= FRICTION
        self.vel[1] *= FRICTION

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.pos[:] = wrap_position(self.pos)

    def draw(self):
        forward = angle_to_vector(self.angle)
        right = angle_to_vector(self.angle + math.pi / 2)

        tip = (self.pos[0] + forward[0] * 20,
               self.pos[1] + forward[1] * 20)

        left = (self.pos[0] - forward[0] * 15 + right[0] * 10,
                self.pos[1] - forward[1] * 15 + right[1] * 10)

        right_pt = (self.pos[0] - forward[0] * 15 - right[0] * 10,
                    self.pos[1] - forward[1] * 15 - right[1] * 10)

        pygame.draw.polygon(screen, WHITE, [tip, left, right_pt], 2)

        if self.thrust:
            flame = (self.pos[0] - forward[0] * 25,
                     self.pos[1] - forward[1] * 25)
            pygame.draw.circle(screen, ACCENT, flame, 5)

    def rotate(self, direction):
        self.angle += direction * 0.08

    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [
            self.pos[0] + forward[0] * 20,
            self.pos[1] + forward[1] * 20
        ]
        missile_vel = [
            self.vel[0] + forward[0] * MISSILE_SPEED,
            self.vel[1] + forward[1] * MISSILE_SPEED
        ]
        return Missile(missile_pos, missile_vel)


class Missile:
    def __init__(self, pos, vel):
        self.pos = pos[:]
        self.vel = vel[:]
        self.life = 60
        self.radius = 3

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[:] = wrap_position(self.pos)
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen, RED, self.pos, self.radius)


class Asteroid:
    def __init__(self):
        self.pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        angle = random.random() * 2 * math.pi
        self.vel = [math.cos(angle) * ASTEROID_SPEED,
                    math.sin(angle) * ASTEROID_SPEED]
        self.radius = random.randint(20, 40)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[:] = wrap_position(self.pos)

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.pos, self.radius, 2)

# ---------------- GAME STATE ----------------
ship = Ship()
missiles = []
asteroids = [Asteroid() for _ in range(5)]
score = 0
lives = 3

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                missiles.append(ship.shoot())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.rotate(-1)
    if keys[pygame.K_RIGHT]:
        ship.rotate(1)
    if keys[pygame.K_UP]:
        ship.thrust = True
    else:
        ship.thrust = False

    # UPDATE
    ship.update()

    for m in missiles[:]:
        m.update()
        if m.life <= 0:
            missiles.remove(m)

    for a in asteroids:
        a.update()

    # DRAW
    ship.draw()
    for m in missiles:
        m.draw()
    for a in asteroids:
        a.draw()

    hud = FONT.render(f"Score: {score}   Lives: {lives}", True, WHITE)
    screen.blit(hud, (20, 20))

    pygame.display.flip()

pygame.quit()
