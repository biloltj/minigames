class Sprite:
    def __init__(self, pos, vel, image, radius, lifespan=None):
        self.pos = list(pos)
        self.vel = list(vel)
        self.image = image
        self.radius = radius
        self.age = 0
        self.lifespan = lifespan

    def update(self, w, h):
        self.pos[0] = (self.pos[0] + self.vel[0]) % w
        self.pos[1] = (self.pos[1] + self.vel[1]) % h
        self.age += 1
        return self.lifespan and self.age > self.lifespan

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.pos))
