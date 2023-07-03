
import jsonlines


# Functions for encoding in rot-2 or rot-13

def pig_encode(sentence, suffix="ay"):
    words = sentence.lower().split()
    new_sentence = []
    for word in words:
        punct = ""
        if word[-1] in [".", "?", "!", ",", ";", ":"] and word[:-1].isalpha():
            punct = word[-1]
            word = word[:-1]

        if not word.isalpha() or word[0] == "q":
            return "UNUSABLE"

        if word[0] in ["a", "e", "i", "o", "u"]:
            new_word = word + suffix
        elif word[0] == "y":
            new_word = word[1:] + "y" + suffix
        else:
            index_vowel = 0
            while word[index_vowel] not in ["a", "e", "i", "o", "u", "y"]:
                index_vowel += 1
            new_word = word[index_vowel:] + word[:index_vowel] + suffix
        
        new_sentence.append(new_word + punct)
    
    return " ".join(new_sentence)




print(pig_encode("stay"))
print(pig_encode("stay", suffix="eb"))

for fi_name, fo_name in [("sentence_outputs/high_probability_piglatin.txt", "stimuli/pig_highprob.jsonl"), ("sentence_outputs/low_probability_piglatin.txt", "stimuli/pig_lowprob.jsonl"), ("sentence_outputs/adversarial_piglatin.txt", "stimuli/pig_adversarial.jsonl"), ("sentence_outputs/random_piglatin.txt", "stimuli/pig_random.jsonl")]:
    
    fi = open(fi_name, "r")
    fo_pig = open(fo_name, "w")
    jsl_pig = jsonlines.Writer(fo_pig)
    fo_boar = open(fo_name.replace("pig", "boar"), "w")
    jsl_boar = jsonlines.Writer(fo_boar)

    count_encoded = 0
    for line in fi:
        example_pig = {}
        example_boar = {}

        # Task
        example_pig["task_name"] = "pig_latin"
        example_boar["task_name"] = "boar_etruscan"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example_pig["example_type"] = example_type
        example_boar["example_type"] = example_type


        sentence = line.strip().lower()
        encoded_pig = pig_encode(sentence)
        encoded_boar = pig_encode(sentence, suffix="eb")

        
        # Instruction
        example_pig["task_instruction"] = 'There is a secret way of talking called Pig Latin in which you move the first consonant cluster of each word to the end of the word, and then add -ay to the end of the word. If the word starts with a vowel, you simply add -ay to the end without otherwise changing the word. For example, below is a sentence in English and its equivalent in Pig Latin:\nEnglish: "the frogs are noisy."\nPig Latin: "ethay ogsfray areay oisynay."\n\nWrite this sentence in Pig Latin: \nEnglish: "%s"\nPig Latin:'
        example_boar["task_instruction"] = 'There is a secret way of talking called Boar Etruscan in which you move the first consonant cluster of each word to the end of the word, and then add -eb to the end of the word. If the word starts with a vowel, you simply add -eb to the end without otherwise changing the word. For example, below is a sentence in English and its equivalent in Boar Etruscan:\nEnglish: "the frogs are noisy."\nBoar Etruscan: "etheb ogsfreb areeb oisyneb."\n\nWrite this sentence in Boar Etruscan: \nEnglish: "%s"\nBoar Etruscan:'

        # Input
        example_pig["input"] = sentence
        example_boar["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example_pig["instruction_plus_input"] = example_pig["task_instruction"] % example_pig["input"]
        example_boar["instruction_plus_input"] = example_boar["task_instruction"] % example_boar["input"]

        # The correct output
        example_pig["correct_output"] = encoded_pig
        example_boar["correct_output"] = encoded_boar


        jsl_pig.write(example_pig)
        jsl_boar.write(example_boar)
        

        count_encoded += 1
        if count_encoded == 100:
            break


    





