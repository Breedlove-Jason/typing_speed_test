import time
import random
import re
import tkinter as tk
import tkinter.font as tkfont

BG_COLOR = "#180d2f"
TEXT_COLOR = "#02caec"
BTN_COLOR = "#44c4c2"
BTN_HIGHLIGHT_COLOR = "#43b949"
ERROR_COLOR = "#b94347"
FONT_FAMILY = "Nerd Fonts"
FONT_SIZE = 20


class TypingSpeedTest:
    def __init__(self):
        """
        Initializes the TypingSpeedTest class.

        It sets up the main window and configures the initial state of the application.
        """
        self.text = None
        self.stripped_words = None
        self.random_words = None
        self.words_num = 10
        self.window = tk.Tk()
        self.window.title("Typing Speed Test")
        self.window.geometry("1300x600")
        self.window.config(bg=BG_COLOR)

        self.results = []

        self.num_words_entry = tk.Entry(self.window, font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE))
        self.num_words_entry.configure(width=10)
        self.num_words_entry.pack(side=tk.LEFT, padx=10, pady=10)

        self.generate_button = tk.Button(
            self.window, text="Generate Words", command=self.generate_words,
            font=tkfont.Font(family=FONT_FAMILY, size=int(FONT_SIZE * 0.7)), background=BTN_COLOR,
            padx=10, pady=10
        )
        self.generate_button.pack(side=tk.LEFT)

        self.type_this = tk.Text(self.window, height=10, width=50, wrap=tk.WORD,
                                 font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE))
        self.type_this.configure(background=TEXT_COLOR)
        self.type_this.pack(padx=10, pady=(0, 10))

        self.entry = tk.Entry(self.window, font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE))
        self.entry.configure(width=50)
        self.entry.pack(padx=10, pady=(10, 0))

        self.start_button = tk.Button(
            self.window, text="Start", command=self.start_test, font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE),
            width=10, background=BTN_HIGHLIGHT_COLOR
        )
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(
            self.window, text="Stop", command=self.stop_test, font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE),
            width=10, background=BTN_COLOR
        )
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.view_scores_button = tk.Button(
            self.window, text="Scores", command=self.show_scores, font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE),
            width=20, background=BTN_COLOR
        )
        self.view_scores_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.start_time = 0
        self.generate_words()

    def generate_words(self):
        """
        Generates random words based on the user input and updates the display.

        It reads the number of words from the input field, generates the random words,
        and updates the text to be displayed for the typing test.
        """
        num_words_entry_text = self.num_words_entry.get()
        if num_words_entry_text.isdigit():
            self.words_num = int(num_words_entry_text)

        with open("words_alpha.txt", "r") as f:
            words = f.read().splitlines()

        self.random_words = random.sample(words, self.words_num)
        self.stripped_words = [re.sub(r"[^a-zA-Z0-9]+", '', word) for word in self.random_words]
        self.text = " ".join(self.stripped_words)
        self.update_display()

    def update_display(self):
        """
        Updates the display with the current text to be typed.

        It clears the input field, sets the focus to the input field, and updates
        the text to be displayed for the typing test.
        """
        self.type_this.delete('1.0', tk.END)
        self.type_this.insert(tk.END, self.text)
        self.entry.configure(background=TEXT_COLOR)
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def start_test(self):
        """
        Starts the typing test.

        It destroys the start button, enables the input field, binds the event for
        checking the input, and starts the timer.
        """
        self.start_button.destroy()
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.entry.bind("<KeyRelease>", self.check_input)
        self.start_time = time.time()

    def stop_test(self):
        """
        Stops the current typing test.

        It unbinds the event for checking the input, enables the input field,
        generates new words for the next test, and updates the results.
        """
        self.entry.unbind("<KeyRelease>")
        self.entry.configure(state="normal")

        if getattr(self.entry, 'error', False):
            self.entry.delete(0, tk.END)
            self.entry.configure(background=TEXT_COLOR, foreground="black")
            self.entry.error = False
            self.entry.focus()
            return

        self.generate_words()

        self.start_button = tk.Button(
            self.window, text="Start", command=self.start_test, font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE),
            width=10, background=BTN_HIGHLIGHT_COLOR
        )
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button.pack_forget()

        result = self.calculate_result()
        self.results.append(result)

        with open("scores.txt", "a") as f:
            f.write("\n".join(self.results))

        self.results = self.results[::-1]

    def calculate_result(self):
        """
        Calculates the result of the typing test.

        It calculates the elapsed time and the typing speed in words per minute.
        """
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        words_per_minute = (len(self.text) / elapsed_time) * 60
        result_text = f"Time: {elapsed_time:.2f} seconds\n"
        result_text += f"Speed: {words_per_minute:.2f} words per minute"
        return result_text

    def show_scores(self):
        """
           Displays the test scores in a separate window.

           It creates a new window and a listbox to display the test scores.
           """
        scores_window = tk.Toplevel(self.window)
        scores_window.title("Test Scores")
        scores_window.configure(background=BG_COLOR)
        scores_window.geometry("800x800")

        scores_listbox = tk.Listbox(scores_window, font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE), bg=TEXT_COLOR,
                                    fg="black", width=375)
        scores_listbox.pack(padx=10, pady=10)

        # Load scores from file
        scores = []
        with open("scores.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    scores.append(line)  # convert line to integer

        # Insert scores into the listbox
        for score in scores:
            scores_listbox.insert(tk.END, score)

    def check_input(self, event):
        """
        Checks the input against the expected text.

        It validates the input against the expected text, handles errors,
        and stops the test if the input matches the expected text.
        """
        entry_text = self.entry.get()

        if entry_text:
            current_char = entry_text[-1]

            if len(entry_text) > len(self.text) or current_char != self.text[len(entry_text) - 1]:
                self.entry.delete(len(entry_text) - 1, tk.END)
                self.entry.configure(background=ERROR_COLOR)
                self.entry.error = True
                return

            if getattr(self.entry, 'error', False):
                self.entry.configure(background=TEXT_COLOR)
                self.entry.error = False

        if entry_text == self.text:
            self.stop_test()
            result = self.calculate_result()
            self.results.append(result)
            result_label = tk.Label(self.window, text=result, font=tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE),
                                    bg=BG_COLOR, fg=TEXT_COLOR)
            result_label.pack(padx=10, pady=10)

    def run(self):
        """
        Runs the main event loop of the application.
        """
        self.window.mainloop()


if __name__ == '__main__':
    test = TypingSpeedTest()
    test.run()
