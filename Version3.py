import random
import tkinter as tk
from tkinter import messagebox
import time

class SpaceWordChallenge:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Space Word Challenge")
        self.master.geometry("400x400") 
        self.master.resizable(False, False)
        self.master.configure(bg="#D9E6EB")

        self.label = tk.Label(self.master, text="Space Word Challenge", font=("Arial", 20, "bold"), bg="#D9E6EB", fg="#004466")
        self.label.pack(pady=(20, 10))

        self.planet_frame = tk.Frame(self.master, bg="#D9E6EB")
        self.planet_frame.pack()

        self.planet_label = tk.Label(self.planet_frame, text="", font=("Arial", 18), bg="#D9E6EB", fg="#004466")
        self.planet_label.pack(pady=10)

        self.guess_label = tk.Label(self.master, text="Enter a letter:", font=("Arial", 12), bg="#D9E6EB", fg="#004466")
        self.guess_label.pack()

        self.entry = tk.Entry(self.master, font=("Arial", 12), state=tk.DISABLED)
        self.entry.pack()

        self.entry.bind("<Return>", self.check_guess)  

        self.guess_button = tk.Button(self.master, text="Guess", font=("Arial", 12), bg="#FFD700", fg="#004466", command=self.check_guess, state=tk.DISABLED)
        self.guess_button.pack(pady=10)

        self.start_button = tk.Button(self.master, text="Start", font=("Arial", 12), bg="#FFD700", fg="#004466", command=self.start_game)
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(self.master, text="Reset", font=("Arial", 12), bg="#FFD700", fg="#004466", command=self.reset_game, state=tk.DISABLED)
        self.reset_button.pack(pady=10)

        self.attempts_label = tk.Label(self.master, text="", font=("Arial", 12), bg="#D9E6EB", fg="#004466")
        self.attempts_label.pack()

        self.timer_label = tk.Label(self.master, text="", font=("Arial", 12), bg="#D9E6EB", fg="#004466")
        self.timer_label.pack(side=tk.RIGHT, padx=20, pady=10)

        self.difficulty_label = tk.Label(self.master, text="Difficulty:", font=("Arial", 12), bg="#D9E6EB", fg="#004466")
        self.difficulty_label.pack(side=tk.LEFT, padx=5, pady=10)

        self.difficulty_var = tk.StringVar(self.master)
        self.difficulty_var.set("Easy")
        self.difficulty_menu = tk.OptionMenu(self.master, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.config(font=("Arial", 12), bg="#FFD700", fg="#004466", width=8)
        self.difficulty_menu.pack(side=tk.LEFT, padx=2, pady=10)

        self.planet = ""
        self.guessed_letters = []
        self.attempts = 5
        self.start_time = 0
        self.game_started = False
        self.timer_stopped = False

    def start_game(self):
        self.set_difficulty()
        self.planet = self.choose_planet()
        self.guessed_letters = []
        self.start_time = time.time()
        self.game_started = True
        self.timer_stopped = False
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")
        self.update_display()
        self.update_timer()
        self.difficulty_menu.config(state=tk.DISABLED)  # Disable the difficulty menu

    def reset_game(self):
        self.planet_label.config(text="")
        self.entry.delete(0, tk.END)
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)
        self.game_started = False
        self.attempts_label.pack_forget()
        self.timer_label.config(text="")
        self.timer_stopped = True
        self.difficulty_menu.config(state=tk.NORMAL)  # Enable the difficulty menu

    def choose_planet(self):
        planet_list = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
        return random.choice(planet_list)

    def set_difficulty(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            self.attempts = 5
        elif difficulty == "Medium":
            self.attempts = 4
        elif difficulty == "Hard":
            self.attempts = 3

    def update_display(self):
        displayed_planet = " ".join(letter if letter.lower() in self.guessed_letters or not letter.isalpha() else "_" for letter in self.planet)
        self.planet_label.config(text=displayed_planet)

        self.attempts_label.config(text=f"Attempts left: {self.attempts}")

    def update_timer(self):
        if self.game_started and not self.timer_stopped:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time} s")
            self.master.after(1000, self.update_timer)

    def check_guess(self, event=None):
        if not self.game_started:
            messagebox.showinfo("Game Not Started", "Please start the game first.")
            return

        guess = self.entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showinfo("Invalid Guess", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Invalid Guess", "You already guessed that letter!")
            self.entry.delete(0, tk.END)
            return

        if guess not in self.planet.lower():
            self.attempts -= 1
            messagebox.showinfo("Incorrect Guess", f"Oops! '{guess}' is not in the planet name. You have {self.attempts} attempts left.")
            if self.attempts == 0:
                messagebox.showinfo("Game Over", f"Sorry, you're out of attempts. The correct planet was: {self.planet}")
                self.reset_game()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Correct Guess", "Good guess!")
            self.guessed_letters.append(guess)
            self.update_display()
            self.entry.delete(0, tk.END)

            if "_" not in self.planet_label.cget("text"):
                end_time = time.time()
                time_taken = end_time - self.start_time
                self.timer_label.config(text=f"Time: {int(time_taken)} s")
                self.timer_stopped = True
                score = self.attempts * 10 - int(time_taken)
                messagebox.showinfo("Congratulations!", f"You've guessed the planet in {int(time_taken)} seconds!\nYour score: {score}")
                self.reset_game()
        
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")

    def main(self):
        self.master.mainloop()

if __name__ == "__main__":
    SpaceWordChallenge().main()
