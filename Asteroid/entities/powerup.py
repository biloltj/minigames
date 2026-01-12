import random
from entities.sprite import Sprite

class PowerUp(Sprite):
    TYPES = ["shield", "rapid", "life"]

    def __init__(self, pos, image):
        self.type = random.choice(self.TYPES)
        super().__init__(pos, [0,1], image, 20, 600)
