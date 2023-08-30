

import jsonlines
import sys

from nltk import word_tokenize

from datasets import load_dataset
ds = load_dataset("c4", "en", split="train", streaming=True)

number_dict = {}
for i in range(1,103):
    number_dict[str(i)] = 0


# Number of numbers we've seen
count = 0
fo = open("numbers.txt", "w")
for index, obj in enumerate(ds):

    if count >= 1000000:
        break

    line = obj["text"].lower()
    lines = line.split("\n")

    for line in lines:
        words = word_tokenize(line)
        for word in words:
            if word in number_dict:
                number_dict[word] += 1
                count += 1

                if count % 10000 == 0 and count != 0:
                    print(count)

                if count >= 1000000:
                    break

        if count >= 1000000:
            break

for i in range(1,103):
    fo.write(str(i) + "\t" + str(number_dict[str(i)]) + "\n")
        





