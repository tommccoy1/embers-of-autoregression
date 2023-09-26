
import jsonlines


# Functions for encoding in rot-1 or rot-3
alphabet = "abcdefghijklmnopqrstuvwxyz"
index2char = {}
char2index = {}
for index, char in enumerate(alphabet):
    index2char[index] = char
    char2index[char] = index

def rot_encode(sequence, n):
    new_sequence = []
    for char in sequence:
        if not char.isalpha():
            new_sequence.append(char)
        elif char.isupper():
            index = char2index[char.lower()]
            new_char = index2char[(index+n)%26]
            new_sequence.append(new_char.upper())
        else:
            index = char2index[char]
            new_char = index2char[(index+n)%26]
            new_sequence.append(new_char)

    return "".join(new_sequence)


print(rot_encode("stay", 1))
print(rot_encode("stay", 3))

for shift in range(1,26):
    for task in ["dec"]:
        for fi_name, fi_label in [("../examples/sentences_high_probability.txt", "highprob")]: 

            fo_name = "../stimuli/shift_"  +  str(shift) + ".jsonl"
    
            fi = open(fi_name, "r")
            fo = open(fo_name, "w")
            jsl = jsonlines.Writer(fo)

            count_encoded = 0
            for line in fi:
                example = {}

                # Task
                example["task_name"] = "rot-" + str(shift)

                # Condition
                example_type = fo_name.split("_")[1].split(".")[0]
                example["example_type"] = example_type


                sentence = line.strip()
                encoded = rot_encode(sentence, shift)

        
                # Instruction
                if task == "dec":
                    if shift == 1:
                        example["task_instruction"] = 'Rot-' + str(shift) + ' is a cipher in which each letter is shifted ' + str(shift) + ' position forward in the alphabet. For example, here is a message written in rot-' + str(shift) + ' along with the original text that it was created from:\nRot-' + str(shift) + ' text: "' + rot_encode("Stay here!", shift) + '"\nOriginal text: "Stay here!"\n\nHere is another message in rot-' + str(shift) + '. Decode this message to produce the original text:\nRot-' + str(shift) + ' text: "%s"\nOriginal text:'
                    else:
                        example["task_instruction"] = 'Rot-' + str(shift) + ' is a cipher in which each letter is shifted ' + str(shift) + ' positions forward in the alphabet. For example, here is a message written in rot-' + str(shift) + ' along with the original text that it was created from:\nRot-' + str(shift) + ' text: "' + rot_encode("Stay here!", shift) + '"\nOriginal text: "Stay here!"\n\nHere is another message in rot-' + str(shift) + '. Decode this message to produce the original text:\nRot-' + str(shift) + ' text: "%s"\nOriginal text:'
                elif task == "enc":
                    if shift == 1:
                        example["task_instruction"] = 'Rot-' + str(shift) + ' is a cipher in which each letter is shifted ' + str(shift) + ' position forward in the alphabet. For example, here is a message and its corresponding version in rot-' + str(shift) + ':\nOriginal text: "Stay here!"\nRot-' + str(shift) + ' text: "' + rot_encode("Stay here!", shift) + '"\n\nHere is another message. Encode this message in rot-' + str(shift) + ':\nOriginal text: "%s"\nRot-' + str(shift) + ' text:'
                    else:
                        example["task_instruction"] = 'Rot-' + str(shift) + ' is a cipher in which each letter is shifted ' + str(shift) + ' positions forward in the alphabet. For example, here is a message and its corresponding version in rot-' + str(shift) + ':\nOriginal text: "Stay here!"\nRot-' + str(shift) + ' text: "' + rot_encode("Stay here!", shift) + '"\n\nHere is another message. Encode this message in rot-' + str(shift) + ':\nOriginal text: "%s"\nRot-' + str(shift) + ' text:'

                
                # Input and correct output
                if task == "dec":
                    example["input"] = encoded
                    example["correct_output"] = sentence
                else:
                    example["input"] = sentence
                    example["correct_output"] = encoded

                # Combining the instruction and input (this is the string that should be given to the model)
                example["instruction_plus_input"] = example["task_instruction"] % example["input"]


                jsl.write(example)
        

                count_encoded += 1
                if count_encoded == 100:
                    break


    





