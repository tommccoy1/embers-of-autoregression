
from random import shuffle

fi = open("../examples/swap_medium_probability.txt", "r")
fo = open("../examples/swap_low_probability.txt", "w")

roman_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def is_roman(word):
    for char in word:
        if char not in roman_letters:
            return False

    return True


# Preserve the first and last words in their positions; shuffle all others
for index, line in enumerate(fi):
    found = False

    while not found:
        words = line.strip().split()
        new_words = words[1:-1]
        shuffle(new_words)
        new_words = [words[0]] + new_words + [words[-1]]
        if new_words[1] not in ["a", "an", "the"]:
            valid = True
            for index, word in enumerate(new_words):
                if word in ["a", "an", "the"]:
                    if not is_roman(new_words[index+1]) or not is_roman(new_words[index-1]) or new_words[index+1] in ["a", "an", "the"] or new_words[index-1] in ["a", "an", "the"]:
                        valid = False
            if valid:
                found = True

    fo.write(" ".join(new_words) + "\n")


