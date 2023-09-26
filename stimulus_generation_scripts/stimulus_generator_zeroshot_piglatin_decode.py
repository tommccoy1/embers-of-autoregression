
import jsonlines


letters = "abcdefghijklmnopqrstuvwxyz'’"
def is_roman(word):
    for char in word:
        if char.lower() not in letters:
            return False

    return True

# Function for converting a sentence to Pig Latin or Boar Etruscan
def pig_encode(sentence, suffix="ay", vowel_consonant=""):
    words = sentence.lower().split()
    new_sentence = []
    for word in words:
        punct = ""
        if word[-1] in [".", "?", "!", ",", ";", ":", "”"] and word[:-1].isalpha():
            punct = word[-1]
            word = word[:-1]

        prefix = ""
        if word[0] in ["“"] and word[1:].isalpha():
            prefix = word[0]
            word = word[1:]

        if (not word.isalpha() or word[0] == "q") and not (word == "—" or word == "–"):

            usable = True
            for char in word:
                if char.isalpha() or char in ["'", "’", "“", "”"]:
                    continue
                else:
                    print("\"" + word + "\"", char)
                    return "UNUSABLE"

        if word == "—" or word == "–":
            new_word = word
        elif word[0] in ["a", "e", "i", "o", "u"]:
            if is_roman(word):
                new_word = prefix + word + vowel_consonant + suffix
            else:
                print("UNHANDLED WORD VOWEL-INITIAL", word)
                15/0

        elif word[0] == "y":
            if is_roman(word):
                new_word = prefix + word[1:] + "y" + suffix
            else:
                print("UNHANDLED WORD Y-INITIAL", word)
                15/0
        else:
            if is_roman(word):
                index_vowel = 0
                while word[index_vowel] not in ["a", "e", "i", "o", "u", "y"]:
                    index_vowel += 1
                new_word = prefix + word[index_vowel:] + word[:index_vowel] + suffix
            else:
                print("UNHANDLED WORD CONSONANT-INITIAL", word)
                15/0
        
        new_sentence.append(new_word + punct)
    
    return " ".join(new_sentence)




print(pig_encode("stay"))
print(pig_encode("stay", suffix="uv"))

for suffix, vowel_consonant in [("ay", ""), ("uv", ""), ("ay", "w"), ("ay", "y"), ("ay", "h"), ("ay", "s"), ]:
    for condition_in, condition_out in [("high_probability", "highprob"), ("medium_probability", "mediumprob"), ("low_probability", "lowprob"), ("adversarial", "adversarial")]:
        fi_name = "../examples/piglatin_" + condition_in + ".txt"
        fo_name = "../stimuli/zeroshot_pigdec_" + vowel_consonant + suffix + "_" + condition_out + ".jsonl"
        fi = open(fi_name, "r")
        fo = open(fo_name, "w")
        jsl = jsonlines.Writer(fo)

        count_encoded = 0
        for line in fi:
            example = {}

            # Task
            example["task_name"] = "pig_latin_decode_" + vowel_consonant + suffix

            # Condition
            example_type = fo_name.split("_")[1].split(".")[0]
            example["example_type"] = example_type


            sentence = line.strip().lower()
            encoded = pig_encode(sentence, suffix=suffix, vowel_consonant=vowel_consonant)

            # Instruction
            if suffix == "ay":
                language_name = "Pig Latin"
            elif suffix == "uv":
                language_name = "Boar Etruscan"

            example["task_instruction"] = 'There is a secret way of talking called ' + language_name + ' in which you move the first consonant cluster of each word to the end of the word, and then add -' + suffix + ' to the end of the word. If the word starts with a vowel, you simply add -' + vowel_consonant + suffix + ' to the end without otherwise changing the word. Convert this sentence from ' + language_name + ' to English:\n' + language_name + ': "%s"\nEnglish:'

            # Input
            example["input"] = encoded

            # Combining the instruction and input (this is the string that should be given to the model)
            example["instruction_plus_input"] = example["task_instruction"] % example["input"]

            # The correct output
            example["correct_output"] = sentence


            jsl.write(example)
        
            count_encoded += 1
            if count_encoded == 100:
                break


    





