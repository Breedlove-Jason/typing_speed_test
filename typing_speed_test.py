import time
import tkinter as tk
import random
import re

window = tk.Tk()
window.title("Typing Speed Test")
window.geometry("600x400")
window.config(bg="#180d2f")


def generate_random_words(num_words):
    with open("words_alpha.txt", "r") as f:
        words = f.read().splitlines()
    rand_words = random.sample(words, num_words)
    return rand_words


random_words = generate_random_words(100)
stripped_words = [re.sub(r"[^a-zA-Z0-9]+", '', word) for word in random_words]
text = " ".join(stripped_words)

type_this = tk.Text(window, height=10, width=50)
type_this.insert(tk.END, text)
type_this.configure(background="#02caec")
type_this.pack()

entry = tk.Entry(window, font=("Arial", 20))
entry.configure(width=50)
entry.pack()

window.mainloop()
