# Valid Input:
# Hello, World, Owl, Her, Row
import tkinter as tk
from tkinter import messagebox

crossword_layout = [
    ['_', '_', '_', '_', '_'],
    ['_', '#', '_', '#', '_'],
    ['_', '_', '_', '_', '_'],
    ['_', '#', '_', '#', '_'],
    ['_', '_', '_', '_', '_']
]

grid_size = len(crossword_layout)
labels = [[None for _ in range(grid_size)] for _ in range(grid_size)]
word_entries = []

def is_valid(word, row, col, direction, grid):
    for k in range(len(word)):
        r, c = (row + k, col) if direction == 'V' else (row, col + k)
        if r >= grid_size or c >= grid_size:
            return False
        if crossword_layout[r][c] == '#':
            return False
        if grid[r][c] not in ('', word[k]):
            return False
    return True

def place_word(word, row, col, direction, grid):
    placed = []
    for k in range(len(word)):
        r, c = (row + k, col) if direction == 'V' else (row, col + k)
        if grid[r][c] == '':
            grid[r][c] = word[k]
            placed.append((r, c))
    return placed

def remove_word(placed, grid):
    for r, c in placed:
        grid[r][c] = ''

def solve_csp(index, grid, words):
    if index == len(words):
        return True
    word = words[index]
    for i in range(grid_size):
        for j in range(grid_size):
            for direction in ['H', 'V']:
                if is_valid(word, i, j, direction, grid):
                    placed = place_word(word, i, j, direction, grid)
                    if solve_csp(index + 1, grid, words):
                        return True
                    remove_word(placed, grid)
    return False

def solve():
    user_words = [entry.get().strip().upper() for entry in word_entries if entry.get().strip()]
    user_words = list(filter(lambda w: len(w) <= grid_size, user_words))

    if not user_words:
        messagebox.showerror("Input Error", "Enter at least one word (max length: {}).".format(grid_size))
        return

    grid = [['' if crossword_layout[i][j] == '_' else '#' for j in range(grid_size)] for i in range(grid_size)]
    
    if solve_csp(0, grid, user_words):
        for i in range(grid_size):
            for j in range(grid_size):
                if crossword_layout[i][j] == '#':
                    labels[i][j]['text'] = ''
                    labels[i][j]['bg'] = 'black'
                else:
                    labels[i][j]['text'] = grid[i][j]
                    labels[i][j]['bg'] = 'lightgreen' if grid[i][j] != '' else 'white'
    else:
        messagebox.showinfo("Result", "No solution found with given words.")


root = tk.Tk()
root.title("Generalized Crossword Puzzle CSP Solver")

title_label = tk.Label(root, text="Crossword Puzzle CSP Solver", font=("Arial", 14, 'bold'))
title_label.pack(pady=10)

entry_frame = tk.Frame(root)
entry_frame.pack()

tk.Label(entry_frame, text="Enter words (length ≤ {}):".format(grid_size), font=("Arial", 12)).pack()

for _ in range(10):
    entry = tk.Entry(entry_frame, font=("Arial", 12))
    entry.pack(pady=2)
    word_entries.append(entry)

grid_frame = tk.Frame(root)
grid_frame.pack(pady=10)

for i in range(grid_size):
    for j in range(grid_size):
        bg_color = 'white' if crossword_layout[i][j] == '_' else 'black'
        labels[i][j] = tk.Label(grid_frame, width=4, height=2, relief='solid',
                                font=('Arial', 12), bg=bg_color)
        labels[i][j].grid(row=i, column=j)

solve_button = tk.Button(root, text="Solve Puzzle", command=solve, font=('Arial', 12))
solve_button.pack(pady=10)

root.mainloop()


