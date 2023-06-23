
import random

fi = open("sentence_outputs/high_probability.txt", "r")
fo = open("sentence_outputs/typo.txt", "w")


for line in fi:
    sentence = line.strip()
    words = sentence.split()

    found = False
    while not found:
        index = random.choice(list(range(len(words))))
        word = words[index]
        if len(word) < 4 or (not word[-1].isalnum() and len(word) < 5):
            continue

        if not word[-1].isalnum():
            typo_index = random.choice(list(range(len(word)))[1:-3])
            print("A", typo_index, len(word))
        else:
            typo_index = random.choice(list(range(len(word)))[1:-2])
            print("B", typo_index, len(word))

        new_word = word[:typo_index] + word[typo_index+1] + word[typo_index] + word[typo_index+2:]
        if word[typo_index+1].isalpha() and word[typo_index].isalpha():
            found = True

    new_words = words[:]
    new_words[index] = new_word
    new_sentence = " ".join(new_words)
    fo.write(new_sentence + "\n")


