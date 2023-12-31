
import random
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

fi_common = open("counting_common_words.txt", "r")
fi_rare = open("counting_rare_words.txt", "r")

signatures = {}

def signature(word):
    tokens = enc.encode(word)
    tokens_spaced = enc.encode(" " + word)

    positions = []
    for token in tokens:
        positions.append(str(len(enc.decode([token]))))

    positions_spaced = []
    for token in tokens_spaced:
        positions_spaced.append(str(len(enc.decode([token]).strip())))

    signature_unspaced = "".join(positions)
    signature_spaced = "".join(positions_spaced)

    if signature_unspaced == signature_spaced:
        return signature_unspaced
    else:
        return None

for line in fi_common:
    word = line.strip().split()[-1]
    seq = signature(word)
    if seq is None:
        continue

    if seq not in signatures:
        signatures[seq] = [[], []]

    signatures[seq][0].append(word)


for line in fi_rare:
    word = line.strip().split()[-1]
    seq = signature(word)
    if seq is None:
        continue

    if seq not in signatures:
        signatures[seq] = [[], []]

    signatures[seq][1].append(word)

signatures_both = []
for seq in signatures:
    if signatures[seq][0] != [] and signatures[seq][1] != []:
        signatures_both.append(seq)


fo_common = open("../examples/counting_words_common.txt", "w")
fo_rare = open("../examples/counting_words_rare.txt", "w")


for length in range(1,101):
    for _ in range(30):
        words_common = []
        words_rare = []
        for _ in range(length):

            # Iterate to avoid repeats
            found = False
            while not found:
                seq = random.choice(signatures_both)
                common = random.choice(signatures[seq][0])
                rare = random.choice(signatures[seq][1])

                if common not in words_common and rare not in words_rare:
                    found = True

            words_common.append(common)
            words_rare.append(rare)

        if len(words_common) != len(list(set(words_common))) or len(words_rare) != len(list(set(words_rare))):
            print("ERROR: REPEAT")


        joined = " ".join(words_common)
        joined2 = " ".join(words_rare)

        fo_common.write(" ".join(words_common) + "\n")
        fo_rare.write(" ".join(words_rare) + "\n")








