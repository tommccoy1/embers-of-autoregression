
import random


troublesome_letters = "kjxzqgwbf"

fi = open("wikitext-103/vocab.txt", "r")
vocab = [{}, {}, {}]
vocab_by_first = {}
vocab_by_second = {}
for index, line in enumerate(fi):
    word = line.strip()

    contains_troublesome_letter = False
    for letter in troublesome_letters:
        if letter in word:
            contains_troublesome_letter = True
    if contains_troublesome_letter:
        continue

    if len(word) > 8:
        continue

    if index < 500:
        vocab[0][word] = 1
    elif 5000 <= index and index < 6000:
        vocab[1][word] = 1
    elif 19000 <= index and index < 20000:
        vocab[2][word] = 1

    first = word[0]
    if first not in vocab_by_first:
        # 0-500, 5000-6000, 19000-20000
        vocab_by_first[first] = [{}, {}, {}]

    if index < 500:
        vocab_by_first[first][0][word] = 1
    elif 5000 <= index and index < 6000:
        vocab_by_first[first][1][word] = 1
    elif 19000 <= index and index < 20000:
        vocab_by_first[first][2][word] = 1

    second = word[1]
    if second not in vocab_by_second:
        # 0-500, 5000-6000, 19000-20000
        vocab_by_second[second] = [{}, {}, {}]

    if index < 500:
        vocab_by_second[second][0][word] = 1
    elif 5000 <= index and index < 6000:
        vocab_by_second[second][1][word] = 1
    elif 19000 <= index and index < 20000:
        vocab_by_second[second][2][word] = 1


output_word_lengths = []
for output_word_index, output_name in [(1, "medium"), (2, "rare"), (0, "common")]:
    
    output_words = []
    if output_word_lengths == []:
        for _ in range(100):
            found = False
            while not found:
                output_word = random.choice(list(vocab[output_word_index].keys()))
                if output_word not in output_words:
                    found = True
            output_words.append(output_word)
            output_word_lengths.append(len(output_word))
    else:
        for example_index in range(100):
            length = output_word_lengths[example_index]

            found = False
            while not found:
                output_word = random.choice(list(vocab[output_word_index].keys()))
                if len(output_word) == length and output_word not in output_words:
                    found = True
            output_words.append(output_word)
    print(output_name)
    print(len(list(set(output_words))))
    print("")

    for option_word_index, option_name in [(0, "common"), (1, "medium"), (2, "rare")]:
        fo1 = open("sentence_outputs/acronyms_stratified_first_" + output_name + "_" + option_name + ".txt", "w")
        fo2 = open("sentence_outputs/acronyms_stratified_second_" + output_name + "_" + option_name + ".txt", "w")
        
        for inner_example_index in range(100):
            output_word = output_words[inner_example_index]

            sequence1 = []
            sequence2 = []
            for char in output_word:
                options1 = list(vocab_by_first[char][option_word_index].keys())
                word1 = random.choice(options1)
                sequence1.append(word1)

                options2 = list(vocab_by_second[char][option_word_index].keys())
                word2 = random.choice(options2)
                sequence2.append(word2)

            fo1.write(output_word + "\t" + " ".join(sequence1) + "\n")
            fo2.write(output_word + "\t" + " ".join(sequence2) + "\n")



