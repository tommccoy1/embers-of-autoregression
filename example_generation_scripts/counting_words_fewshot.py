
import random
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

def generate_example():
    length = random.choice(list(range(1, 101)))
    words = []
    for _ in range(length):

        # Iterate to avoid repeats
        found = False
        while not found:
            word = random.choice(all_words)
            
            if word not in words:
                found = True

        words.append(word)

    if len(words) != len(list(set(words))):
        print("ERROR: REPEAT")

    joined = " ".join(words)

    return joined


fi_common = open("counting_common_words.txt", "r")
fo_5 = open("../examples/counting_words_5shot.txt", "w")
fo_10 = open("../examples/counting_words_10shot.txt", "w")
fo_100 = open("../examples/counting_words_100shot.txt", "w")

all_words = []
for line in fi_common:
    parts = line.strip().split()
    word = parts[1]
    all_words.append(word)


for _ in range(5):
    example = generate_example()
    fo_5.write(example + "\n")

for _ in range(10):
    example = generate_example()
    fo_10.write(example + "\n")

for _ in range(100):
    example = generate_example()
    fo_100.write(example + "\n")






