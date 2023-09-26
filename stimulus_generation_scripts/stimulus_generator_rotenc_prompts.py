
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

for prompt_type in ["step2", "cot2", "cot3"]:
    for direction in ["enc"]:
        for fi_name, fo_name in [("../examples/sentences_high_probability.txt", "../stimuli/rot2" + direction + prompt_type + "_highprob.jsonl")]: 
    
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
                if direction == "dec":
                    if prompt_type == "basic":
                        example2["task_instruction"] = 'Rot-2 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, here is a message written in rot-2 along with the original text that it was created from:\nRot-2 text: "Uvca jgtg!"\nOriginal text: "Stay here!"\n\nHere is another message in rot-2. Decode this message to produce the original text:\nRot-2 text: "%s"\nOriginal text:'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message written in rot-13 along with the original text that it was created from:\nRot-13 text: "Fgnl urer!"\nOriginal text: "Stay here!"\n\nHere is another message in rot-13. Decode this message to produce the original text:\nRot-13 text: "%s"\nOriginal text:'
                    elif prompt_type == "step":
                        example2["task_instruction"] = 'Rot-2 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, here is a message written in rot-2 along with the original text that it was created from:\nRot-2 text: "Uvca jgtg!"\nOriginal text: "Stay here!"\n\nHere is another message in rot-2. Decode the message to produce the original text. Make sure to think step by step. On the last line, write the words "Original text:" followed by the decoded message:\nRot-2 text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message written in rot-13 along with the original text that it was created from:\nRot-13 text: "Fgnl urer!"\nOriginal text: "Stay here!"\n\nHere is another message in rot-13. Decode the message to produce the original text. Make sure to think step by step. On the last line, write the words "Original text:" followed by the decoded message:\nRot-13 text: "%s"'
                    elif prompt_type == "cot":
                        example2["task_instruction"] = 'Rot-2 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, here is a message written in rot-2:\nRot-2 text: "Uvca jgtg!"\n\nTo decode this message, we shift each letter 2 positions backward:\n1. U -> S\n2. v -> t\n3. c -> a\n4. a -> y\n5.   ->  \n6. j -> h\n7. g -> e\n8. t -> r\n9. g -> e\n10. ! -> !\n\nTherefore, the original text is: "Stay here!"\n\nHere is another message in rot-2. Decode the message one letter at a time. On the last line, write the words "Original text:" followed by the decoded message:\nRot-2 text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message written in rot-13:\nRot-13 text: "Fgnl urer!"\n\nTo decode this message, we shift each letter 13 positions backward:\n1. F -> S\n2. g -> t\n3. n -> a\n4. l -> y\n5.   ->  \n6. u -> h\n7. r -> e\n8. e -> r\n9. r -> e\n10. ! -> !\n\nTherefore, the original text is: "Stay here!"\n\nHere is another message in rot-13. Decode the message one letter at a time. On the last line, write the words "Original text:" followed by the decoded message:\nRot-13 text: "%s"'
                
                elif direction == "enc":
                    if prompt_type == "step2":
                        example2["task_instruction"] = 'Rot-2 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, here is a message and its corresponding version in rot-2:\nOriginal text: "Stay here!"\nRot-2 text: "Uvca jgtg!"\n\nHere is another message. Encode this message in rot-2. Make sure to think step by step. On the last line, write the words "Rot-2 text:" followed by the encoded message:\nOriginal text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message and its corresponding version in rot-13:\nOriginal text: "Stay here!"\nRot-13 text: "Fgnl urer!"\n\nHere is another message. Encode this message in rot-13. On the last line, write the words "Rot-13 text:" followed by the encoded message:\nOriginal text: "%s"\nLet\'s think step by step.' 

                    elif prompt_type == "cot2":
                        example2["task_instruction"] = 'Rot-2 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, here is a message to be encoded:\nOriginal text: "Stay here!"\n\nTo encode this message, we shift each letter 2 positions forward:\n1. S -> U\n2. t -> v\n3. a -> c\n4. y -> a\n5.   ->  \n6. h -> j\n7. e -> g\n8. r -> t\n9. e -> g\n10. ! -> !\n\nTherefore, the rot-2 text is: "Uvca jgtg!"\n\nHere is another message. Encode the message one letter at a time. On the last line, write the words "Rot-2 text:" followed by the encoded message:\nOriginal text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message to be encoded:\nOriginal text: "Stay here!"\n\nTo encode this message, we shift each letter 13 positions forward:\n1. The first word in "Stay"\n * S -> F\n * t -> g\n * a -> n\n * y -> l\nSo "Stay" becomes "Fgnl"\n2. The second word is "here!"\n * h -> u\n * e -> r\n * r -> e\n * e -> r\n * ! -> !\nSo "here!" becomes "urer!"\n\nTherefore, the rot-13 text is: "Fgnl urer!"\n\nHere is another message. Encode the message word by word and letter by letter. On the last line, write the words "Rot-13 text:" followed by the encoded message:\nOriginal text: "%s"' 
                    elif prompt_type == "cot3":
                        example2["task_instruction"] = 'Rot-2 is a cipher in which each letter is shifted 2 positions forward in the alphabet. For example, here is a message to be encoded:\nOriginal text: "Stay here!"\n\nTo encode this message, we shift each letter 2 positions forward:\n1. S -> U\n2. t -> v\n3. a -> c\n4. y -> a\n5.   ->  \n6. h -> j\n7. e -> g\n8. r -> t\n9. e -> g\n10. ! -> !\n\nTherefore, the rot-2 text is: "Uvca jgtg!"\n\nHere is another message. Encode the message one letter at a time. On the last line, write the words "Rot-2 text:" followed by the encoded message:\nOriginal text: "%s"'
                        example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. For example, here is a message and an illustration of how to encode it in rot-13 by shifting the letters forward one position at a time:\nOriginal text: "Stay here!"\nShifted forward 1: "Tubz ifsf!"\nShifted forward 2: "Uvca jgtg!"\nShifted forward 3: "Vwdb khuh!"\nShifted forward 4: "Wxec livi!"\nShifted forward 5: "Xyfd mjwj!"\nShifted forward 6: "Yzge nkxk!"\nShifted forward 7: "Zahf olyl!"\nShifted forward 8: "Abig pmzm!"\nShifted forward 9: "Bcjh qnan!"\nShifted forward 10: "Cdki robo!"\nShifted forward 11: "Delj spcp!"\nShifted forward 12: "Efmk tqdq!"\nShifted forward 13: "Fgnl urer!"\n\nTherefore, the rot-13 text is: "Fgnl urer!"\n\nHere is another message. Encode this message in rot-13 by shifting each letter one position at a time. On the last line, write the words "Rot-13 text:" followed by the encoded message:\nOriginal text: "%s"\n'  


                # Input
                if direction == "dec":
                    example2["input"] = encoded2
                    example13["input"] = encoded13
                else:
                    example2["input"] = sentence
                    example13["input"] = sentence

                # Combining the instruction and input (this is the string that should be given to the model)
                example2["instruction_plus_input"] = example2["task_instruction"] % example2["input"]
                example13["instruction_plus_input"] = example13["task_instruction"] % example13["input"]

                # The correct output
                if direction == "dec":
                    example2["correct_output"] = sentence
                    example13["correct_output"] = sentence
                else:
                    example2["correct_output"] = encoded2
                    example13["correct_output"] = encoded13


                jsl2.write(example2)
                jsl13.write(example13)
        

                count_encoded += 1
                if count_encoded == 20:
                    break


    





