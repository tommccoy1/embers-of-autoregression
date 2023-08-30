
import jsonlines

# Function to encode text with the keyboard code
row1 = "qwertyuiopq"
row2 = "asdfghjkla"
row3 = "zxcvbnmz"

encoding_dict = {}
for row in [row1, row2, row3]:
    prev = None
    for char in row:
        if prev is not None:
            encoding_dict[prev] = char
            encoding_dict[prev.upper()] = char.upper()
        prev = char

def keyboard_encode(sequence):
    new_sequence = []
    for char in sequence:
        if char in encoding_dict:
            new_sequence.append(encoding_dict[char])
        else:
            new_sequence.append(char)

    return "".join(new_sequence)


print(keyboard_encode("abcdefghijklmnopqrstuvwxyz"))
print(keyboard_encode("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

for fi_name, fo_name in [("../examples/sentences_high_probability.txt", "../stimuli/keyboard_highprob.jsonl")]: 
   
    for prompt_type in ["keyboardcot", "keyboardcotreference", "keyboardcotdetailed"]:
        fi = open(fi_name, "r")
        fo = open(fo_name.replace("keyboard", prompt_type), "w")
        jsl = jsonlines.Writer(fo)

        count_encoded = 0
        for line in fi:
            example = {}

            # Task
            example["task_name"] = prompt_type

            # Condition
            example_type = fo_name.split("_")[1].split(".")[0]
            example["example_type"] = example_type


            sentence = line.strip()
            encoded = keyboard_encode(sentence)

            # Instruction
            if prompt_type == "keyboardcot":
                example["task_instruction"] = 'The keyboard cipher is a cipher where each letter is replaced with the letter to the right of it on a QWERTY keyboard. If the letter does not have a letter to its right, then you should wrap around to the start of the row; e.g., "p" maps to "q". For example, here is a message to be encoded:\nOriginal message: "Hello world!"\n\nTo encode this message, we replace each letter with the one to the right of it on a QWERTY keyboard:\n1. The first word is "Hello"\n * H -> J\n * e -> r\n * l -> a\n * l -> a\n * o -> p\n So "Hello" becomes "Jraap"\n2. The second word is "world!"\n * w -> e\n * o -> p\n * r -> t\n * l -> a\n * d -> f\n * ! -> !\n So "world!" becomes "eptaf!"\n\nTherefore, the message in the keyboard cipher is: "Jraap eptaf!"\n\nHere is another message. Encode the message in the keyboard cipher, word by word and letter by letter. On the last line, write the words "Keyboard cipher:" followed by the encoded message:\nOriginal message: "%s"'
            elif prompt_type == "keyboardcotreference":
                example["task_instruction"] = 'The keyboard cipher is a cipher where each letter is replaced with the letter to the right of it on a QWERTY keyboard. If the letter does not have a letter to its right, then you should wrap around to the start of the row; e.g., "p" maps to "q". For reference, here are the three rows of a QWERTY keyboard:\nq w e r t y u i o p\na s d f g h j k l\nz x c v b n m\n\nFor example, here is a message to be encoded:\nOriginal message: "Hello world!"\n\nTo encode this message, we replace each letter with the one to the right of it on a QWERTY keyboard:\n1. The first word is "Hello"\n * H -> J\n * e -> r\n * l -> a\n * l -> a\n * o -> p\n So "Hello" becomes "Jraap"\n2. The second word is "world!"\n * w -> e\n * o -> p\n * r -> t\n * l -> a\n * d -> f\n * ! -> !\n So "world!" becomes "eptaf!"\n\nTherefore, the message in the keyboard cipher is: "Jraap eptaf!"\n\nHere is another message. Encode the message in the keyboard cipher, word by word and letter by letter. On the last line, write the words "Keyboard cipher:" followed by the encoded message:\nOriginal message: "%s"'
            elif prompt_type == "keyboardcotdetailed":
                example["task_instruction"] = 'The keyboard cipher is a cipher where each letter is replaced with the letter to the right of it on a QWERTY keyboard. If the letter does not have a letter to its right, then you should wrap around to the start of the row; e.g., "p" maps to "q". For reference, here are the correct replacements for all letters:\na -> s\nb -> n\nc -> v\nd -> f\ne -> r\nf -> g\ng -> h\nh -> j\ni -> o\nj -> k\nk -> l\nl -> a\nm -> z\nn -> m\no -> p\np -> q\nq -> w\nr -> t\ns -> d\nt -> y\nu -> i\nv -> b\nw -> e\nx -> c\ny -> u\nz -> x\n\nFor example, here is a message to be encoded:\nOriginal message: "Hello world!"\n\nTo encode this message, we replace each letter with the one to the right of it on a QWERTY keyboard:\n1. The first word is "Hello"\n * H -> J\n * e -> r\n * l -> a\n * l -> a\n * o -> p\n So "Hello" becomes "Jraap"\n2. The second word is "world!"\n * w -> e\n * o -> p\n * r -> t\n * l -> a\n * d -> f\n * ! -> !\n So "world!" becomes "eptaf!"\n\nTherefore, the message in the keyboard cipher is: "Jraap eptaf!"\n\nHere is another message. Encode the message in the keyboard cipher, word by word and letter by letter. On the last line, write the words "Keyboard cipher:" followed by the encoded message:\nOriginal message: "%s"'


            # Input
            example["input"] = sentence

            # Combining the instruction and input (this is the string that should be given to the model)
            example["instruction_plus_input"] = example["task_instruction"] % example["input"]

            # The correct output
            example["correct_output"] = encoded

            jsl.write(example)

            count_encoded += 1
            if count_encoded == 100:
                break


    





