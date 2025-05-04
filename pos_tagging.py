# The/DT minisolar/?? system/?? has/VBZ a/DT planet/??? called/??? Jupiter/??? that/WDT has/VBZ many/JJ moons/??? which/WDT never/??? caught/??? fire/?? .
import re

def fill_missing_tags(tagged_sentence):

    existing_tags = set(re.findall(r'/([A-Z]{2,4})', tagged_sentence))
    existing_tags.discard('??')
    existing_tags.discard('???')

    guess_tags = {
        "system": "NN",
        "star": "NN",
        "caught": "VBN",
        "fire": "NN",
        "planet": "NN",
        "Jupiter": "NNP",
        "called": "VBN",
        "moons": "NNS",
        "never": "RB",
        "minisolar": "JJ"
    }


    def replacer(match):
        word = match.group(1)
        missing_tag = match.group(2)
        guessed_tag = guess_tags.get(word.lower(), 'NN')
        if guessed_tag in existing_tags:
            return f"{word}/{guessed_tag}"
        return f"{word}/{guessed_tag}"


    filled_sentence = re.sub(r'(\w+)/(\?{2,3})', replacer, tagged_sentence)

    return filled_sentence


print("Enter a POS-tagged sentence with missing tags (use ?? or ???):")
input_sentence = ""
print("(End your input with a blank line)")


while True:
    line = input()
    if line.strip() == "":
        break
    input_sentence += line + "\n"

output_sentence = fill_missing_tags(input_sentence.strip())
print("\nCorrected Sentence:\n")
print(output_sentence)
