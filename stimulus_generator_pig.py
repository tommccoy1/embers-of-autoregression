

consonants = ["bcdfghjklmnpqrstvwxz"]
vowels = ["aeiou"]

def pig_encode(sentence):
    words = sentence.lower().split()
    new_sentence = []
    for word in words:
        suffix = ""
        if word[-1] in [".", "?", "!", ",", ";", ":"] and word[:-1].isalpha():
            suffix = word[-1]
            word = word[:-1]

        if not word.isalpha() or word[0] == "q":
            return "UNUSABLE"

        if word[0] in ["a", "e", "i", "o", "u"]:
            new_word = word + "ay"
        elif word[0] == "y":
            new_word = word[1:] + "yay"
        else:
            index_vowel = 0
            while word[index_vowel] not in ["a", "e", "i", "o", "u", "y"]:
                index_vowel += 1
            new_word = word[index_vowel:] + word[:index_vowel] + "ay"
        
        new_sentence.append(new_word + suffix)
    
    return " ".join(new_sentence)

for fi_name, fo_name in [("sentence_outputs/high_probability.txt", "stimuli/pig_highprob.txt")]: 
    count_unusable = 0 
    fi = open(fi_name, "r")

    for line in fi:
        print(line.strip())
        print(pig_encode(line.strip()))
        print("")

        if pig_encode(line.strip()) == "UNUSABLE":
            count_unusable += 1

print("Count unusable:", count_unusable)







