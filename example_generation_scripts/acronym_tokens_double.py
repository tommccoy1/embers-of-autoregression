
import tiktoken
from collections import Counter

enc = tiktoken.get_encoding("cl100k_base")

fi = open("../wikitext-103/wiki.train.tokens", "r")
vocab_upper = Counter()
vocab_lower = Counter()

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def only_roman(word):
    for char in word:
        if char not in alphabet:
            return False

    return True


for line in fi:
    words = line.strip().split()

    for word in words:
        if word.islower():

            upper_word = word.upper()
            lower_word = word.lower()

            if len(upper_word) == 7 and only_roman(upper_word):
                upper_tokens = len(enc.encode(upper_word))
                lower_tokens = len(enc.encode(lower_word))

                upper_tokens_spaced = len(enc.encode(" " + upper_word))
                lower_tokens_spaced = len(enc.encode(" " + lower_word))
                
                if upper_tokens == 2 and upper_tokens_spaced == 2:
                    if upper_word not in vocab_upper:
                        vocab_upper[upper_word] = 0
                    vocab_upper[upper_word] += 1

                if lower_tokens == 2 and lower_tokens_spaced == 2:
                    if lower_word not in vocab_lower:
                        vocab_lower[lower_word] = 0
                    vocab_lower[lower_word] += 1

fo_upper = open("../wikitext-103/vocab_double_tokens_upper.txt", "w")
for word in vocab_upper.most_common():
    fo_upper.write(str(word[1]) + "\t" + word[0] + "\n")

fo_lower = open("../wikitext-103/vocab_double_tokens_lower.txt", "w")
for word in vocab_lower.most_common():
    fo_lower.write(str(word[1]) + "\t" + word[0] + "\n")






