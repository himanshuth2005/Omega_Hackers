import random
import tkinter as tk
from tkinter import messagebox
import time

class SpaceWordChallenge:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Space Word Challenge")
        self.master.geometry("400x370") 
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

        self.entry = tk.Entry(self.master, font=("Arial", 12))
        self.entry.pack()

        self.entry.bind("<Return>", self.check_guess)  

        self.guess_button = tk.Button(self.master, text="Guess", font=("Arial", 12), bg="#FFD700", fg="#004466", command=self.check_guess)
        self.guess_button.pack(pady=10)

        self.attempts_label = tk.Label(self.master, text="", font=("Arial", 12), bg="#D9E6EB", fg="#004466")
        self.attempts_label.pack()

        self.planet = self.choose_planet()
        self.guessed_letters = []
        self.attempts = 6
        self.start_time = time.time()

        self.update_display()

    def choose_planet(self):
        planet_list = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
        return random.choice(planet_list)

    def update_display(self):
        displayed_planet = ""
        for letter in self.planet:
            if letter.lower() in self.guessed_letters or not letter.isalpha():
                displayed_planet += letter
            else:
                displayed_planet += "_"
        self.planet_label.config(text=displayed_planet)

        self.attempts_label.config(text=f"Attempts left: {self.attempts}")

    def check_guess(self, event=None):
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
                self.master.destroy()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Correct Guess", "Good guess!")
            self.guessed_letters.append(guess)
            self.update_display()
            self.entry.delete(0, tk.END)

            if "_" not in self.planet_label.cget("text"):
                end_time = time.time()
                time_taken = end_time - self.start_time
                score = self.attempts * 10 - int(time_taken)
                messagebox.showinfo("Congratulations!", f"You've guessed the planet in {int(time_taken)} seconds!\nYour score: {score}")
                self.master.destroy()
        
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")

    def main(self):
        self.master.mainloop()

if __name__ == "__main__":
    SpaceWordChallenge().main()
