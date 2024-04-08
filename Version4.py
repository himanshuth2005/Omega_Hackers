import random
import tkinter as tk
from tkinter import messagebox
import time

class SpaceWordChallenge:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Space Word Challenge")
        self.master.attributes('-fullscreen', True)  # Maximize window to full screen

        # Set background image
        self.bg_image = tk.PhotoImage(file="space_bg.png")
        self.bg_label = tk.Label(self.master, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Space-themed color combination
        self.label_color = "#FFFFFF"  # White
        self.button_color = "#FFD700"  # Gold

        self.label_frame = tk.Frame(self.master, bg='black')  # Frame for labels
        self.label_frame.pack()

        self.label = tk.Label(self.label_frame, text="Space Word Challenge", font=("Arial", 30, "bold"), fg=self.label_color, bg='black')
        self.label.pack(pady=(50, 30))

        self.category_label = tk.Label(self.master, text="Select a category:", font=("Arial", 20), fg=self.label_color, bg='black')
        self.category_label.pack()

        self.category_var = tk.StringVar(self.master)
        self.category_var.set("Planets")
        self.category_menu = tk.OptionMenu(self.master, self.category_var, "Planets", "Galaxies", "Stars")
        self.category_menu.config(font=("Arial", 20), bg=self.button_color, fg=self.label_color, width=12)
        self.category_menu.pack(pady=20)

        self.planet_frame = tk.Frame(self.master, bg='black')  # Frame for planet label
        self.planet_frame.pack()

        self.planet_label = tk.Label(self.planet_frame, text="", font=("Arial", 30), fg=self.label_color, bg='black')
        self.planet_label.pack(pady=20)

        self.guess_label = tk.Label(self.master, text="Enter a letter:", font=("Arial", 20), fg=self.label_color, bg='black')
        self.guess_label.pack()

        self.entry = tk.Entry(self.master, font=("Arial", 20), state=tk.DISABLED)
        self.entry.pack()

        self.entry.bind("<Return>", self.check_guess)  

        self.guess_button = tk.Button(self.master, text="Guess", font=("Arial", 20), bg=self.button_color, fg=self.label_color, command=self.check_guess, state=tk.DISABLED)
        self.guess_button.pack(pady=20)

        self.start_button = tk.Button(self.master, text="Start", font=("Arial", 20), bg=self.button_color, fg=self.label_color, command=self.start_game)
        self.start_button.pack(pady=20)

        self.reset_button = tk.Button(self.master, text="Reset", font=("Arial", 20), bg=self.button_color, fg=self.label_color, command=self.reset_game, state=tk.DISABLED)
        self.reset_button.pack(pady=20)
        
        self.attempts_label = tk.Label(self.master, text="Your Text Here", font=("Arial", 20), fg='white', bg='black')
        self.attempts_label.pack()

        self.quit_button = tk.Button(self.master, text="Quit", font=("Arial", 20), bg=self.button_color, fg=self.label_color, command=self.master.destroy)
        self.quit_button.pack(pady=20)

        self.score_label = tk.Label(self.master, text="", font=("Arial", 20), fg=self.label_color, bg='black')
        self.score_label.pack()

        self.timer_label = tk.Label(self.master, text="", font=("Arial", 20), fg=self.label_color, bg='black')
        self.timer_label.pack(side=tk.RIGHT, padx=20, pady=10)

        self.category = ""
        self.planet = ""
        self.guessed_letters = []
        self.attempts = 5
        self.start_time = 0
        self.game_started = False
        self.timer_stopped = False

    def start_game(self):
        self.set_category()
        self.planet = self.choose_word()
        self.guessed_letters = []
        self.start_time = time.time()
        self.game_started = True
        self.timer_stopped = False
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        self.attempts = 5  # Reset attempts
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")
        self.update_display()
        self.update_timer()

    def reset_game(self):
        self.planet_label.config(text="")
        self.entry.delete(0, tk.END)
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)
        self.game_started = False
        self.attempts_label.config(text="")  # Remove attempts label
        self.timer_label.config(text="")
        self.score_label.config(text="")  # Remove score label
        self.timer_stopped = True  

    def choose_word(self):
        if self.category == "Planets":
            word_list = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
        elif self.category == "Galaxies":
            word_list = ["Milky Way", "Andromeda", "Triangulum", "Messier 87", "Whirlpool", "Centaurus A"]
        elif self.category == "Stars":
            word_list = ["Sun", "Sirius", "Alpha Centauri", "Betelgeuse", "Vega", "Polaris", "Proxima Centauri"]
        else:
            word_list = []
        return random.choice(word_list)

    def set_category(self):
        self.category = self.category_var.get()

    def update_display(self):
        displayed_word = " ".join(letter if letter.lower() in self.guessed_letters or not letter.isalpha() else "_" for letter in self.planet)
        self.planet_label.config(text=displayed_word)

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
            messagebox.showinfo("Invalid Guess", "Please enter a single alphabetical character.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Invalid Guess", "You already guessed that letter!")
            self.entry.delete(0, tk.END)
            return

        if guess not in self.planet.lower():
            self.attempts -= 1 
            messagebox.showinfo("Incorrect Guess", f"Oops! '{guess}' is not in the word. You have {self.attempts} attempts left.")
            if self.attempts == 0:
                messagebox.showinfo("Game Over", f"Sorry, you're out of attempts. The correct word was: {self.planet}")
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
                self.score_label.config(text=f"Score: {score}")
                messagebox.showinfo("Congratulations!", f"You've guessed the word in {int(time_taken)} seconds!\nYour score: {score}")
                self.reset_game()
        
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")

    def main(self):
        self.master.mainloop()

if __name__ == "__main__":
    SpaceWordChallenge().main()
