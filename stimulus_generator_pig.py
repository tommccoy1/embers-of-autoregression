

consonants = ["bcdfghjklmnpqrstvwxz"]
vowels = ["aeiou"]

def pig_encode(sentence):
    words = sentence.lower().split()
    new_sentence = []
    for word in sentence:
        if word[0] in ["a", "e", "i", "o", "u"]:
            new_sentence.append(word + "ay")

    for char in sequence:
        if not char.isalpha():
            new_sequence.append(char)
        elif char.isupper():
            new_sequence.append(rot2[char.lower()].upper())
        else:
            new_sequence.append(rot2[char])

    return "".join(new_sequence)

def rot13_encode(sequence):
    new_sequence = []
    for char in sequence:
        if not char.isalpha():
            new_sequence.append(char)
        elif char.isupper():
            new_sequence.append(rot13[char.lower()].upper())
        else:
            new_sequence.append(rot13[char])

    return "".join(new_sequence)


print(rot2_encode("stay"))
print(rot13_encode("stay"))

for fi_name, fo_name in [("sentence_outputs/high_probability.txt", "stimuli/rot2_highprob.txt"), ("sentence_outputs/low_probability.txt", "stimuli/rot2_lowprob.txt"), ("sentence_outputs/adversarial.txt", "stimuli/rot2_adversarial.txt"), ("sentence_outputs/random.txt", "stimuli/rot2_random.txt")]:
    
    fi = open(fi_name, "r")
    fo2 = open(fo_name, "w")
    fo13 = open(fo_name.replace("rot2", "rot13"), "w")

    count_encoded = 0
    for line in fi:
        sentence = line.strip()
        encoded2 = rot2_encode(sentence)
        encoded13 = rot13_encode(sentence)

        inp2 = 'Rot-2 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, "stay" would become "uvca". Decode the following message, which was written in rot-2: "' + encoded2 + '"'
        inp13 = 'Rot-13 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, "stay" would become "fgnl". Decode the following message, which was written in rot-13: "' + encoded13 + '"'
        
        fo2.write(inp2 + "\n")
        fo13.write(inp13 + "\n")
        count_encoded += 1
        if count_encoded == 100:
            break








