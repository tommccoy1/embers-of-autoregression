
import tiktoken
from collections import Counter

enc = tiktoken.get_encoding("cl100k_base")

fi = open("../wikitext-103/wiki.train.tokens", "r")
vocab_upper = Counter()
vocab_lower = Counter()

alphabet = "abcdefghijklmnopqrstuvwxyz"
def only_roman(word):
    for char in word:
        if char not in alphabet:
            return False

    return True


tokens_dict = {}

for index, line in enumerate(fi):
    if index % 100000 == 0:
        print(index)

    words = line.strip().split()

    for word in words:
        if word.islower():

            lower_word = word.lower()

            if only_roman(lower_word):
                if lower_word in tokens_dict:
                    lower_tokens = tokens_dict[lower_word][0]
                    lower_tokens_spaced = tokens_dict[lower_word][1]
                else:
                    lower_tokens = len(enc.encode(lower_word))
                    lower_tokens_spaced = len(enc.encode(" " + lower_word))
                    tokens_dict[lower_word] = [lower_tokens, lower_tokens_spaced]
               
                if lower_tokens == lower_tokens_spaced:
                    pair = (lower_word, lower_tokens)
                    if pair not in vocab_lower:
                        vocab_lower[pair] = 0
                    vocab_lower[pair] += 1


fo_lower = open("../wikitext-103/counting_tokens.txt", "w")
for pair in vocab_lower.most_common():
    count = vocab_lower[pair[0]]
    word = pair[0][0]
    tokens = pair[0][1]
    
    if count >= 20:
        fo_lower.write(str(count) + "\t" + str(tokens) + "\t" + str(word) + "\n")






