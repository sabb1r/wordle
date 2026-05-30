from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import string
from copy import copy

TOTAL_ATTEMPT = 6
WORD_LENGTH = 5
BACKSPACE = 8
ENTER = 13
FILE_PATH = 'resource/five_letter_words.txt'

with open(FILE_PATH, 'r') as f:
    content = f.read()
    DICTIONARY = content.split('\n')


class Wordle:
    def __init__(self, root):
        self.root = root
        self.root.title('Wordle implemented in python')
        self.WORD = random.choice(DICTIONARY)
        self.content = ttk.Frame(root)
        self.content.grid(row=0, column=0, rowspan=TOTAL_ATTEMPT, columnspan=WORD_LENGTH, sticky=NSEW)

        style = ttk.Style()
        style.configure('Cell.TLabel', font='helvetica 18')

        self.table = []
        row = [None] * WORD_LENGTH
        for _ in range(TOTAL_ATTEMPT):
            self.table.append(copy(row))

        for i in range(TOTAL_ATTEMPT):
            for j in range(WORD_LENGTH):
                frame = ttk.Frame(self.content, width=40, height=40, borderwidth=5, relief='groove')
                frame.grid(row=i, column=j, padx=5, pady=5)
                frame.grid_propagate(False)

                cell = ttk.Label(frame, anchor='center')
                cell.grid(row=0, column=0, sticky=NSEW)
                cell['style'] = 'Cell.TLabel'
                self.table[i][j] = cell

        self.current_row = 0
        self.current_column = 0
        self.root.bind('<KeyPress>', lambda e: self.display(e))

    def popup(self, msg_tag):
        if msg_tag == 'win':
            msg = 'Congratulations!!'
        else:
            msg = 'Oh No! You Lose. Hidden word is: {}'.format(self.WORD)
        messagebox.showinfo(message=msg)

        decision = messagebox.askyesno(
            message='Do you wanna play again?',
            icon='question',
            title='Play Again'
            )
        return decision

    def obtain_word(self):
        word = []
        for cell in self.table[self.current_row]:
            word.append(cell['text'].lower())
        return ''.join(word)

    def is_valid(self, word):
        if word in DICTIONARY:
            return True
        else:
            return False

    def reset(self):
        for i in range(WORD_LENGTH):
            self.table[self.current_row][i]['text'] = ''

    def judge(self):
        user_word = self.obtain_word()
        if self.is_valid(user_word):
            pattern = [0] * WORD_LENGTH
            for i in range(WORD_LENGTH):
                current_cell = self.table[self.current_row][i]
                current_char = user_word[i]
                if current_char == self.WORD[i]:
                    pattern[i] = 1
                    current_cell['background'] = 'green'
                else:
                    if current_char in self.WORD:
                        if user_word[self.WORD.index(current_char)] != current_char:
                            current_cell['background'] = 'yellow'
                        if self.WORD.count(current_char) > 1:
                            current_cell['background'] = 'yellow'
            if sum(pattern) == WORD_LENGTH:
                return 1
            else:
                return 0
        else:
            return -1

    def display(self, e):
        char = e.char
        if self.current_column < WORD_LENGTH:
            current_cell = self.table[self.current_row][self.current_column]
            if ord(char) == BACKSPACE:
                # Delete Previous Entry
                if self.current_column:
                    self.current_column -= 1
                    prev_cell = self.table[self.current_row][self.current_column]
                    prev_cell['text'] = ''
            elif char in string.ascii_letters:
                # Proceed
                current_cell['text'] = char.upper()
                self.current_column += 1
        else:
            if ord(char) == ENTER:
                status = self.judge()
                if status == 1:
                    result = self.popup('win')
                    if result:
                        self.content.destroy()
                        Wordle(self.root)
                    else:
                        self.root.destroy()
                elif status == -1:
                    self.current_column = 0
                    self.reset()
                else:
                    self.current_row += 1
                    self.current_column = 0
            elif ord(char) == BACKSPACE:
                prev_cell = self.table[self.current_row][self.current_column - 1]
                prev_cell['text'] = ''
                self.current_column -= 1
        if self.current_row == TOTAL_ATTEMPT:
            reply = self.popup('lose')
            if reply:
                self.content.destroy()
                Wordle(self.root)
            else:
                self.root.destroy()

def main():
    root = Tk()
    Wordle(root)
    root.mainloop()

if __name__ == '__main__':
    main()

