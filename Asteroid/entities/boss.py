from entities.sprite import Sprite
from settings import BOSS_RADIUS

class Boss(Sprite):
    def __init__(self, pos, image):
        super().__init__(pos, [1.5, 0], image, BOSS_RADIUS)
        self.health = 30

    def hit(self):
        self.health -= 1
        return self.health <= 0
