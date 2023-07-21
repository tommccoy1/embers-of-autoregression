
import random
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")


common_numbers = []
rare_numbers = []
fi_counts = open("../wikitext-103/counting_numbers.txt", "r")
numbers = {}
for line in fi_counts:
    parts = line.strip().split()
    numbers[int(parts[0])] = int(parts[1])

for n in numbers:
    if n >= 3 and n <= 103:
        if numbers[n] > 2*numbers[n-1] and numbers[n] > 2*numbers[n-2] and numbers[n] > 2*numbers[n+1] and numbers[n] > 2*numbers[n+2]:
            common_numbers.append(n)
            rare_numbers.append(n-2)
            rare_numbers.append(n-1)
            rare_numbers.append(n+1)
            rare_numbers.append(n+2)



fi_common = open("../wikitext-103/counting_common_words.txt", "r")
fi_rare = open("../wikitext-103/counting_rare_words.txt", "r")

common_words = []
rare_words = []

for line in fi_common:
    word = line.strip().split()[-1]
    common_words.append(word)

for line in fi_rare:
    word = line.strip().split()[-1]
    rare_words.append(word)



fo_common_common = open("../examples/counting_words_common_common.txt", "w")
fo_common_rare = open("../examples/counting_words_common_rare.txt", "w")
fo_rare_common = open("../examples/counting_words_rare_common.txt", "w")
fo_rare_rare = open("../examples/counting_words_rare_rare.txt", "w")


for common_number in common_numbers:
    # Each common number is repeated 100 times
    for _ in range(100):
        words_common = []
        words_rare = []

        for _ in range(common_number):
            words_common.append(random.choice(common_words))
            words_rare.append(random.choice(rare_words))

        fo_common_common.write(" ".join(words_common) + "\n")
        fo_common_rare.write(" ".join(words_rare) + "\n")


for rare_number in rare_numbers:
    # Each rare number is repeated 25 times
    for _ in range(25):
        words_common = []
        words_rare = []

        for _ in range(rare_number):
            words_common.append(random.choice(common_words))
            words_rare.append(random.choice(rare_words))

        fo_rare_common.write(" ".join(words_common) + "\n")
        fo_rare_rare.write(" ".join(words_rare) + "\n")






