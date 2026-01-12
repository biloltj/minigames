import pygame
from settings import WIDTH, HEIGHT, FPS
from entities.ship import Ship
from game.game import Game
from game.level import LevelManager

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

assets = {
    "ship": pygame.image.load("assets/double_ship.png").convert_alpha(),
    "asteroid": pygame.image.load("assets/asteroid_blue.png").convert_alpha(),
    "missile": pygame.image.load("assets/shot2.png").convert_alpha(),
    "boss": pygame.image.load("assets/asteroid_blue.png").convert_alpha(),
    "powerup": pygame.image.load("assets/shot2.png").convert_alpha()
}

ship = Ship([WIDTH//2, HEIGHT//2], assets["ship"])
levels = LevelManager()
game = Game(ship, assets, levels)
game.spawn_wave()

running = True
while running:
    clock.tick(FPS)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: ship.angle_vel = -0.05
            if event.key == pygame.K_RIGHT: ship.angle_vel = 0.05
            if event.key == pygame.K_UP: ship.thrust = True
            if event.key == pygame.K_SPACE:
                game.missiles.append(ship.shoot(assets["missile"]))
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                ship.angle_vel = 0
            if event.key == pygame.K_UP:
                ship.thrust = False

    ship.update(WIDTH, HEIGHT)
    ship.draw(screen)
    game.update()

    for a in game.asteroids: a.draw(screen)
    for m in game.missiles: m.draw(screen)
    for p in game.powerups: p.draw(screen)
    if game.boss: game.boss.draw(screen)

    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render(f"Lives: {game.lives}", True, (255,255,255)), (20,20))
    screen.blit(font.render(f"Score: {game.score}", True, (255,255,255)), (650,20))
    screen.blit(font.render(f"Level: {levels.level}", True, (255,255,255)), (350,20))

    pygame.display.flip()

pygame.quit()
