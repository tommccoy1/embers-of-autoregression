

fi1 = open("sentence_outputs/high_probability.txt", "r")
fi2 = open("sentence_outputs/adversarial.txt", "r")

saved = {}
for line1, line2 in zip(fi1, fi2):
    saved[line1] = line2

fi3 = open("sentence_outputs/high_probability_piglatin.txt", "r")
fo = open("sentence_outputs/adversarial_piglatin.txt", "w")

for line in fi3:
    if line in saved:
        fo.write(saved[line])
    else:
        fo.write("zzz" + line)



