
from collections import Counter
import jsonlines
from datasets import load_dataset

ds = load_dataset("c4", "en", split="train", streaming=True)

def depunct(text):
    return text.replace(".", "").replace(",", "").replace("\"", "").replace("'", "")

fi_names = open("birthday_info.txt", "r")
names = Counter()

for line in fi_names:
    name = line.strip().split("\t")[0]
    if len(name.split()) == 2:
        names[name] = 0


word_count = 0
for index, obj in enumerate(ds):
    if (index+1) % 1000000 == 0:
        print(index+1)
        print(word_count)
       
    if index > 100000000:
        print("WORD COUNT:", word_count)
        break

    text = depunct(obj["text"])
    words = text.split()
    word_count += len(words)

    for index in range(len(words) - 1):
        bigram = " ".join(words[index:index+2])
        if bigram in names:
            names[bigram] += 1
            
fo = open("birthday_counts.txt", "w")
for name, count in names.most_common():
    fo.write(str(count) + "\t" + name + "\n")




