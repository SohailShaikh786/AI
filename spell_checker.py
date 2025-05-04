import re
from collections import Counter
from string import ascii_lowercase
import os

def words(text):
    return re.findall(r"(?:[a-z]+[a-z'\-]?[a-z]|[a-z]+)", text.lower())

def alternate_words(word):
    lst = []

    for i in ascii_lowercase:
        for j in range(len(word)+1):
            lst.append(word[:j] + i + word[j:])

    for i in range(1, len(word)):
        lst.append(word[:i-1] + word[i] + word[i-1] + word[i+1:])

    for i in range(len(word)):
        lst.append(word[:i] + word[i+1:])

    
    for i in ascii_lowercase:
        for j in range(len(word)):
            lst.append(word[:j] + i + word[j+1:])

    return lst

def valueOf(word):
    return Vocabulary[word]

def spelled_word(word):
    suggestions = set(alternate_words(word)).intersection(set(Vocabulary))
    if suggestions:
        max_score_word = max(suggestions, key=valueOf)
        return sorted([w for w in suggestions if Vocabulary[w] == Vocabulary[max_score_word]])[0]
    return word
def load_vocabulary(filepath='input.txt'):
    if not os.path.exists(filepath):
        print(" Error: 'input.txt' not found. Please ensure it exists in the same directory.")
        exit(1)
    return Counter(words(open(filepath, encoding='utf-8').read()))


Vocabulary = load_vocabulary()


try:
    n = int(input("Enter number of words to check: ").strip())
    for _ in range(n):
        word = input(" Enter word: ").strip().lower()
        if word in Vocabulary:
            print(f"Correct: {word}")
        else:
            corrected = spelled_word(word)
            print(f" Incorrect. Suggestion: {corrected}")
except Exception as e:
    print(f"Error: {e}")
