import pygame
from settings import GRAVITY, PLAYER_SPEED, JUMP_STRENGTH

class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.velocity_y = 0
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def update(self):
        self.handle_input()
        self.apply_gravity()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
