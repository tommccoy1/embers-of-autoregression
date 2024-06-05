
import random
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

fi = open("counting_common_words.txt", "r")

words = []
for line in fi:
    word = line.strip().split()[-1]
    words.append(word)


fo = open("../examples/sorting_words_examples.txt", "w")


for _ in range(100):
    found = False
    while not found:
        length = random.choice(list(range(10,21)))
        word_list = []
        for _ in range(length):
            word = random.choice(words)
            word_list.append(word)

        # Ensure no repeats
        if len(list(set(word_list))) == len(word_list):
            found = True

    fo.write(", ".join(word_list) + "\n")









