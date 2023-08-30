

import jsonlines
import sys

from datasets import load_dataset
ds = load_dataset("c4", "en", split="train", streaming=True)

phrases_to_check_for = ["in alphabetical order", "in reverse alphabetical order", "in ascending order", "in descending order", "the first letter of each word", "the second letter of each word"]

phrase_counts = {}
for phrase in phrases_to_check_for:
    phrase_counts[phrase] = 0

fo_pig = open("c4_piglatin.txt", "a")
fo_general = open("c4_counts.txt", "a")

for index, obj in enumerate(ds):
    if index % 100000 == 0:
        print(index)
        print(phrase_counts)

    line = obj["text"].lower()
    if "pig latin" in line:
        fo_pig.write(line + "\n")

    for phrase in phrases_to_check_for:
        if phrase in line:
            phrase_counts[phrase] += 1


for key in phrase_counts:
    fo.write(key + "\t" + str(phrase_counts[phrase] + "\n"))


