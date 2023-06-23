


fi1 = open("sentence_outputs/acronyms_first_word.txt", "r")
fi2 = open("sentence_outputs/acronyms_first_adversarial.txt", "r")
fi3 = open("sentence_outputs/acronyms_first_random.txt", "r")
fi4 = open("sentence_outputs/acronyms_second_word.txt", "r")
fi5 = open("sentence_outputs/acronyms_second_adversarial.txt", "r")
fi6 = open("sentence_outputs/acronyms_second_random.txt", "r")

fo = open("sentence_outputs/combined_acronyms.txt", "w")
for line1, line2, line3, line4, line5, line6  in zip(fi1, fi2, fi3, fi4, fi5, fi6):
    fo.write("\t".join([line1.strip(), line2.strip(), line3.strip(), line4.strip(), line5.strip(), line6.strip()]) + "\n")

