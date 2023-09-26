
import jsonlines


# Functions for encoding in rot-2 or rot-13
alphabet = "abcdefghijklmnopqrstuvwxyz"
rot2 = {}
rot13 = {}
for index, char in enumerate(alphabet):
    rot2[char] = alphabet[(index+2)%26]
    rot13[char] = alphabet[(index+13)%26]

def rot2_encode(sequence):
    new_sequence = []
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

for fi_name, fo_name in [("../examples/sentences_high_probability.txt", "../stimuli/rot2enc_highprob.jsonl"), ("../examples/sentences_medium_probability.txt", "../stimuli/rot2enc_mediumprob.jsonl"), ("../examples/sentences_adversarial.txt", "../stimuli/rot2enc_adversarial.jsonl"), ("../examples/sentences_low_probability.txt", "../stimuli/rot2enc_lowprob.jsonl")]:
    
    fi = open(fi_name, "r")
    fo2 = open(fo_name, "w")
    jsl2 = jsonlines.Writer(fo2)
    fo13 = open(fo_name.replace("rot2", "rot13"), "w")
    jsl13 = jsonlines.Writer(fo13)

    count_encoded = 0
    for line in fi:
        example2 = {}
        example13 = {}

        # Task
        example2["task_name"] = "rot2"
        example13["task_name"] = "rot13"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example2["example_type"] = example_type
        example13["example_type"] = example_type


        sentence = line.strip()
        encoded2 = rot2_encode(sentence)
        encoded13 = rot13_encode(sentence)

        
        # Instruction
        example2["task_instruction"] = 'Rot-2 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, here is a message and its corresponding version in rot-2:\nOriginal text: "Stay here!"\nRot-2 text: "Uvca jgtg!"\n\nHere is another message. Encode this message in rot-2:\nOriginal text: "%s"\nRot-2 text:'
        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message and its corresponding version in rot-13:\nOriginal text: "Stay here!"\nRot-13 text: "Fgnl urer!"\n\nHere is another message. Encode this message in rot-13:\nOriginal text: "%s"\nRot-13 text:'

        # Input
        example2["input"] = sentence
        example13["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example2["instruction_plus_input"] = example2["task_instruction"] % example2["input"]
        example13["instruction_plus_input"] = example13["task_instruction"] % example13["input"]

        # The correct output
        example2["correct_output"] = encoded2
        example13["correct_output"] = encoded13


        jsl2.write(example2)
        jsl13.write(example13)
        

        count_encoded += 1
        if count_encoded == 100:
            break


    





