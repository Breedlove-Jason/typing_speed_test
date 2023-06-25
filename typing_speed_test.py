import time
import tkinter as tk
import random
import re
import tkinter.font as tkfont

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

entry_font = tkfont.Font(family="Nerd Fonts", size=20)
entry = tk.Entry(window, font=entry_font)
entry.configure(width=50)
entry.pack()


button_font = tkfont.Font(family="Nerd Fonts", size=20)
start_time = time.time()
start_button = tk.Button(window, text="Start", command=lambda: start_test(), font=button_font)
start_button.configure(width=10, background="#43b949")
start_button.pack()

stop_button = tk.Button(window, text="Stop", command=lambda: start_test(), font=button_font)
stop_button.configure(width=10, background="#b94347")
stop_button.pack()


def start_test():
    start_button.destroy()
    entry.focus()
    entry.bind("<KeyRelease>", lambda event: check_input(event))


window.mainloop()

# TODO: split words into characters and validate each character against the entry

# TODO Measure time taken to type by counting the number of seconds between the start and end of the test and divide 
#  the number of characters by the number of seconds to get the number of characters per second

# words_per_minute = (words_typed / elapsed_time) * 60
