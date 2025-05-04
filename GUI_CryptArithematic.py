# Words: SEND, MORE
# Operator: +  
# Result Word: MONEY


import tkinter as tk
from tkinter import messagebox
import heapq


class CryptarithmeticSolver:
    def __init__(self, words, result):
        self.words = words
        self.result = result
        self.unique_letters = list(set(''.join(words + [result])))

    def is_valid_assignment(self, letter_map):
        if len(set(letter_map.values())) < len(letter_map):
            return False
        word_values = []
        for word in self.words + [self.result]:
            if letter_map.get(word[0], -1) == 0:
                return False
            try:
                num_value = int(''.join(str(letter_map[letter]) for letter in word))
                word_values.append(num_value)
            except KeyError:
                return False
        return sum(word_values[:-1]) == word_values[-1]

    def heuristic(self, letter_map):
        try:
            left_sum = sum(
                int(''.join(str(letter_map[letter]) for letter in word))
                for word in self.words
            )
            right_sum = int(''.join(str(letter_map[letter]) for letter in self.result))
            return abs(left_sum - right_sum)
        except KeyError:
            return float('inf')

    def best_first_search(self):
        if len(self.unique_letters) > 10:
            return None  # Impossible to assign unique digits to more than 10 letters

        start_state = (0, 0, {}, self.unique_letters.copy())
        open_list = [start_state]
        unique_id = 0

        while open_list:
            _, _, current_map, remaining_letters = heapq.heappop(open_list)

            if not remaining_letters:
                if self.is_valid_assignment(current_map):
                    return current_map
                continue

            current_letter = remaining_letters[0]
            used_digits = set(current_map.values())

            for digit in range(10):
                if digit not in used_digits:
                    # Prevent leading zeros
                    if digit == 0 and any(word[0] == current_letter for word in self.words + [self.result]):
                        continue
                    new_map = current_map.copy()
                    new_map[current_letter] = digit
                    h_score = self.heuristic(new_map)
                    unique_id += 1
                    heapq.heappush(open_list, (
                        h_score,
                        unique_id,
                        new_map,
                        remaining_letters[1:]
                    ))
        return None


def solve_cryptarithmetic(words, result):
    solver = CryptarithmeticSolver(words, result)
    return solver.best_first_search()


def on_solve():
    words = entry_words.get().upper().replace(" ", "").split(',')
    result_word = entry_result.get().upper().strip()

    if len(words) < 2:
        messagebox.showerror("Error", "Enter at least two words.")
        return

    if not result_word.isalpha() or not all(word.isalpha() for word in words):
        messagebox.showerror("Error", "Words must only contain letters.")
        return

    total_letters = set(''.join(words + [result_word]))
    if len(total_letters) > 10:
        messagebox.showerror("Error", "Too many unique letters (max 10 allowed).")
        return

    solution = solve_cryptarithmetic(words, result_word)

    if solution:
        result_text = "Solution Found:\n"
        for letter, digit in sorted(solution.items()):
            result_text += f"{letter}: {digit}\n"

        def word_to_num(word):
            return int(''.join(str(solution[letter]) for letter in word))

        word_nums = [word_to_num(word) for word in words]
        result_num = word_to_num(result_word)

        result_text += "\nVerification:\n"
        for word, num in zip(words, word_nums):
            result_text += f"{word}: {num}\n"
        result_text += f"{result_word}: {result_num}\n"
        result_text += f"\nEquation Check: {' + '.join(map(str, word_nums))} == {result_num}\n"
        result_text += f"Correct: {sum(word_nums) == result_num}"

        result_label.config(text=result_text)
    else:
        messagebox.showinfo("No Solution", "No valid solution found.")


# GUI Setup
root = tk.Tk()
root.title("Cryptarithmetic Solver")
root.geometry("500x450")

tk.Label(root, text="Enter Words (comma-separated):").pack()
entry_words = tk.Entry(root, width=40)
entry_words.pack()

tk.Label(root, text="Enter Result Word:").pack()
entry_result = tk.Entry(root, width=40)
entry_result.pack()

tk.Button(root, text="Solve", command=on_solve).pack(pady=10)

result_label = tk.Label(root, text="", justify="left", wraplength=480)
result_label.pack()

root.mainloop()


