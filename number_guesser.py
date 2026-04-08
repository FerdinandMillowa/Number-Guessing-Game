import random
import time
import json
import os

HIGH_SCORE_FILE = "high_scores.json"

def load_high_scores():
    if not os.path.exists(HIGH_SCORE_FILE):
        return {"Easy": None, "Medium": None, "Hard": None}
    with open(HIGH_SCORE_FILE, "r") as f:
        return json.load(f)

def save_high_score(difficulty, attempts):
    scores = load_high_scores()
    current_best = scores.get(difficulty)
    
    # If no high score exists or current attempt is better (fewer tries)
    if current_best is None or attempts < current_best:
        scores[difficulty] = attempts
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=4)
        return True
    return False

def play_round():
    print("\n" + "="*30)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    # 1. Difficulty Selection
    print("\nPlease select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")
    
    choice = input("\nEnter your choice (1-3): ")
    difficulties = {"1": ("Easy", 10), "2": ("Medium", 5), "3": ("Hard", 3)}
    
    if choice not in difficulties:
        print("Invalid choice. Defaulting to Medium.")
        diff_name, chances = difficulties["2"]
    else:
        diff_name, chances = difficulties[choice]
        
    print(f"\nGreat! You have selected the {diff_name} difficulty level.")
    print("Let's start the game!")

    # 2. Game Setup
    secret_number = random.randint(1, 100)
    attempts = 0
    start_time = time.time() # Start the timer

    # 3. Guessing Loop
    while attempts < chances:
        try:
            guess = int(input("\nEnter your guess: "))
        except ValueError:
            print("Please enter a valid number!")
            continue
            
        attempts += 1
        
        if guess == secret_number:
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            print(f"Congratulations! You guessed the correct number in {attempts} attempts.")
            print(f"Time taken: {duration} seconds.")
            
            if save_high_score(diff_name, attempts):
                print(f"NEW HIGH SCORE for {diff_name}!")
            return
        
        elif guess < secret_number:
            print(f"Incorrect! The number is greater than {guess}.")
        else:
            print(f"Incorrect! The number is less than {guess}.")
            
        print(f"Chances remaining: {chances - attempts}")

    print(f"\nGame Over! You ran out of chances. The number was {secret_number}.")

def main():
    while True:
        play_round()
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != 'yes' and play_again != 'y':
            print("Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()