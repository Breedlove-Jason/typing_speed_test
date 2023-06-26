import time
import tkinter as tk
import random
import re
import tkinter.font as tkfont


class TypingSpeedTest:

    def __init__(self):
        self.words_num = 5
        self.window = tk.Tk()
        self.window.title("Typing Speed Test")
        self.window.geometry("600x400")
        self.window.config(bg="#180d2f")

        self.random_words = self._generate_random_words(self.words_num)
        self.stripped_words = [re.sub(r"[^a-zA-Z0-9]+", '', word) for word in self.random_words]
        self.text = " ".join(self.stripped_words)

        self.type_this = tk.Text(self.window, height=10, width=50, wrap=tk.WORD)
        self.type_this.insert(tk.END, self.text)
        self.type_this.configure(background="#02caec")
        self.type_this.pack()

        self.entry_font = tkfont.Font(family="Nerd Fonts", size=20)
        self.entry = tk.Entry(self.window, font=self.entry_font)
        self.entry.configure(width=50)
        self.entry.pack()

        self.button_font = tkfont.Font(family="Nerd Fonts", size=20)
        self.start_button = tk.Button(self.window, text="Start", command=self._start_test, font=self.button_font)
        self.start_button.configure(width=10, background="#43b949")
        self.start_button.pack()

        self.stop_button = tk.Button(self.window, text="Stop", command=self._stop_test, font=self.button_font)
        self.stop_button.configure(width=10, background="#b94347")
        self.stop_button.pack()

        self.start_time = 0

    def _generate_random_words(self, num_words):
        with open("words_alpha.txt", "r") as f:
            words = f.read().splitlines()
        rand_words = random.sample(words, num_words)
        return rand_words

    def _start_test(self):
        self.start_button.destroy()
        self.entry.focus()
        self.start_time = time.time()
        self.entry.bind("<KeyRelease>", lambda event: self._check_input(event))

    def _stop_test(self):
        self.entry.unbind("<Key>")
        # self.entry.configure(state="disabled")
        self.entry.configure(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.configure(background="#02caec")
        self.entry.configure(foreground="black")
        self.entry.focus()

        self.random_words = self._generate_random_words(self.words_num)
        self.stripped_words = [re.sub(r"[^a-zA-Z0-9]+", '', word) for word in self.random_words]
        self.text = " ".join(self.stripped_words)
        self.type_this.delete(1.0, tk.END)
        self.type_this.insert(tk.END, self.text)

        # self.entry.configure(background="#43b949")
        # self.entry.configure(foreground="#ffffff")
        # self.entry.configure(disabledbackground="#43b949")
        # self.entry.configure(disabledforeground="#ffffff")
        # self.entry.configure(insertbackground="#ffffff")
        # self.entry.configure(highlightbackground="#43b949")
        # self.entry.configure(highlightcolor="#ffffff")
        # self.entry.configure(selectbackground="#43b949")
        # self.entry.configure(selectforeground="#ffffff")
        # self.entry.configure(selectborderwidth="0")

    def _check_input(self, event):
        entry_text = self.entry.get()
        current_char = entry_text[-1]

        if entry_text:
            current_char = entry_text[-1]

            if len(entry_text) > len(self.text) or current_char != self.text[len(entry_text) - 1]:
                self.entry.delete(len(entry_text) - 1, tk.END)
                self.entry.configure(background="#b94347")
                self.entry.error = True
            elif getattr(self.entry, 'error', False):
                self.entry.configure(background="#02caec")
                self.entry.error = False

        if entry_text == self.text:
            self._stop_test()
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            words_per_minute = (len(self.text) / elapsed_time) * 60
            # words_per_minute = (len(self.stripped_words) / elapsed_time) * 60
            result_text = f"Time: {elapsed_time:.2f} seconds\n"
            result_text += f"Speed: {words_per_minute:.2f} words per minute"

            result_label = tk.Label(self.window, text=result_text, font=self.entry_font, bg="#180d2f", fg="#ffffff")
            result_label.pack()

    def run(self):
        self.window.mainloop()


test = TypingSpeedTest()
test.run()
