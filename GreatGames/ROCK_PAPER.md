# ✋🖖 Rock Paper Scissors Lizard Spock  
### Neon Arcade Edition (Pygame)

A modern **Pygame-based remake** of the classic *Rock–Paper–Scissors–Lizard–Spock* game with a clean neon interface, sound effects, animations, and score tracking.

Inspired by the expanded rule set popularized by *The Big Bang Theory*.

---

## 🎮 About the Game

Rock–Paper–Scissors–Lizard–Spock is an extension of the classic Rock–Paper–Scissors game designed to reduce ties and add strategic depth.

Each round:
1. The **player chooses one move**
2. The **computer randomly selects a move**
3. The game evaluates the winner using predefined rules
4. Scores and win streaks are updated

---

## 🧠 Game Rules

Each move defeats **two** other moves and loses to **two**.

### Winning Rules
- ✂️ **Scissors** cuts **Paper**
- 📄 **Paper** covers **Rock**
- 🪨 **Rock** crushes **Lizard**
- 🦎 **Lizard** poisons **Spock**
- 🖖 **Spock** smashes **Scissors**
- ✂️ **Scissors** decapitates **Lizard**
- 🦎 **Lizard** eats **Paper**
- 📄 **Paper** disproves **Spock**
- 🖖 **Spock** vaporizes **Rock**
- 🪨 **Rock** crushes **Scissors**

If both players choose the same move, the round is a **tie**.

---

## ✨ Features

- 🎨 Neon-style arcade interface  
- 🖱️ Clickable buttons (no text input required)  
- 🎧 Sound effects for win, lose, and tie  
- ⏳ Animated “computer thinking” delay  
- 📊 Score tracking (Player vs Computer)  
- 🔥 Win streak counter  
- 🔄 Reset anytime  

---

## 🎮 Controls

### Mouse
- **Left Click** → Select a move

### Keyboard
| Key | Action |
|---|---|
| `R` | Reset scores |
| `ESC` | Quit game |

---

## 📦 Requirements

- **Python 3.9+**
- **Pygame 2.x**

Install Pygame:
```bash
pip install pygame
