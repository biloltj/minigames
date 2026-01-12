import pygame
from utils import angle_to_vector
from entities.sprite import Sprite

class Ship:
    def __init__(self, pos, image):
        self.pos = list(pos)
        self.vel = [0, 0]
        self.angle = 0
        self.angle_vel = 0
        self.thrust = False
        self.image = image
        self.radius = 35
        self.shield = False
        self.rapid_fire = False

    def update(self, w, h):
        self.angle += self.angle_vel
        if self.thrust:
            fwd = angle_to_vector(self.angle)
            self.vel[0] += fwd[0] * 0.15
            self.vel[1] += fwd[1] * 0.15

        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        self.pos[0] = (self.pos[0] + self.vel[0]) % w
        self.pos[1] = (self.pos[1] + self.vel[1]) % h

    def draw(self, screen):
        rot = pygame.transform.rotate(self.image, -self.angle * 57.3)
        screen.blit(rot, rot.get_rect(center=self.pos))

    def shoot(self, missile_img):
        fwd = angle_to_vector(self.angle)
        vel = [self.vel[0] + 7*fwd[0], self.vel[1] + 7*fwd[1]]
        return Sprite(self.pos[:], vel, missile_img, 4, 60)
