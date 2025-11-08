import pygame, sys, random

# Initialize Pygame
pygame.init()
W, H = 400, 500
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("2048 Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Colors
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Game constants
GRID_SIZE = 4
TILE_SIZE = W // GRID_SIZE
MARGIN = 5

def draw_board(board, score):
    win.fill(BACKGROUND_COLOR)
    # Draw tiles
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = board[i][j]
            rect = pygame.Rect(j*TILE_SIZE + MARGIN, i*TILE_SIZE + MARGIN + 100,
                               TILE_SIZE - 2*MARGIN, TILE_SIZE - 2*MARGIN)
            color = TILE_COLORS.get(value, (60, 58, 50)) if value != 0 else EMPTY_COLOR
            pygame.draw.rect(win, color, rect)
            if value != 0:
                text = font.render(str(value), True, (0,0,0))
                text_rect = text.get_rect(center=rect.center)
                win.blit(text, text_rect)
    # Draw score
    score_text = font.render(f"Score: {score}", True, (0,0,0))
    win.blit(score_text, (10, 10))
    pygame.display.update()

def add_new_tile(board):
    empty = [(i,j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j]==0]
    if empty:
        i,j = random.choice(empty)
        board[i][j] = 2 if random.random() < 0.9 else 4

def slide_left(row):
    new_row = [i for i in row if i != 0]
    score = 0
    i = 0
    while i < len(new_row)-1:
        if new_row[i] == new_row[i+1]:
            new_row[i] *= 2
            score += new_row[i]
            new_row.pop(i+1)
            new_row.append(0)
        i += 1
    new_row += [0]*(GRID_SIZE - len(new_row))
    return new_row, score

def move(board, direction):
    score = 0
    moved = False
    if direction == 'UP':
        board = list(map(list, zip(*board)))
        for i in range(GRID_SIZE):
            new_row, gained = slide_left(board[i])
            if new_row != board[i]:
                moved = True
            board[i] = new_row
            score += gained
        board = list(map(list, zip(*board)))
    elif direction == 'DOWN':
        board = list(map(list, zip(*board)))
        for i in range(GRID_SIZE):
            board[i].reverse()
            new_row, gained = slide_left(board[i])
            board[i] = new_row[::-1]
            if new_row[::-1] != board[i]:
                moved = True
            score += gained
        board = list(map(list, zip(*board)))
    elif direction == 'LEFT':
        for i in range(GRID_SIZE):
            new_row, gained = slide_left(board[i])
            if new_row != board[i]:
                moved = True
            board[i] = new_row
            score += gained
    elif direction == 'RIGHT':
        for i in range(GRID_SIZE):
            board[i].reverse()
            new_row, gained = slide_left(board[i])
            board[i] = new_row[::-1]
            if new_row[::-1] != board[i]:
                moved = True
            score += gained
    return board, moved, score

def is_game_over(board):
    if any(0 in row for row in board):
        return False
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE-1):
            if board[i][j]==board[i][j+1] or board[j][i]==board[j+1][i]:
                return False
    return True

def main():
    board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    score = 0

    while True:
        draw_board(board, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                direction = None
                if event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'
                elif event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if direction:
                    board, moved, gained = move(board, direction)
                    if moved:
                        score += gained
                        add_new_tile(board)
                    if is_game_over(board):
                        draw_board(board, score)
                        print("Game Over!")
                        # Wait for Restart or Quit
                        waiting = True
                        while waiting:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if e.type == pygame.KEYDOWN:
                                    if e.key == pygame.K_r:
                                        main()
                                    if e.key == pygame.K_q:
                                        pygame.quit()
                                        sys.exit()
        clock.tick(60)

if __name__ == "__main__":
    main()
