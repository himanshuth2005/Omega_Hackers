import random
import time

class SpaceWordChallengeCLI:
    def __init__(self):
        self.planet = self.choose_planet()
        self.guessed_letters = []
        self.attempts = 6
        self.start_time = time.time()

    def choose_planet(self):
        planet_list = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
        return random.choice(planet_list)

    def update_display(self):
        displayed_planet = ""
        for letter in self.planet:
            if letter.lower() in self.guessed_letters:
                displayed_planet += letter
            else:
                displayed_planet += "_"
        print(" ".join(displayed_planet))
        return displayed_planet

    def check_guess(self, guess):
        
        if not guess.isalpha() or len(guess) != 1:
            print("Invalid guess. Please enter a single letter.")
            return

        
        if guess in self.guessed_letters:
            print("You already guessed that letter!")
            return

        
        self.guessed_letters.append(guess)

        
        if guess not in self.planet.lower():
            self.attempts -= 1
            print(f"Oops! '{guess}' is not in the planet name. You have {self.attempts} attempts left.")
            if self.attempts == 0:
                print(f"Game Over. You're out of attempts. The correct planet was: {self.planet}")
                return False
        else:
            print("Good guess!")
            self.update_display()

            if "_" not in self.update_display():
                end_time = time.time()
                time_taken = end_time - self.start_time
                score = self.attempts * 10 - int(time_taken)
                print(f"Congratulations! You've guessed the planet in {int(time_taken)} seconds! Your score: {score}")
                return False

        return True

def main():
    game = SpaceWordChallengeCLI()
    print("Welcome to SpaceWord Challenge!")
    print("Guess the name of the planet.")
    game.update_display()

    while game.attempts > 0:
        guess = input("Enter a letter: ").lower()
        if not game.check_guess(guess):
            break

if __name__ == "__main__":
    main()
