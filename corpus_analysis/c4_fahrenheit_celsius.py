

import jsonlines
import sys

from nltk import word_tokenize

from datasets import load_dataset
ds = load_dataset("c4", "en", split="train", streaming=True)

count_printed = 0
fo = open("fahrenheit_celsius_pairs.txt", "w")
for index, obj in enumerate(ds):
    if count_printed % 100 == 0 and count_printed != 0:
        print(count_printed)

    if count_printed >= 10000:
        break

    line = obj["text"].lower()
    lines = line.split("\n")

    for line in lines:
        if ("fahrenheit" in line and "celsius" in line) or ("°f" in line and "°c" in line):
            words = word_tokenize(line)
            prev = None
            
            f = None
            c = None

            for word in words:
                if word == "fahrenheit":
                    f = prev
                elif word == "celsius":
                    c = prev
                elif word == "°f":
                    f = prev
                elif word == "°c":
                    c = prev
                elif word.endswith("°f"):
                    f = word.replace("°f", "")
                elif word.endswith("°c"):
                    c = word.replace("°c", "")

                prev = word[:]

            if f is None or c is None:
                continue

            try:
                f_float = float(f)
                c_float = float(c)

                fo.write(f + "\t" + c + "\n")

                count_printed += 1
            except:
                #print(line)
                #print(f)
                #print(c)
                #print("")
                continue






