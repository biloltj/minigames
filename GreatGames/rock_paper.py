import pygame
import random
import sys

# -------------------------------
# Setup
# -------------------------------
pygame.init()
WIDTH, HEIGHT = 700, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Lizard Spock")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("consolas", 40)
font = pygame.font.SysFont("consolas", 24)
big_font = pygame.font.SysFont("consolas", 32)

# Colors
BG = (20, 20, 35)
WHITE = (240, 240, 240)
PURPLE = (170, 90, 255)
BLUE = (90, 180, 255)
RED = (255, 90, 90)
GREEN = (90, 255, 140)

# -------------------------------
# Game Logic
# -------------------------------
choices = ["rock", "Spock", "paper", "lizard", "scissors"]

win_map = {
    ("scissors", "paper"),
    ("paper", "rock"),
    ("rock", "lizard"),
    ("lizard", "Spock"),
    ("Spock", "scissors"),
    ("scissors", "lizard"),
    ("lizard", "paper"),
    ("paper", "Spock"),
    ("Spock", "rock"),
    ("rock", "scissors")
}

player_score = 0
computer_score = 0
message = "Choose your move!"
player_choice = None
computer_choice = None


def get_winner(p, c):
    if p == c:
        return "tie"
    if (p, c) in win_map:
        return "player"
    return "computer"


# -------------------------------
# UI Button Class
# -------------------------------
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=10)
        label = font.render(self.text, True, WHITE)
        screen.blit(label, (
            self.rect.centerx - label.get_width() // 2,
            self.rect.centery - label.get_height() // 2
        ))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# -------------------------------
# Create Buttons
# -------------------------------
buttons = []
start_x = 60
for i, name in enumerate(choices):
    buttons.append(Button(name, start_x + i * 120, 330, 110, 45))


# -------------------------------
# Main Loop
# -------------------------------
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
            if event.key == pygame.K_r:
                player_score = computer_score = 0
                message = "Scores reset!"

        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                if b.clicked(event.pos):
                    player_choice = b.text
                    computer_choice = random.choice(choices)
                    result = get_winner(player_choice, computer_choice)

                    if result == "player":
                        player_score += 1
                        message = "You win!"
                    elif result == "computer":
                        computer_score += 1
                        message = "Computer wins!"
                    else:
                        message = "It's a tie!"

    # -------------------------------
    # Draw UI
    # -------------------------------
    title = title_font.render("Rock Paper Scissors Lizard Spock", True, PURPLE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # Scores
    score_text = font.render(
        f"Player: {player_score}   Computer: {computer_score}",
        True, WHITE
    )
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 80))

    # Choices
    if player_choice:
        p_text = big_font.render(f"You chose: {player_choice}", True, GREEN)
        c_text = big_font.render(f"Computer chose: {computer_choice}", True, RED)
        screen.blit(p_text, (60, 150))
        screen.blit(c_text, (60, 200))

    # Result message
    msg = big_font.render(message, True, WHITE)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 260))

    # Buttons
    for b in buttons:
        b.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
