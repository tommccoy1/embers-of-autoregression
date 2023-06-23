
import sys
import random


fi = open("wikitext-103/vocab.txt", "r")
vocab = {}
vocab_by_first = {}
vocab_by_second = {}
for line in fi:
    word = line.strip()
    vocab[word] = 1

    first = word[0]
    if first not in vocab_by_first:
        vocab_by_first[first] = {}
    vocab_by_first[first][word] = 1

    second = word[1]
    if second not in vocab_by_second:
        vocab_by_second[second] = {}
    vocab_by_second[second][word] = 1


output_word = sys.argv[1]

sequence1 = []
sequence2 = []
for char in output_word:
    options1 = list(vocab_by_first[char].keys())
    word1 = random.choice(options1)
    sequence1.append(word1)

    options2 = list(vocab_by_second[char].keys())
    word2 = random.choice(options2)
    sequence2.append(word2)


print(" ".join(sequence1))
print(" ".join(sequence2))




