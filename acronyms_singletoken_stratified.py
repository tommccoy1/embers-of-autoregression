
import random


troublesome_letters = "bjxz"

fi_lower = open("wikitext-103/vocab_single_tokens_lower.txt", "r")
fi_upper = open("wikitext-103/vocab_single_tokens_upper.txt", "r")
vocab_lower = [{}, {}]
vocab_upper = [{}, {}]
vocab_by_first = {}
vocab_by_second = {}

lower_list = []
for index, line in enumerate(fi_lower):
    word = line.strip().split("\t")[1].lower()

    contains_troublesome_letter = False
    for letter in troublesome_letters:
        if letter in word:
            contains_troublesome_letter = True
    if contains_troublesome_letter:
        continue

    lower_list.append(word)


upper_list = []
for index, line in enumerate(fi_upper):
    word = line.strip().split("\t")[1].lower()

    contains_troublesome_letter = False
    for letter in troublesome_letters:
        if letter in word:
            contains_troublesome_letter = True
    if contains_troublesome_letter:
        continue

    upper_list.append(word)

print("UPPER LENGTH", len(upper_list))
print("LOWER LENGTH", len(lower_list))
for lower_common in lower_list[:1000]:
    vocab_lower[0][lower_common] = 1

    first = lower_common[0]
    if first not in vocab_by_first:
        vocab_by_first[first] = [{}, {}]

    vocab_by_first[first][0][lower_common] = 1

    second = lower_common[1]
    if second not in vocab_by_second:
        vocab_by_second[second] = [{}, {}]

    vocab_by_second[second][0][lower_common] = 1

for lower_rare in lower_list[-1000:]:
    vocab_lower[1][lower_rare] = 1

    first = lower_rare[0]
    if first not in vocab_by_first:
        vocab_by_first[first] = [{}, {}]

    vocab_by_first[first][1][lower_rare] = 1

    second = lower_rare[1]
    if second not in vocab_by_second:
        vocab_by_second[second] = [{}, {}]

    vocab_by_second[second][1][lower_rare] = 1

for upper_common in upper_list[:500]:
    vocab_upper[0][upper_common] = 1

for upper_rare in upper_list[-500:]:
    vocab_upper[1][upper_rare] = 1



output_word_lengths = []
for output_word_index, output_name in [(0, "common"), (1, "rare")]:
    
    output_words = []
    for example_index in range(1000):

        found = False
        while not found:
            output_word = random.choice(list(vocab_upper[output_word_index].keys()))
            #if output_word not in output_words:
            #    found = True
            found = True
        output_words.append(output_word)

    for option_word_index, option_name in [(0, "common"), (1, "rare")]:
        fo1 = open("sentence_outputs/acronyms_singlestratified_first_" + output_name + "_" + option_name + ".txt", "w")
        fo2 = open("sentence_outputs/acronyms_singlestratified_second_" + output_name + "_" + option_name + ".txt", "w")
        
        for inner_example_index in range(1000):
            output_word = output_words[inner_example_index]

            sequence1 = []
            sequence2 = []
            for char in output_word:
                #print(char)
                options1 = list(vocab_by_first[char][option_word_index].keys())
                word1 = random.choice(options1)
                sequence1.append(word1)

                options2 = list(vocab_by_second[char][option_word_index].keys())
                word2 = random.choice(options2)
                sequence2.append(word2)

            fo1.write(output_word + "\t" + " ".join(sequence1) + "\n")
            fo2.write(output_word + "\t" + " ".join(sequence2) + "\n")



