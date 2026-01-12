import random
from utils import distance
from entities.asteroid import Asteroid
from entities.boss import Boss
from entities.powerup import PowerUp
from settings import WIDTH, HEIGHT, MAX_ASTEROIDS

class Game:
    def __init__(self, ship, assets, level_mgr):
        self.ship = ship
        self.assets = assets
        self.level_mgr = level_mgr

        self.asteroids = []
        self.missiles = []
        self.powerups = []
        self.boss = None

        self.score = 0
        self.lives = 3

    def spawn_wave(self):
        if self.level_mgr.boss_level():
            self.boss = Boss([WIDTH//2, 100], self.assets["boss"])
        else:
            for _ in range(MAX_ASTEROIDS):
                pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
                self.asteroids.append(
                    Asteroid(pos, self.assets["asteroid"], self.level_mgr.speed())
                )

    def update(self):
        # missiles
        for m in self.missiles[:]:
            if m.update(WIDTH, HEIGHT):
                self.missiles.remove(m)

        # asteroids
        for a in self.asteroids[:]:
            a.update(WIDTH, HEIGHT)
            if distance(a.pos, self.ship.pos) < a.radius + self.ship.radius:
                self.asteroids.remove(a)
                self.lives -= 1

        # missile hits asteroid
        for a in self.asteroids[:]:
            for m in self.missiles[:]:
                if distance(a.pos, m.pos) < a.radius + m.radius:
                    self.asteroids.remove(a)
                    self.missiles.remove(m)
                    self.score += 1
                    if random.random() < 0.1:
                        self.powerups.append(
                            PowerUp(a.pos, self.assets["powerup"])
                        )

        # boss
        if self.boss:
            self.boss.update(WIDTH, HEIGHT)
            for m in self.missiles[:]:
                if distance(self.boss.pos, m.pos) < self.boss.radius + m.radius:
                    self.missiles.remove(m)
                    if self.boss.hit():
                        self.boss = None
                        self.level_mgr.next()

        # powerups
        for p in self.powerups[:]:
            p.update(WIDTH, HEIGHT)
            if distance(p.pos, self.ship.pos) < p.radius + self.ship.radius:
                if p.type == "life":
                    self.lives += 1
                if p.type == "shield":
                    self.ship.shield = True
                if p.type == "rapid":
                    self.ship.rapid_fire = True
                self.powerups.remove(p)

        if not self.asteroids and not self.boss:
            self.level_mgr.next()
            self.spawn_wave()
