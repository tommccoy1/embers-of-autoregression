

fi1 = open("sentence_outputs/acronyms_first_word.txt", "r")
fi2 = open("sentence_outputs/acronyms_second_word.txt", "r")
fi3 = open("sentence_outputs/acronyms_first_random.txt", "r")
fi4 = open("sentence_outputs/acronyms_second_random.txt", "r")
fi5 = open("sentence_outputs/acronyms_first_adversarial.txt", "r")
fi6 = open("sentence_outputs/acronyms_second_adversarial.txt", "r")

for fi, position in [(fi1, 0), (fi2, 1), (fi3, 0), (fi4, 1), (fi5, 0), (fi6, 1)]:
    for line in fi:
        parts = line.strip().split("\t")
        word = parts[0]
        seq = parts[1].split()

        acronym = "".join([x[position] for x in seq])
        if word != acronym:
            15/0




