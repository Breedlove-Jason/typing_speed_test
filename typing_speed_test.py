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


random_words = generate_random_words(25)
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
start_button = tk.Button(window, text="Start", command=lambda: start_test(), font=button_font)
start_button.configure(width=10, background="#43b949")
start_button.pack()

stop_button = tk.Button(window, text="Stop", command=lambda: stop_test(), font=button_font)
stop_button.configure(width=10, background="#b94347")
stop_button.pack()


def start_test():
    global start_time
    start_button.destroy()
    entry.focus()
    start_time = time.time()
    entry.bind("<KeyRelease>", lambda event: check_input(event))


def stop_test():
    entry.unbind("<Key>")
    entry.configure(state="disabled")
    entry.configure(background="#43b949")
    entry.configure(foreground="#ffffff")
    entry.configure(disabledbackground="#43b949")
    entry.configure(disabledforeground="#ffffff")
    entry.configure(insertbackground="#ffffff")
    entry.configure(highlightbackground="#43b949")
    entry.configure(highlightcolor="#ffffff")
    entry.configure(selectbackground="#43b949")
    entry.configure(selectforeground="#ffffff")
    entry.configure(selectborderwidth="0")


def check_input(event):
    entry_text = entry.get()
    current_char = entry_text[-1]

    if len(entry_text) > len(text) or current_char != text[len(entry_text) - 1]:
        entry.delete(len(entry_text) - 1, tk.END)
        entry.configure(background="#b94347")
        entry.error = True
    elif getattr(entry, 'error', False):
        entry.configure(background="#02caec")
        entry.error = False

    if entry_text == text:
        stop_test()
        end_time = time.time()
        elapsed_time = end_time - start_time
        words_per_minute = (len(text) / elapsed_time) * 60

        result_text = f"Time: {elapsed_time:.2f} seconds\n"
        result_text += f"Speed: {words_per_minute:.2f} words per minute"

        result_label = tk.Label(window, text=result_text, font=entry_font, bg="#180d2f", fg="#ffffff")
        result_label.pack()


start_time = 0
window.mainloop()
