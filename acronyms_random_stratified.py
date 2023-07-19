
import random


for option_type in ["common", "medium", "rare"]: 
    fi_first = open("sentence_outputs/acronyms_stratified_first_rare_" + option_type + ".txt", "r")
    lengths_first = []
    words_first = []
    for line in fi_first:
        words = line.strip().split("\t")[1].split()
        lengths_first.append(len(words))
        words_first = words_first + words

    fo_first = open("sentence_outputs/acronyms_stratified_first_random_" + option_type + ".txt", "w")
    random.shuffle(words_first)
    current_index = 0
    for length in lengths_first:
        seq = words_first[current_index:current_index+length]
        acronym = [x[0] for x in seq]
        fo_first.write("".join(acronym) + "\t" + " ".join(seq) + "\n")
        current_index = current_index+length




    fi_second = open("sentence_outputs/acronyms_stratified_second_rare_" + option_type + ".txt", "r")
    lengths_second = []
    words_second = []
    for line in fi_second:
        words = line.strip().split("\t")[1].split()
        lengths_second.append(len(words))
        words_second = words_second + words

    fo_second = open("sentence_outputs/acronyms_stratified_second_random_" + option_type + ".txt", "w")
    random.shuffle(words_second)
    current_index = 0
    for length in lengths_second:
        seq = words_second[current_index:current_index+length]
        acronym = [x[1] for x in seq]
        fo_second.write("".join(acronym) + "\t" + " ".join(seq) + "\n")
        current_index = current_index+length


