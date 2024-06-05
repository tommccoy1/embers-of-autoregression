
import jsonlines


# Functions for encoding in rot-12 or rot-13
alphabet = "abcdefghijklmnopqrstuvwxyz"
rot12 = {}
rot13 = {}
for index, char in enumerate(alphabet):
    rot12[char] = alphabet[(index+12)%26]
    rot13[char] = alphabet[(index+13)%26]

def rot12_encode(sequence):
    new_sequence = []
    for char in sequence:
        if not char.isalpha():
            new_sequence.append(char)
        elif char.isupper():
            new_sequence.append(rot12[char.lower()].upper())
        else:
            new_sequence.append(rot12[char])

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


print(rot12_encode("stay"))
print(rot13_encode("stay"))

for prompt_type in ["basic", "step", "cot"]:
    for direction in ["enc", "dec"]:
        for fi_name, fo_name in [("../examples/sentences_high_probability.txt", "../stimuli/rot12" + direction + prompt_type + "_highprob.jsonl"), ("../examples/sentences_medium_probability.txt", "../stimuli/rot12" + direction + prompt_type + "_mediumprob.jsonl"), ("../examples/sentences_low_probability.txt", "../stimuli/rot12" + direction + prompt_type + "_lowprob.jsonl")]:
    
            fi = open(fi_name, "r")
            fo12 = open(fo_name, "w")
            jsl12 = jsonlines.Writer(fo12)
            fo13 = open(fo_name.replace("rot12", "rot13"), "w")
            jsl13 = jsonlines.Writer(fo13)

            count_encoded = 0
            for line in fi:
                example12 = {}
                example13 = {}

                # Task
                example12["task_name"] = "rot12"
                example13["task_name"] = "rot13"

                # Condition
                example_type = fo_name.split("_")[1].split(".")[0]
                example12["example_type"] = example_type
                example13["example_type"] = example_type


                sentence = line.strip()
                encoded12 = rot12_encode(sentence)
                encoded13 = rot13_encode(sentence)

        
                # Instruction
                if direction == "dec":
                    if prompt_type == "basic":
                        example12["task_instruction"] = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. For example, here is a message written in rot-12 along with the original text that it was created from:\nRot-12 text: "Efmk tqdq!"\nOriginal text: "Stay here!"\n\nHere is another message in rot-12. Decode this message to produce the original text:\nRot-12 text: "%s"\nOriginal text:'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message written in rot-13 along with the original text that it was created from:\nRot-13 text: "Fgnl urer!"\nOriginal text: "Stay here!"\n\nHere is another message in rot-13. Decode this message to produce the original text:\nRot-13 text: "%s"\nOriginal text:'
                    elif prompt_type == "step":
                        example12["task_instruction"] = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. For example, here is a message written in rot-12 along with the original text that it was created from:\nRot-12 text: "Efmk tqdq!"\nOriginal text: "Stay here!"\n\nHere is another message in rot-12. Decode the message to produce the original text. Make sure to think step by step. On the last line, write the words "Original text:" followed by the decoded message:\nRot-12 text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message written in rot-13 along with the original text that it was created from:\nRot-13 text: "Fgnl urer!"\nOriginal text: "Stay here!"\n\nHere is another message in rot-13. Decode the message to produce the original text. Make sure to think step by step. On the last line, write the words "Original text:" followed by the decoded message:\nRot-13 text: "%s"'
                    elif prompt_type == "cot":
                        example12["task_instruction"] = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. For example, here is a message written in rot-12:\nRot-12 text: "Efmk tqdq!"\n\nTo decode this message, we shift each letter 12 positions backward:\n1. E -> S\n2. f -> t\n3. m -> a\n4. k -> y\n5.   ->  \n6. t -> h\n7. q -> e\n8. d -> r\n9. q -> e\n10. ! -> !\n\nTherefore, the original text is: "Stay here!"\n\nHere is another message in rot-12. Decode the message one letter at a time. On the last line, write the words "Original text:" followed by the decoded message:\nRot-12 text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message written in rot-13:\nRot-13 text: "Fgnl urer!"\n\nTo decode this message, we shift each letter 13 positions backward:\n1. F -> S\n2. g -> t\n3. n -> a\n4. l -> y\n5.   ->  \n6. u -> h\n7. r -> e\n8. e -> r\n9. r -> e\n10. ! -> !\n\nTherefore, the original text is: "Stay here!"\n\nHere is another message in rot-13. Decode the message one letter at a time. On the last line, write the words "Original text:" followed by the decoded message:\nRot-13 text: "%s"'
                
                elif direction == "enc":
                    if prompt_type == "basic":
                        example12["task_instruction"] = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. For example, here is a message and its corresponding version in rot-12:\nOriginal text: "Stay here!"\nRot-12 text: "Efmk tqdq!"\n\nHere is another message. Encode this message in rot-12:\nOriginal text: "%s"\nRot-12 text:'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message and its corresponding version in rot-13:\nOriginal text: "Stay here!"\nRot-13 text: "Fgnl urer!"\n\nHere is another message. Encode this message in rot-13:\nOriginal text: "%s"\nRot-13 text:'
                    elif prompt_type == "step":
                        example12["task_instruction"] = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. For example, here is a message and its corresponding version in rot-12:\nOriginal text: "Stay here!"\nRot-12 text: "Efmk tqdq!"\n\nHere is another message. Encode this message in rot-12. Make sure to think step by step. On the last line, write the words "Rot-12 text:" followed by the encoded message:\nOriginal text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message and its corresponding version in rot-13:\nOriginal text: "Stay here!"\nRot-13 text: "Fgnl urer!"\n\nHere is another message. Encode this message in rot-13. Make sure to think step by step. On the last line, write the words "Rot-13 text:" followed by the encoded message:\nOriginal text: "%s"' 

                    elif prompt_type == "cot":
                        example12["task_instruction"] = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. For example, here is a message to be encoded:\nOriginal text: "Stay here!"\n\nTo encode this message, we shift each letter 12 positions forward:\n1. S -> E\n2. t -> f\n3. a -> m\n4. y -> k\n5.   ->  \n6. h -> t\n7. e -> q\n8. r -> d\n9. e -> q\n10. ! -> !\n\nTherefore, the rot-12 text is: "Efmk tqdq!"\n\nHere is another message. Encode the message one letter at a time. On the last line, write the words "Rot-12 text:" followed by the encoded message:\nOriginal text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message to be encoded:\nOriginal text: "Stay here!"\n\nTo encode this message, we shift each letter 13 positions forward:\n1. S -> F\n2. t -> g\n3. a -> n\n4. y -> l\n5.   ->  \n6. h -> u\n7. e -> r\n8. r -> e\n9. e -> r\n10. ! -> !\n\nTherefore, the rot-13 text is: "Fgnl urer!"\n\nHere is another message. Encode the message one letter at a time. On the last line, write the words "Rot-13 text:" followed by the encoded message:\nOriginal text: "%s"' 


                # Input
                if direction == "dec":
                    example12["input"] = encoded12
                    example13["input"] = encoded13
                else:
                    example12["input"] = sentence
                    example13["input"] = sentence

                # Combining the instruction and input (this is the string that should be given to the model)
                example12["instruction_plus_input"] = example12["task_instruction"] % example12["input"]
                example13["instruction_plus_input"] = example13["task_instruction"] % example13["input"]

                # The correct output
                if direction == "dec":
                    example12["correct_output"] = sentence
                    example13["correct_output"] = sentence
                else:
                    example12["correct_output"] = encoded12
                    example13["correct_output"] = encoded13


                jsl12.write(example12)
                jsl13.write(example13)
        

                count_encoded += 1
                if count_encoded == 100:
                    break


    





