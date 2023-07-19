
import random

for output_type in ["common", "medium", "rare", "random"]:
    fi = open("sentence_outputs/acronyms_stratified_first_" + output_type + "_rare.txt", "r")
    fo = open("sentence_outputs/acronyms_stratified_first_" + output_type + "_random.txt", "w")

    for line in fi:
        parts = line.strip().split("\t")
        output = parts[0]
        words = parts[1].split()

        extra_chars = ""
        for word in words:
            extra_chars = extra_chars + word[1:]

        extra_chars = list(extra_chars)
        random.shuffle(extra_chars)
        extra_chars = "".join(extra_chars)
        new_output = []
        current_index = 0
        for word in words:
            new_word = word[0]
            remaining_length = len(word) - 1
            new_word = new_word + extra_chars[current_index:current_index + remaining_length]
            new_output.append(new_word)

            current_index = current_index + remaining_length

        fo.write(output + "\t" + " ".join(new_output) + "\n")


for output_type in ["common", "medium", "rare", "random"]:
    fi = open("sentence_outputs/acronyms_stratified_second_" + output_type + "_rare.txt", "r")
    fo = open("sentence_outputs/acronyms_stratified_second_" + output_type + "_random.txt", "w")

    for line in fi:
        parts = line.strip().split("\t")
        output = parts[0]
        words = parts[1].split()

        extra_chars = ""
        for word in words:
            extra_chars = extra_chars + word[0] + word[2:]

        extra_chars = list(extra_chars)
        random.shuffle(extra_chars)
        extra_chars = "".join(extra_chars)
        new_output = []
        current_index = 0
        for word in words:
            remaining_length = len(word) - 1
            extra_part = extra_chars[current_index:current_index + remaining_length]
            new_word = extra_part[0] + word[1] + extra_part[2:]
            new_output.append(new_word)

            current_index = current_index + remaining_length

        fo.write(output + "\t" + " ".join(new_output) + "\n")




