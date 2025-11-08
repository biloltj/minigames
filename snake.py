import pygame, random, sys


pygame.init()
W, H = 600, 400
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("🐍 Snake Game by Bilol")
clock = pygame.time.Clock()


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
WHITE = (255, 255, 255)

def main_game():
    snake = [(100, 50), (90, 50), (80, 50)]
    direction = 'RIGHT'
    food = (random.randrange(1, W//10)*10, random.randrange(1, H//10)*10)
    lives = 3
    score = 0

    def move_snake():
        nonlocal direction
        x, y = snake[0]
        if direction == 'UP': y -= 10
        if direction == 'DOWN': y += 10
        if direction == 'LEFT': x -= 10
        if direction == 'RIGHT': x += 10
        new_head = (x, y)
        snake.insert(0, new_head)
        if new_head == food:
            return True
        else:
            snake.pop()
            return False

    def check_collision():
        x, y = snake[0]
        if x < 0 or x >= W or y < 0 or y >= H:
            return True
        if snake[0] in snake[1:]:
            return True
        return False

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != 'DOWN': direction = 'UP'
                if e.key == pygame.K_DOWN and direction != 'UP': direction = 'DOWN'
                if e.key == pygame.K_LEFT and direction != 'RIGHT': direction = 'LEFT'
                if e.key == pygame.K_RIGHT and direction != 'LEFT': direction = 'RIGHT'

        if move_snake():
            score += 1
            food = (random.randrange(1, W//10)*10, random.randrange(1, H//10)*10)

        if check_collision():
            lives -= 1
            if lives == 0:
               
                while True:
                    win.fill(BLACK)
                    font = pygame.font.SysFont(None, 50)
                    text1 = font.render(f"Game Over! Score: {score}", True, WHITE)
                    text2 = font.render("Press R to Restart or Q to Quit", True, WHITE)
                    win.blit(text1, (W//2 - text1.get_width()//2, H//2 - 60))
                    win.blit(text2, (W//2 - text2.get_width()//2, H//2 + 10))
                    pygame.display.update()

                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if e.type == pygame.KEYDOWN:
                            if e.key == pygame.K_r:
                                main_game()  
                            if e.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
            else:
               
                snake = [(100, 50), (90, 50), (80, 50)]
                direction = 'RIGHT'

       
        win.fill(BLACK)
        for x, y in snake:
            pygame.draw.rect(win, GREEN, (x, y, 10, 10))
        pygame.draw.rect(win, RED, (*food, 10, 10))
        pygame.draw.rect(win, WHITE, (0, 0, W, H), 2)

        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {score}  Lives: {lives}", True, WHITE)
        win.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(15)

main_game()
