import random
from entities.sprite import Sprite
from settings import ASTEROID_RADIUS

class Asteroid(Sprite):
    def __init__(self, pos, image, speed):
        vel = [random.uniform(-1,1)*speed, random.uniform(-1,1)*speed]
        super().__init__(pos, vel, image, ASTEROID_RADIUS)
