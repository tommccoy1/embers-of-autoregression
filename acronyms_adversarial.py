
import random


fi = open("wikitext-103/vocab.txt", "r")
vocab = {}
for line in fi:
    word = line.strip()
    vocab[word] = 1

fi_first = open("sentence_outputs/acronyms_first_word.txt", "r")
fo_first = open("sentence_outputs/acronyms_first_adversarial.txt", "w")

current_lines = []
for line in fi_first:
    current_lines.append(line)
    if len(current_lines) == 2:
        words1 = current_lines[0].strip().split("\t")[1].split()
        words2 = current_lines[1].strip().split("\t")[1].split()

        satisfied = False
        while not satisfied:
            position1 = random.choice(list(range(len(words1))))
            position2 = random.choice(list(range(len(words2))))

            replacement_from_1 = words1[position1]
            replacement_from_2 = words2[position2]

            new_words1 = words1[:]
            new_words2 = words2[:]

            new_words1[position1] = replacement_from_2
            new_words2[position2] = replacement_from_1

            new_acronym1 = "".join([x[0] for x in new_words1])
            new_acronym2 = "".join([x[0] for x in new_words2])

            if new_acronym1 not in vocab and new_acronym2 not in vocab:
                satisfied = True

        fo_first.write(new_acronym1 + "\t" + " ".join(new_words1) + "\n")
        fo_first.write(new_acronym2 + "\t" + " ".join(new_words2) + "\n")
        
        current_lines = []





fi_second = open("sentence_outputs/acronyms_second_word.txt", "r")
fo_second = open("sentence_outputs/acronyms_second_adversarial.txt", "w")

current_lines = []
for line in fi_second:
    current_lines.append(line)
    if len(current_lines) == 2:
        words1 = current_lines[0].strip().split("\t")[1].split()
        words2 = current_lines[1].strip().split("\t")[1].split()

        satisfied = False
        while not satisfied:
            position1 = random.choice(list(range(len(words1))))
            position2 = random.choice(list(range(len(words2))))

            replacement_from_1 = words1[position1]
            replacement_from_2 = words2[position2]

            new_words1 = words1[:]
            new_words2 = words2[:]

            new_words1[position1] = replacement_from_2
            new_words2[position2] = replacement_from_1

            new_acronym1 = "".join([x[1] for x in new_words1])
            new_acronym2 = "".join([x[1] for x in new_words2])

            if new_acronym1 not in vocab and new_acronym2 not in vocab:
                satisfied = True

        fo_second.write(new_acronym1 + "\t" + " ".join(new_words1) + "\n")
        fo_second.write(new_acronym2 + "\t" + " ".join(new_words2) + "\n")
        
        current_lines = []


