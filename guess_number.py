import random, time

def play_game():
    print("\n🎯 Welcome to Guess the Number!")
    print("Choose difficulty:")
    print("1. Easy (1-10)\n2. Medium (1-50)\n3. Hard (1-100)")

    choice = input("> ")
    if choice == '1': limit = 10
    elif choice == '2': limit = 50
    else: limit = 100

    number = random.randint(1, limit)
    attempts = 0

    start_time = time.time()

    while True:
        guess = input(f"Enter a number between 1 and {limit}: ")
        if not guess.isdigit():
            print("❌ Enter a number!")
            continue
        guess = int(guess)
        attempts += 1

        if guess < number:
            print("⬇ Too low!")
        elif guess > number:
            print("⬆ Too high!")
        else:
            duration = int(time.time() - start_time)
            print(f"🎉 Correct! You got it in {attempts} tries and {duration}s!")
            score = max(100 - (attempts * 5 + duration), 0)
            print(f"🏆 Your score: {score}")
            break

while True:
    play_game()
    again = input("Play again? (y/n): ").lower()
    if again != 'y':
        print("👋 Thanks for playing!")
        break
