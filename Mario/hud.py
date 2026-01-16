import pygame

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 32)

    def draw(self, screen, player):
        text = self.font.render(
            f"Score: {player.score}   Lives: {player.lives}",
            True, (0, 0, 0)
        )
        screen.blit(text, (10, 10))
