
from random import shuffle

fi = open("sentences/sentences_medium_probability.txt", "r")
fo = open("sentences/sentences_low_probability.txt", "w")

# Preserve the first and last words in their positions; shuffle all others
for index, line in enumerate(fi):
    words = line.strip().split()
    new_words = words[1:-1]
    shuffle(new_words)
    new_words = [words[0]] + new_words + [words[-1]]
    fo.write(" ".join(new_words) + "\n")


