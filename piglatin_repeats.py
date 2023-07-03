
fi_orig = open("sentence_outputs/high_probability.txt", "r")
fi_pig = open("sentence_outputs/high_probability_piglatin.txt", "r")


verified = {}
for line in fi_orig:
    verified[line] = 1

fo = open("sentence_outputs/high_probability_piglatin_verified.txt", "w")
for line in fi_pig:
    if line in verified:
        fo.write(line)


