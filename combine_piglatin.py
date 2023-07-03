

fi1 = open("sentence_outputs/high_probability_piglatin_verified.txt", "r")
fi2 = open("sentence_outputs/high_probability_piglatin_verified2.txt", "r")
fi3 = open("sentence_outputs/high_probability_piglatin_verified3.txt", "r")


fo = open("sentence_outputs/high_probability_piglatin.txt", "w")
for fi in [fi1, fi2, fi3]:
    for line in fi:
        fo.write(line)



