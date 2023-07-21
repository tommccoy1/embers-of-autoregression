
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

for fi_name, fo_name in [("../examples/sentences_high_probability.txt", "../stimuli/keyboard_highprob.jsonl"), ("../examples/sentences_low_probability.txt", "../stimuli/keyboard_lowprob.jsonl"), ("../examples/sentences_adversarial.txt", "../stimuli/keyboard_adversarial.jsonl"), ("../examples/sentences_random.txt", "../stimuli/keyboard_random.jsonl")]:
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        example["task_name"] = "keyboard"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example["example_type"] = example_type


        sentence = line.strip()
        encoded = keyboard_encode(sentence)

        
        # Instruction
        example["task_instruction"] = 'The keyboard cipher is a cipher where each letter is replaced with the letter to the right of it on a QWERTY keyboard. If the letter does not have a letter to its right, then you should wrap around to the start of the row; e.g., "p" maps to "q".Here is an example of a message written in the keyboard cipher:\nOriginal message: "Hi there!"\nKeyboard cipher: "Jo yjrtr!"\n\nEncode the following message in the keyboard cipher:\nOriginal message: "%s"\nKeyboard cipher:'


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


    





