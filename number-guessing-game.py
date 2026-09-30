#!/usr/bin/env python3
"""Number Guessing Game: pick a difficulty, guess the number, beat your high score.

Run:  python3 number_guessing_game.py
"""
import json
import random
from pathlib import Path

SCORE_FILE = Path(__file__).with_name("highscores.json")

# name: (highest number, allowed guesses, points per unused guess)
LEVELS = {
    "1": ("Easy", 50, 8, 10),
    "2": ("Medium", 100, 7, 20),
    "3": ("Hard", 500, 9, 40),
}


def load_scores():
    try:
        return json.loads(SCORE_FILE.read_text())
    except (OSError, ValueError):
        return {}


def save_scores(scores):
    try:
        SCORE_FILE.write_text(json.dumps(scores, indent=2))
    except OSError:
        print("(Could not save your high score.)")


def ask_int(prompt, low, high):
    """Keep asking until the player types a whole number in range."""
    while True:
        text = input(prompt).strip()
        if not text.lstrip("-").isdigit():
            print(f"  Please type a whole number between {low} and {high}.")
            continue
        value = int(text)
        if low <= value <= high:
            return value
        print(f"  Out of range. Pick a number from {low} to {high}.")


def temperature(diff, top):
    """Hot/cold hint based on how far the guess is from the answer."""
    ratio = diff / top
    if ratio <= 0.03:
        return "Burning hot!"
    if ratio <= 0.10:
        return "Warm"
    if ratio <= 0.25:
        return "Cool"
    return "Cold"


def play(level_key, scores):
    name, top, max_guesses, bonus = LEVELS[level_key]
    secret = random.randint(1, top)
    print(f"\n{name}: I'm thinking of a number from 1 to {top}. You have {max_guesses} guesses.")

    for attempt in range(1, max_guesses + 1):
        guess = ask_int(f"Guess {attempt}/{max_guesses}: ", 1, top)
        if guess == secret:
            score = (max_guesses - attempt + 1) * bonus
            print(f"\nCorrect! You got it in {attempt} {'guess' if attempt == 1 else 'guesses'}. Score: {score}")
            best = scores.get(name, 0)
            if score > best:
                scores[name] = score
                save_scores(scores)
                print(f"New high score for {name}!" if best else f"First high score for {name} saved.")
            else:
                print(f"High score for {name}: {best}")
            return
        direction = "higher" if guess < secret else "lower"
        print(f"  Go {direction}. {temperature(abs(guess - secret), top)}")

    print(f"\nOut of guesses. The number was {secret}.")


def main():
    scores = load_scores()
    print("=== Number Guessing Game ===")
    while True:
        print("\nChoose a difficulty:")
        for key, (name, top, tries, _) in LEVELS.items():
            best = scores.get(name)
            extra = f", best score {best}" if best else ""
            print(f"  {key}) {name}: 1-{top}, {tries} guesses{extra}")
        choice = input("Your choice (1-3, or q to quit): ").strip().lower()
        if choice == "q":
            break
        if choice not in LEVELS:
            print("  Please enter 1, 2, 3 or q.")
            continue
        play(choice, scores)
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            break
    print("Thanks for playing!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nThanks for playing!")