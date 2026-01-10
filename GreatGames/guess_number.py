import pygame
import random
import math
import sys


pygame.init()
WIDTH, HEIGHT = 600, 420
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Number")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("consolas", 40)
font = pygame.font.SysFont("consolas", 24)
small_font = pygame.font.SysFont("consolas", 20)


BG = (20, 20, 35)
WHITE = (240, 240, 240)
BLUE = (90, 180, 255)
GREEN = (90, 255, 150)
RED = (255, 90, 90)
GRAY = (120, 120, 140)


num_range = 100
secret_number = 0
remaining_guesses = 0
message = ""
input_text = ""
game_over = False

def new_game():
    global secret_number, remaining_guesses, message, input_text, game_over
    secret_number = random.randrange(0, num_range)
    remaining_guesses = int(math.ceil(math.log(num_range, 2)))
    message = f"New game! Guess a number from 0 to {num_range - 1}"
    input_text = ""
    game_over = False

def check_guess(guess):
    global remaining_guesses, message, game_over

    if guess < secret_number:
        message = "Higher!"
    elif guess > secret_number:
        message = "Lower!"
    else:
        message = "Correct! 🎉 Starting new game..."
        game_over = True
        return

    remaining_guesses -= 1

    if remaining_guesses == 0:
        message = f"Out of guesses! Number was {secret_number}"
        game_over = True

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=8)
        label = small_font.render(self.text, True, WHITE)
        screen.blit(label, (
            self.rect.centerx - label.get_width() // 2,
            self.rect.centery - label.get_height() // 2
        ))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

input_box = pygame.Rect(200, 210, 200, 40)

btn_100 = Button("Range [0–100)", 80, 140, 200, 40)
btn_1000 = Button("Range [0–1000)", 320, 140, 200, 40)
btn_new = Button("New Game", 200, 300, 200, 40)


new_game()
running = True

while running:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_RETURN and input_text.isdigit() and not game_over:
                check_guess(int(input_text))
                input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

            elif event.unicode.isdigit() and len(input_text) < 4:
                input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_100.clicked(event.pos):
                num_range = 100
                new_game()

            if btn_1000.clicked(event.pos):
                num_range = 1000
                new_game()

            if btn_new.clicked(event.pos):
                new_game()

    if game_over:
        pygame.time.delay(800)
        new_game()

   
    title = title_font.render("Guess the Number", True, BLUE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    info = font.render(f"Remaining guesses: {remaining_guesses}", True, WHITE)
    screen.blit(info, (WIDTH//2 - info.get_width()//2, 90))

    msg = font.render(message, True, GREEN if "Correct" in message else WHITE)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 180))

    
    pygame.draw.rect(screen, WHITE, input_box, 2, border_radius=6)
    txt = font.render(input_text, True, WHITE)
    screen.blit(txt, (input_box.x + 10, input_box.y + 8))

    hint = small_font.render("Type a number and press Enter", True, GRAY)
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 255))

    btn_100.draw()
    btn_1000.draw()
    btn_new.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
