


fi1 = open("sentence_outputs/high_probability.txt", "r")
fi2 = open("sentence_outputs/low_probability.txt", "r")
fi3 = open("sentence_outputs/adversarial.txt", "r")
fi4 = open("sentence_outputs/typo.txt", "r")
fi5 = open("sentence_outputs/typo_common.txt", "r")
fi6 = open("sentence_outputs/random.txt", "r")
fi7 = open("sentence_outputs/templatic.txt", "r")

fo = open("sentence_outputs/combined.txt", "w")
for line1, line2, line3, line4, line5, line6, line7  in zip(fi1, fi2, fi3, fi4, fi5, fi6, fi7):
    fo.write("\t".join([line1.strip(), line2.strip(), line3.strip(), line4.strip(), line5.strip(), line6.strip(), line7.strip()]) + "\n")

