# Words: SEND, MORE
# Operator: +  
# Result Word: MONEY

import heapq
import operator


class CryptarithmeticSolver:
    def __init__(self, words, result, op_char):
        self.words = words
        self.result = result
        self.op_char = op_char
        self.unique_letters = list(set(''.join(words + [result])))

      
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

        if op_char not in self.operators:
            raise ValueError(f"Unsupported operator: {op_char}")

    def is_valid_assignment(self, letter_map):
        if len(set(letter_map.values())) < len(letter_map):
            return False
        try:
            word_values = []
            for word in self.words + [self.result]:
                if letter_map.get(word[0], -1) == 0:
                    return False
                num_value = int(''.join(str(letter_map[letter]) for letter in word))
                word_values.append(num_value)

            left = word_values[0]
            for val in word_values[1:-1]:
                left = self.operators[self.op_char](left, val)

            right = word_values[-1]

            
            if self.op_char == '/' and (right != left or left != int(left)):
                return False

            return abs(left - right) < 1e-6  
        except (KeyError, ValueError, ZeroDivisionError):
            return False

    def heuristic(self, letter_map):
        try:
            left = int(''.join(str(letter_map[letter]) for letter in self.words[0]))
            for word in self.words[1:]:
                val = int(''.join(str(letter_map[letter]) for letter in word))
                left = self.operators[self.op_char](left, val)
            right = int(''.join(str(letter_map[letter]) for letter in self.result))
            return abs(left - right)
        except (KeyError, ValueError, ZeroDivisionError):
            return float('inf')

    def best_first_search(self):
        if len(self.unique_letters) > 10:
            return None  

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
                if digit in used_digits:
                    continue
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


def solve_cryptarithmetic(words, result, operator_char):
    solver = CryptarithmeticSolver(words, result, operator_char)
    return solver.best_first_search()


def main():
    print("=== Cryptarithmetic Solver ===")
    words_input = input("Enter words (comma-separated): ").strip().upper()
    operator_char = input("Enter operator: ").strip()
    result_word = input("Enter result word: ").strip().upper()

    words = [w.strip() for w in words_input.split(",") if w.strip().isalpha()]
    if len(words) < 2:
        print("Error: Enter at least two words.")
        return

    if not result_word.isalpha():
        print("Error: Result word must only contain letters.")
        return

    total_letters = set(''.join(words + [result_word]))
    if len(total_letters) > 10:
        print("Error: Too many unique letters (max 10 allowed).")
        return

    solution = solve_cryptarithmetic(words, result_word, operator_char)

    if solution:
        print("\nSolution Found:")
        for letter, digit in sorted(solution.items()):
            print(f"{letter}: {digit}")

        def word_to_num(word):
            return int(''.join(str(solution[letter]) for letter in word))

        word_nums = [word_to_num(word) for word in words]
        result_num = word_to_num(result_word)

        print("\nVerification:")
        for word, num in zip(words, word_nums):
            print(f"{word}: {num}")
        print(f"{result_word}: {result_num}")

       
        expr = str(word_nums[0])
        current = word_nums[0]
        from operator import add, sub, mul, truediv
        op_func = {'+': add, '-': sub, '*': mul, '/': truediv}[operator_char]
        for val in word_nums[1:]:
            expr += f" {operator_char} {val}"
            current = op_func(current, val)
        print(f"\nEquation Check: {expr} == {result_num}")
        print(f"Correct: {abs(current - result_num) < 1e-6}")
    else:
        print("No valid solution found.")


if __name__ == "__main__":
    main()

