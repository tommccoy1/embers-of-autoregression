
from random import shuffle

fi = open("single_tokens_by_freq.txt", "r")
words = []
for line in fi:
    parts = line.strip().split()

    words.append(parts[1])

shuffle(words)

fo = open("../examples/spelling.txt", "w")
for word in words[:1000]:
    fo.write(word + "\n")





