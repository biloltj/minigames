import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from player import Player
from level import Level

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mario-Style Platformer")
    clock = pygame.time.Clock()

    player = Player(100, 300)
    level = Level()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()
        level.handle_collisions(player)

        screen.fill((135, 206, 235))  # sky blue
        level.draw(screen)
        player.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
