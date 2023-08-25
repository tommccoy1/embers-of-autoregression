
import random

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")


def get_split(tokens):
    splits = [str(len(x)) for x in tokens]
    splits = "".join(splits)
    return splits


troublesome_letters = "j"

fi_lower = open("vocab_tokens_lower.txt", "r")
fi_upper = open("vocab_tokens_upper.txt", "r")

# We'll be organizing the vocab by "split points" - the index where
# the first token ends (all our words are 2 tokens long)
vocab_upper = {}

vocab_by_first = {}
vocab_by_second = {}

# Organize the lowercase vocabulary by split points
lower_list = []
for index, line in enumerate(fi_lower):
    word = line.strip().split("\t")[1].lower()

    tokens = enc.encode(word)
    tokens_spaced = enc.encode(" " + word)

    chars = [enc.decode([tokens[i]]).strip() for i in range(len(tokens))]
    chars_spaced = [enc.decode([tokens_spaced[i]]).strip() for i in range(len(tokens_spaced))]

    splits = get_split(chars)
    splits_spaced = get_split(chars_spaced)

    # Ignore words whose split point varies by spacing
    if splits != splits_spaced:
        continue

    contains_troublesome_letter = False
    for letter in troublesome_letters:
        if letter in word:
            contains_troublesome_letter = True
    if contains_troublesome_letter:
        continue

    lower_list.append((word, splits))


# Organize the uppercase vocabulary by split points
upper_list = []
for index, line in enumerate(fi_upper):
    word = line.strip().split("\t")[1].lower()

    tokens = enc.encode(word.upper())
    tokens_spaced = enc.encode(" " + word.upper())

    chars = [enc.decode([tokens[i]]).strip() for i in range(len(tokens))]
    chars_spaced = [enc.decode([tokens_spaced[i]]).strip() for i in range(len(tokens_spaced))]

    splits = get_split(chars)
    splits_spaced = get_split(chars_spaced)

    # Ignore words whose split point varies by spacing
    if splits != splits_spaced:
        continue


    contains_troublesome_letter = False
    for letter in troublesome_letters:
        if letter in word:
            contains_troublesome_letter = True
    
    if contains_troublesome_letter:
        continue

    upper_list.append((word, splits))



print("UPPER LENGTH", len(upper_list))
print("LOWER LENGTH", len(lower_list))

# Indices within the vocab lists that we will draw from for each frequency stratum
# E.g., for the 4th lowercase stratum, we will use positions 2250 to 2950
lower_splits = [(0,1000), (1500,2500), (3000,4000), (4500,5500), (6000,7000)]
upper_splits = [(0,400), (440,840), (880,1280), (1320,1720), (1760,2160)]


# Organize the vocabulary by first or second letters (relevant for 
# first-letter or second-letter acronyms)
for index, (lower_start, lower_end) in enumerate(lower_splits):
    for lower_word in lower_list[lower_start:lower_end]:

        first = lower_word[0][0]
        if first not in vocab_by_first:
            vocab_by_first[first] = {}

        if lower_word[1] not in vocab_by_first[first]:
            vocab_by_first[first][lower_word[1]] = [{}, {}, {}, {}, {}]
        vocab_by_first[first][lower_word[1]][index][lower_word[0]] = 1

        second = lower_word[0][1]
        if second not in vocab_by_second:
            vocab_by_second[second] = {}

        if lower_word[1] not in vocab_by_second[second]:
            vocab_by_second[second][lower_word[1]] = [{}, {}, {}, {}, {}]
        vocab_by_second[second][lower_word[1]][index][lower_word[0]] = 1

for index, (upper_start, upper_end) in enumerate(upper_splits):
    for upper_word in upper_list[upper_start:upper_end]:
        if upper_word[1] not in vocab_upper:
            vocab_upper[upper_word[1]] = [{}, {}, {}, {}, {}]
        vocab_upper[upper_word[1]][index][upper_word[0]] = 1


# Dictionaries that return output files, organized by the commonness of outputs and inputs
# e.g., "13" means "very common output, medium input"; "54" means "very rare output, rare input"
fo_1_dict = {}
fo_2_dict = {}
for first in range(1,6):
    for second in range(1,6):
        if first == 1 or second == 1:
            fo_1_dict[(first, second)] = open("../examples/acronym1_" + str(first) + str(second) + ".txt", "w")
            fo_2_dict[(first, second)] = open("../examples/acronym2_" + str(first) + str(second) + ".txt", "w")


# Produce examples. Across all files, the examples should have the same split points for
# both the output word and all words in the input.
for example_index in range(1000):
    if example_index % 100 == 0:
        print(example_index)
    
    # It may take many tries to find a suitable example, given that we are requiring
    # the same split points
    found = False
    while not found:
        examples1 = {}
        examples2 = {}

        for first in range(1,6):
            for second in range(1,6):
                if first == 1 or second == 1:
                    # Output, input_list (starting as None, empty_list)
                    examples1[(first, second)] = [None, []]
                    examples2[(first, second)] = [None, []]


        possible_output_split_points = []
        for split_point in vocab_upper:
            in_all = True
            for outer_index in range(1,6):
                if len(vocab_upper[split_point][outer_index-1]) == 0:
                    in_all = False

            if in_all:
                for _ in vocab_upper[split_point][0]:
                    possible_output_split_points.append(split_point)

        output_split_point = random.choice(possible_output_split_points)

        # We need a different output for each output commonness level, but it's the 
        # same within output commonness levels (as input commonness varies)
        outputs = []
        for outer_index in range(1,6):
            output = random.choice(list(vocab_upper[output_split_point][outer_index-1].keys()))
            outputs.append(output)
            for inner_index in range(1,6):
                if outer_index == 1 or inner_index == 1:
                    examples1[(outer_index, inner_index)][0] = output
                    examples2[(outer_index, inner_index)][0] = output



        # Now attempt to find input words
        found = True
        for char_index in range(7):
            #print("C" + str(char_index))
            output_chars = [output[char_index] for output in outputs]

            # Find what split points, if any, could work for all conditions
            possible_input_split_points_1 = {}
            possible_input_split_points_2 = {}
            for first in range(1,6):
                for second in range(1,6):
                    if first == 1 or second == 1:
                        possible_input_split_points_1[(first, second)] = []
                        possible_input_split_points_2[(first, second)] = []

            
            for first in range(1,6):
                for second in range(1,6):

                    if first == 1 or second == 1:
                    
                        for split_point in vocab_by_first[output_chars[first-1]]:
                            for _ in vocab_by_first[output_chars[first-1]][split_point][second-1]:
                                possible_input_split_points_1[(first, second)].append(split_point)

                        for split_point in vocab_by_second[output_chars[first-1]]:
                            for _ in vocab_by_second[output_chars[first-1]][split_point][second-1]:
                                possible_input_split_points_2[(first, second)].append(split_point)

            filtered_split_points = []
            for split_point in possible_input_split_points_1[(1,1)]:
                in_all = True
                for first in range(1,6):
                    for second in range(1,6):
                        if first == 1 or second == 1:
                            if split_point not in possible_input_split_points_1[(first,second)]:
                                in_all = False
                            if split_point not in possible_input_split_points_2[(first,second)]:
                                in_all = False
                if in_all:
                    filtered_split_points.append(split_point)

            # If there are no split points that work for all conditions, we have to 
            # give up on this round and try again
            if len(filtered_split_points) == 0:
                found = False
                break

            input_split_point = random.choice(filtered_split_points)
            for key in possible_input_split_points_1:
                if input_split_point not in possible_input_split_points_1[key]:
                    found = False
            for key in possible_input_split_points_2:
                if input_split_point not in possible_input_split_points_2[key]:
                    found = False

            if not found:
                break

            for first in range(1,6):
                for second in range(1,6):
                    if first == 1 or second == 1:
                        first_word = random.choice(list(vocab_by_first[output_chars[first-1]][input_split_point][second-1].keys()))
                        examples1[(first, second)][1].append(first_word)
    
                        second_word = random.choice(list(vocab_by_second[output_chars[first-1]][input_split_point][second-1].keys()))
                        examples2[(first, second)][1].append(second_word)


    # Write the examples to the relevant files
    if found:
        for first in range(1,6):
            for second in range(1,6):
                if first == 1 or second == 1:
                    fo_1_dict[(first, second)].write(examples1[(first, second)][0].upper() + "\t" + " ".join(examples1[(first, second)][1]) + "\n")
                    fo_2_dict[(first, second)].write(examples2[(first, second)][0].upper() + "\t" + " ".join(examples2[(first, second)][1]) + "\n")
                        

    
    

