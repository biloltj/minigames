import pygame
from settings import ENEMY_SIZE

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *ENEMY_SIZE)
        self.direction = 1
        self.speed = 2

    def update(self, platforms):
        self.rect.x += self.speed * self.direction

        for p in platforms:
            if self.rect.colliderect(p):
                self.direction *= -1
                self.rect.x += self.speed * self.direction

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen, (128, 0, 128),
            self.rect.move(-camera.offset_x, 0)
        )
