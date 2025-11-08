import random

ART = {
    'rock': "✊",
    'paper': "✋",
    'scissors': "✌️"
}
options = ['rock', 'paper', 'scissors']

def play_match():
    print("\n🎮 Rock Paper Scissors - Best of 5")
    user_score = comp_score = 0

    while user_score < 3 and comp_score < 3:
        user = input("Choose rock/paper/scissors: ").lower()
        if user not in options:
            print("Please,type word fully!")
            continue

        comp = random.choice(options)
        print(f"You: {ART[user]}  vs  Computer: {ART[comp]}")

        if user == comp:
            print("🤝 Draw!")
        elif (user == 'rock' and comp == 'scissors') or \
             (user == 'paper' and comp == 'rock') or \
             (user == 'scissors' and comp == 'paper'):
            print("✅ You win this round!")
            user_score += 1
        else:
            print("💥 You lose this round.")
            comp_score += 1

        print(f"Score: You {user_score} - {comp_score} Computer\n")

    print("🏆 You won!" if user_score > comp_score else "😢 Computer wins!")

play_match()
