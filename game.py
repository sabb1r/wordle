from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
from english_words import get_english_words_set

DICTIONARY = [x for x in get_english_words_set(['web2'], lower=True) if len(x) == 5]
WORD = random.choice(DICTIONARY)

root = Tk()
root.title('Wordle implemented by Python')

style = ttk.Style()
style.configure('Cell.TLabel', font='helvetica 24')

table = []
for i in range(5):
    table.append([None, None, None, None, None])

for i in range(5):
    for j in range(5):
        frame = ttk.Frame(root, width=40, height=40, borderwidth=5)
        frame.grid(row=i, column=j, padx=5, pady=5)
        frame.grid_propagate(False)

        cell = ttk.Label(frame, anchor='center')
        cell.grid(sticky=NSEW)
        cell['style'] = 'Cell.TLabel'
        table[i][j] = cell

row = 0 
column = 0 

current_cell = table[row][column]

def obtain_word():
    word = []
    for cell in table[row]:
        word.append(cell['text'])
    return ''.join(word)

def is_valid(word):
    if word in DICTIONARY:
        return True
    else:
        return False

def reset():
    for i in range(5):
        table[row][i]['text'] = ''

def judge():
    user_word = obtain_word() 
    if is_valid(user_word): 
        pattern = [0, 0, 0, 0, 0]
        for i in range(5):
            current_cell = table[row][i]
            current_char = user_word[i]
            if current_char == WORD[i]:
                pattern[i] = 1
                current_cell['background'] = 'green'
            else:
                if current_char in WORD:
                    current_cell['background'] = 'yellow'

        if sum(pattern) == 5:
            return 1
        else:
            return 0

    else:
        return -1

def display(e):
    global row
    global column

    current_cell = table[row][column]

    current_cell['text'] = e.char
    current_cell['anchor'] = 'center'
    column += 1
    if column == 5:
        status = judge()
        if status == 1:
            print('You win')
            root.destroy()
        elif status == -1:
            row = row
            column = 0
            reset()
        else:
            row += 1
            column = 0
        if row == 5:
            print('You Lost')
            print('Correct word: {}'.format(WORD))
            root.destroy()

root.bind('<KeyPress>', lambda e: display(e))

root.mainloop()


