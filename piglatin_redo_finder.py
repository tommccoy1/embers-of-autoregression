
from nltk.tokenize import word_tokenize

fi1 = open("sentence_outputs/high_probability_piglatin.txt", "r")
fi2 = open("sentence_outputs/low_probability_piglatin.txt", "r")

fo = open("sentence_outputs/high_probability_redo_piglatin.txt", "w")
for line1, line2 in zip(fi1, fi2):

    words = words = word_tokenize(line2.strip())
    bad_first = False
    for word in words:
        if word[0].lower() == "q":
            bad_first = True
            print(word)
            break
            
        if (not (word.isalpha() or word in [".", ",", "!", ":", ";", "\"", "(", ")", ])) or (word.isupper() and len(word) > 1):
            bad_first = True
            print(word)
            break

    if bad_first:
        fo.write(line1)





