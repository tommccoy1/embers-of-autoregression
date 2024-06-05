
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



instruction_12_dec = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. Below is a message in rot-12. Provide the original text that this encoded message was created from.\n'
instruction_12_dec += 'Rot-12 text: "%s"\n'
instruction_12_dec += 'Original text:'

instruction_13_dec = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. Below is a message in rot-13. Provide the original text that this encoded message was created from.\n'
instruction_13_dec += 'Rot-13 text: "%s"\n'
instruction_13_dec += 'Original text:'


instruction_12_enc = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. Encode the following message into rot-12.\n'
instruction_12_enc += 'Original text: "%s"\n'
instruction_12_enc += 'Rot-12 text:'

instruction_13_enc = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. Encode the following message into rot-13.\n'
instruction_13_enc += 'Original text: "%s"\n'
instruction_13_enc += 'Rot-13 text:'



for shift in ["12", "13"]:
    for direction in ["enc", "dec"]:
        for prob in ["highprob", "mediumprob", "lowprob"]:
            for count in ["10", "100"]:

                fi = None
                if prob == "highprob":
                    fi = open("../examples/sentences_high_probability_train.txt", "r")
                elif prob == "mediumprob":
                    fi = open("../examples/sentences_medium_probability_train.txt", "r") 
                elif prob == "lowprob":
                    fi = open("../examples/sentences_low_probability_train.txt", "r")

                fo = open("../stimuli/rot" + shift + direction + "_" + prob + "_" + count + "shot_finetune.jsonl", "w")
                jsl = jsonlines.Writer(fo)
    
                for index, line in enumerate(fi):
                    if index >= int(count):
                        break

                    example = line.strip()

                    example_dict = {}
                    user_dict = {}
                    assistant_dict = {}

                    if shift == "12":
                        encoded_example = rot12_encode(example)
                    elif shift == "13":
                        encoded_example = rot13_encode(example)
                    else:
                        encoded_example = None


                    if shift == "12" and direction == "enc":
                        prompt = instruction_12_enc
                    elif shift == "12" and direction == "dec":
                        prompt = instruction_12_dec
                    elif shift == "13" and direction == "enc":
                        prompt = instruction_13_enc
                    elif shift == "13" and direction == "dec":
                        prompt = instruction_13_dec


                    user_dict["role"] = "user"
                    assistant_dict["role"] = "assistant"
                    if direction == "dec":
                        user_dict["content"] = prompt % encoded_example
                        assistant_dict["content"] = example
                    else:
                        user_dict["content"] = prompt % example
                        assistant_dict["content"] = encoded_example


                    message_list = [user_dict, assistant_dict]

                    example_dict["messages"] = message_list

                    jsl.write(example_dict)
                fi.close()


