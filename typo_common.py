
import random

typo_file = open("TOEFL-Spell/Annotations.tsv", "r")

typos = {}
first = True
for line in typo_file:
    if first:
        first = False
        continue

    parts = line.strip().split()
    typo = parts[2]
    correct = parts[4]

    if correct not in typos:
        typos[correct] = {}

    if typo not in typos[correct]:
        typos[correct][typo] = 0

    typos[correct][typo] += 1



fi = open("sentence_outputs/high_probability.txt", "r")
fo = open("sentence_outputs/typo_common.txt", "w")


for line in fi:
    sentence = line.strip()
    words = sentence.split()

    candidates = []
    for index in range(len(words)):
        word = words[index]

        if word in typos:

            for typo in typos[word]:
                if abs(len(typo) - len(word)) < 3:
                    candidates.append([typos[word][typo], typo, index, word])

    candidates = sorted(candidates, key=lambda x: len(x[3]))[::-1]
    selection = candidates[0]
    new_word = selection[1]
    index = selection[2]


    new_words = words[:]
    new_words[index] = new_word
    new_sentence = " ".join(new_words)
    fo.write(new_sentence + "\n")

    print(selection[3])
    print(selection[1])
    print("")



