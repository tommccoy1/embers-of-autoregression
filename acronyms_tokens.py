
import random


fi = open("wikitext-103/vocab_tokens.txt", "r")
vocab = {}
vocab_by_length = {}
vocab_by_first = {}
vocab_by_second = {}
for line in fi:

    if "X" in line or "Z" in line:
        continue

    word = line.strip().lower().split()[1]
    vocab[word] = 1

    length = int(line.strip().split()[0])
    if length not in vocab_by_length:
        vocab_by_length[length] = []
    vocab_by_length[length].append(word)

    first = word[0]
    if first not in vocab_by_first:
        vocab_by_first[first] = {}
    vocab_by_first[first][word] = 1

    second = word[1]
    if second not in vocab_by_second:
        vocab_by_second[second] = {}
    vocab_by_second[second][word] = 1


fo1 = open("sentence_outputs/acronyms_first_tokens.txt", "w")
fo2 = open("sentence_outputs/acronyms_second_tokens.txt", "w")
for length in range(1,5):
    for _ in range(50):
        output_word = random.choice(vocab_by_length[length])

        sequence1 = []
        sequence2 = []
        for char in output_word:
            options1 = list(vocab_by_first[char].keys())
            word1 = random.choice(options1)
            sequence1.append(word1)

            options2 = list(vocab_by_second[char].keys())
            word2 = random.choice(options2)
            sequence2.append(word2)

        fo1.write(output_word + "\t" + " ".join(sequence1) + "\n")
        fo2.write(output_word + "\t" + " ".join(sequence2) + "\n")



