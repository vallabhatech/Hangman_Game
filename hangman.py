import requests   # Used to download images from the internet
from PIL import Image, ImageTk # PIL is used to work with images (Pillow library)(pil-python imaging library)
import tkinter as tk  # tkinter is the standard GUI toolkit for Python
from tkinter import messagebox  # Used for pop-up message boxes
import random  # Provides random choices, like selecting a word
import os  # Used to check file paths and existence

# Download and save the background image if not already present
def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)

# URL and path setup for background image
background_url = "https://t4.ftcdn.net/jpg/05/79/54/53/360_F_579545387_6JuKZXKyBuvrGTVxcCIXPZnE5cr41vC9.jpg"
background_path = "background.jpg"
if not os.path.exists(background_path):
    download_image(background_url, background_path)

# Word categories and clues
categories = {
    "Movies": {
        "inception": "A dream within a dream.",
        "avatar": "Blue aliens and Pandora.",
        "joker": "A famous DC villain.",
        "gladiator": "Are you not entertained?",
        "titanic": "A tragic love story at sea."
    },
    "Sports": {
        "soccer": "Also called football worldwide.",
        "cricket": "Bat, ball, and wickets.",
        "tennis": "Played with racquets and a net.",
        "basketball": "Dribble, shoot, and dunk.",
        "boxing": "A combat sport with gloves."
    },
    "Colors": {
        "magenta": "A purplish-pink color.",
        "turquoise": "A blue-green shade.",
        "indigo": "Between blue and violet.",
        "scarlet": "A bright red color.",
        "amber": "A yellow-orange hue."
    },
    "General Knowledge": {
        "gravity": "Force that pulls objects down.",
        "oxygen": "Essential gas for breathing.",
        "planet": "Orbits a star.",
        "pyramid": "Egyptian ancient structure.",
        "compass": "Used for navigation."
    },
    "Fun": {
        "juggle": "Tossing and catching items.",
        "puzzle": "Test of knowledge or skill.",
        "prank": "A playful trick.",
        "giggle": "A light, silly laugh.",
        "circus": "Acrobats, clowns, and animals."
    }
}

# Main game class
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.state('zoomed')  # Fullscreen window
        self.root.resizable(True, True)
        self.root.bind('<Configure>', self.resize_background)  # Dynamic background
        self.root.bind('<Key>', self.on_key_press)  # Key press handling
        self.create_difficulty_screen()

    # First screen to choose difficulty
    def create_difficulty_screen(self):
        self.clear_widgets()
        self.bg_image = Image.open(background_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title = tk.Label(self.root, text="Choose Difficulty", font=("Arial", 28, "bold"), fg="white", bg="#000000")
        title.pack(pady=20)

        frame = tk.Frame(self.root, bg="#000000")
        frame.pack()

        difficulties = [("Easy", 8), ("Medium", 6), ("Hard", 4)]

        for i, (label, tries) in enumerate(difficulties):
            btn = tk.Button(frame, text=label, font=("Arial", 18), width=20,
                            command=lambda t=tries: self.set_difficulty(t), bg="#444", fg="white")
            btn.grid(row=i, column=0, padx=20, pady=10)

    # Set the number of allowed wrong guesses and go to category screen
    def set_difficulty(self, tries):
        self.max_tries = tries
        self.time_limit = 90
        self.create_category_screen()

    # Second screen to choose category
    def create_category_screen(self):
        self.clear_widgets()
        self.bg_image = Image.open(background_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title = tk.Label(self.root, text="Choose a Category", font=("Arial", 28, "bold"), fg="white", bg="#000000")
        title.pack(pady=20)

        frame = tk.Frame(self.root, bg="#000000")
        frame.pack()

        for i, cat in enumerate(categories.keys()):
            btn = tk.Button(frame, text=cat, font=("Arial", 18), width=20,
                            command=lambda c=cat: self.start_game(c), bg="#444", fg="white")
            btn.grid(row=i, column=0, padx=20, pady=10)

    # Start the game with selected category and word
    def start_game(self, category):
        self.category = category
        self.word, self.description = random.choice(list(categories[category].items()))
        self.guessed_word = ["_"] * len(self.word)
        self.tries = self.max_tries
        self.time_left = self.time_limit
        self.clear_widgets()
        self.create_widgets()
        self.start_timer()

    # Clear the screen widgets
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Create game screen UI elements
    def create_widgets(self):
        self.bg_image = Image.open(background_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = tk.Label(self.root, text=f"Category: {self.category}", font=("Arial", 24, "bold"), fg="white", bg="#000000")
        self.title_label.pack(pady=10)

        self.clue_label = tk.Label(self.root, text=f"Clue: {self.description}", font=("Arial", 16), fg="yellow", bg="#000000")
        self.clue_label.pack(pady=10)

        self.word_label = tk.Label(self.root, text=" ".join(self.guessed_word), font=("Arial", 20), fg="white", bg="#000000")
        self.word_label.pack(pady=10)

        self.info_label = tk.Label(self.root, text=f"Chances left: {self.tries} | Found: 0/{len(self.word)}", font=("Arial", 14), fg="white", bg="#000000")
        self.info_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}", font=("Arial", 14), fg="white", bg="#000000")
        self.timer_label.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=200, height=250, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.draw_hangman()

        self.buttons_frame = tk.Frame(self.root, bg="#000000")
        self.buttons_frame.pack(pady=10)
        self.create_letter_buttons()

        self.reset_button = tk.Button(self.root, text="Restart Game", font=("Arial", 14), command=self.create_difficulty_screen, bg="#333", fg="white")
        self.reset_button.pack(pady=10)

    # Start countdown timer
    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            messagebox.showinfo("Game Over", "Time's up! You lost!")
            self.create_difficulty_screen()

    # Create alphabet buttons
    def create_letter_buttons(self):
        self.buttons = {}
        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
            button = tk.Button(self.buttons_frame, text=letter, font=("Arial", 14), width=3,
                               command=lambda l=letter: self.guess_letter(l), bg="#555", fg="white", relief="raised")
            button.grid(row=i // 9, column=i % 9, padx=5, pady=5)
            self.buttons[letter] = button

    # Draw parts of the hangman as wrong guesses increase
    def draw_hangman(self):
        parts = [
            lambda: self.canvas.create_line(20, 230, 180, 230),  # base
            lambda: self.canvas.create_line(100, 230, 100, 20),  # pole
            lambda: self.canvas.create_line(100, 20, 150, 20),   # top bar
            lambda: self.canvas.create_line(150, 20, 150, 50),   # rope
            lambda: self.canvas.create_oval(130, 50, 170, 90),   # head
            lambda: self.canvas.create_line(150, 90, 150, 160),  # body
            lambda: self.canvas.create_line(150, 100, 130, 140), # left arm
            lambda: self.canvas.create_line(150, 100, 170, 140), # right arm
            lambda: self.canvas.create_line(150, 160, 130, 200), # left leg
            lambda: self.canvas.create_line(150, 160, 170, 200), # right leg
        ]
        self.canvas.delete("all")
        for i in range(self.max_tries - self.tries):
            if i < len(parts):
                parts[i]()

    # Handle guessing a letter
    def guess_letter(self, letter):
        button = self.buttons[letter]
        button.config(state=tk.DISABLED, fg="red")
        if letter in self.word:
            for i, l in enumerate(self.word):
                if l == letter:
                    self.guessed_word[i] = letter
            self.word_label.config(text=" ".join(self.guessed_word))
        else:
            self.tries -= 1
            self.draw_hangman()

        correct_letters_found = len([char for char in self.guessed_word if char != "_"])
        self.info_label.config(text=f"Chances left: {self.tries} | Found: {correct_letters_found}/{len(self.word)}")

        if "_" not in self.guessed_word:
            messagebox.showinfo("Game Over", "Congratulations! You guessed the word!")
            self.create_difficulty_screen()
        elif self.tries == 0:
            messagebox.showerror("Game Over", f"You lost! The word was '{self.word}'.")
            self.create_difficulty_screen()

    # Resize the background image dynamically
    def resize_background(self, event):
        bg_image = Image.open(background_path)
        bg_image = bg_image.resize((event.width, event.height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_label.config(image=self.bg_photo)

    # Allow keyboard input for guessing
    def on_key_press(self, event):
        key = event.char.lower()
        if key in self.buttons:
            self.guess_letter(key)

# Launch the game
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()