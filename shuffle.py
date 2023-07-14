
from random import shuffle

fi = open("sentence_outputs/low_probability.txt", "r")

lengths = []
all_words = []

def remove_excess_spaces(string):
    if "  " in string:
        return remove_excess_spaces(string.replace("  ", " "))
    else:
        return string

def only_alnum(string):
    new_string = []
    for char in string:
        if char.isalnum() or char == " ":
            new_string.append(char)

    return remove_excess_spaces("".join(new_string))

for index, line in enumerate(fi):
    if index >= 100:
        break
    words = only_alnum(line.strip()).lower().split()
    lengths.append(len(words))
    all_words = all_words + words[:]

shuffle(all_words)
fo = open("sentence_outputs/random.txt", "w")
start_index = 0
for length in lengths:
    line = all_words[start_index:start_index+length]
    fo.write(" ".join(line) + "\n")
    start_index = start_index+length
    

