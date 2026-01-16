import pygame
from settings import GROUND_Y

class Level:
    def __init__(self):
        self.ground = pygame.Rect(0, GROUND_Y, 800, 100)

    def handle_collisions(self, player):
        if player.rect.colliderect(self.ground):
            player.rect.bottom = self.ground.top
            player.velocity_y = 0
            player.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.ground)
