

import jsonlines
import sys

from nltk import word_tokenize

from datasets import load_dataset
ds = load_dataset("monology/pile", streaming=True)


def is_date(word):
    if "/" not in word:
        return False, None
    if len(word) != 10:
        return False, None

    parts = word.split("/")
    if len(parts) == 3:
        if len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4:
            try:
                first = int(parts[0])
                second = int(parts[1])
                third = int(parts[2])

                if first < 13 and first > 0 and second > 13 and second < 32:
                    date_format = "mmddyyyy"
                elif second < 13 and second > 0 and first > 13 and first < 32:
                    date_format = "ddmmyyyy"
                else:
                    date_format = "unclear"

                return True, date_format

            except:
                return False, None

    return False, None

print(ds)
14/0
count_printed = 0
counts = {}
counts["mmddyyyy"] = 0
counts["ddmmyyyy"] = 0
counts["unclear"] = 0
last_printed = 100
fo = open("pile_dates.txt", "w")
for index, obj in enumerate(ds):
    if count_printed > last_printed:
        print(count_printed)
        print(counts)
        last_printed += 100

    if count_printed >= 100000:
        break

    print(obj)
    line = obj #obj["text"].lower()
    lines = line.split("\n")

    for line in lines:
        words = word_tokenize(line)

        for word in words:
            date, date_type = is_date(word)

            if date:
                counts[date_type] += 1
                fo.write(word + "\t" + date_type + "\n")
                if date_type != "unclear":
                    count_printed += 1





