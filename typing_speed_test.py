import time
import tkinter as tk
import random
import re
import tkinter.font as tkfont


class TypingSpeedTest:
    def __init__(self):
        self.words_num = 3
        self.window = tk.Tk()
        self.window.title("Typing Speed Test")
        self.window.geometry("900x600")
        self.window.config(bg="#180d2f")

        self.results = []

        self.num_words_entry = tk.Entry(self.window, font=tkfont.Font(family="Nerd Fonts", size=20))
        self.num_words_entry.configure(width=10)
        self.num_words_entry.grid(row=0, column=0, padx=10, pady=10)

        self.generate_button = tk.Button(
            self.window, text="Generate Words", command=self._generate_words,
            font=tkfont.Font(family="Nerd Fonts", size=14), background="#44c4c2"
        )
        self.generate_button.grid(row=0, column=1, padx=10, pady=10)

        self.random_words = self._generate_random_words(self.words_num)
        self.stripped_words = [re.sub(r"[^a-zA-Z0-9]+", '', word) for word in self.random_words]
        self.text = " ".join(self.stripped_words)

        self.type_this = tk.Text(self.window, height=10, width=50, wrap=tk.WORD)
        self.type_this.insert(tk.END, self.text)
        self.type_this.configure(background="#02caec")
        self.type_this.grid(row=1, columnspan=2, padx=10, pady=10)

        self.entry_font = tkfont.Font(family="Nerd Fonts", size=20)
        self.entry = tk.Entry(self.window, font=self.entry_font)
        self.entry.configure(width=50)
        self.entry.grid(row=2, columnspan=2, padx=10, pady=10)

        self.button_font = tkfont.Font(family="Nerd Fonts", size=20)
        self.start_button = tk.Button(
            self.window, text="Start", command=self._start_test, font=self.button_font
        )
        self.start_button.configure(width=10, background="#43b949")
        self.start_button.grid(row=3, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(
            self.window, text="Stop", command=self._stop_test, font=self.button_font
        )
        self.stop_button.configure(width=10, background="#b94347")
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)

        self.view_scores_button = tk.Button(
            self.window, text="View Scores", command=self._show_scores, font=self.button_font
        )
        self.view_scores_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.start_time = 0

    def _generate_words(self):
        num_words_entry_text = self.num_words_entry.get()
        if num_words_entry_text.isdigit():
            num_words = int(num_words_entry_text)
            self.random_words = self._generate_random_words(num_words)
            self.stripped_words = [re.sub(r"[^a-zA-Z0-9]+", '', word) for word in self.random_words]
            self.text = " ".join(self.stripped_words)
            self.type_this.delete(1.0, tk.END)
            self.type_this.insert(tk.END, self.text)

    def _generate_random_words(self, num_words):
        with open("words_alpha.txt", "r") as f:
            words = f.read().splitlines()
        rand_words = random.sample(words, num_words)
        return rand_words

    def _start_test(self):
        self.start_button.destroy()
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)
        self.entry.focus()
        self.start_time = time.time()
        self.entry.bind("<KeyRelease>", lambda event: self._check_input(event))

    def _stop_test(self):
        self.entry.unbind("<KeyRelease>")
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

        self.start_button = tk.Button(
            self.window, text="Start", command=self._start_test, font=self.button_font
        )
        self.start_button.configure(width=10, background="#43b949")
        self.start_button.grid(row=3, column=0, padx=10, pady=10)

        result = self._calculate_result()
        self.results.append(result)

    def _calculate_result(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        words_per_minute = (len(self.text) / elapsed_time) * 60
        result_text = f"Time: {elapsed_time:.2f} seconds\n"
        result_text += f"Speed: {words_per_minute:.2f} words per minute"
        return result_text

    def _show_scores(self):
        scores_window = tk.Toplevel(self.window)
        scores_window.title("Test Scores")
        scores_window.configure(background="#02caec")
        scores_window.geometry("800x800")

        scores_listbox = tk.Listbox(scores_window, font=self.entry_font, bg="#02caec", fg="#000000")
        scores_listbox.configure(width=375)
        scores_listbox.pack()

        for result in self.results:
            scores_listbox.insert(tk.END, result)

    def _check_input(self, event):
        entry_text = self.entry.get()

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
            result_text = f"Time: {elapsed_time:.2f} seconds\n"
            result_text += f"Speed: {words_per_minute:.2f} words per minute"

            result_label = tk.Label(self.window, text=result_text, font=self.entry_font, bg="#180d2f", fg="#ffffff")
            result_label.grid(row=5, columnspan=2, padx=10, pady=10)

    def run(self):
        self.window.mainloop()


test = TypingSpeedTest()
test.run()