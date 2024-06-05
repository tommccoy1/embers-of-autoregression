
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


for fi_name, fo_name in [("../examples/shift_fewshot_highprob.txt", "../stimuli/rot12dec_highprob_word_5shot.jsonl"), ("../examples/shift_fewshot_medprob.txt", "../stimuli/rot12dec_mediumprob_word_5shot.jsonl"), ("../examples/shift_fewshot_lowprob.txt", "../stimuli/rot12dec_lowprob_word_5shot.jsonl"),
            ("../examples/shift_fewshot_highprob.txt", "../stimuli/rot12dec_highprob_word_10shot.jsonl"), ("../examples/shift_fewshot_medprob.txt", "../stimuli/rot12dec_mediumprob_word_10shot.jsonl"), ("../examples/shift_fewshot_lowprob.txt", "../stimuli/rot12dec_lowprob_word_10shot.jsonl"),
            ("../examples/shift_fewshot_highprob.txt", "../stimuli/rot12dec_highprob_word_0shot.jsonl"), ("../examples/shift_fewshot_medprob.txt", "../stimuli/rot12dec_mediumprob_word_0shot.jsonl"), ("../examples/shift_fewshot_lowprob.txt", "../stimuli/rot12dec_lowprob_word_0shot.jsonl"),
        ]:
   
    example_count = 0
    if "_5shot" in fo_name:
        example_count = 5
    elif "_10shot" in fo_name:
        example_count = 10
    elif "_0shot" in fo_name:
        example_count = 0

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


        parts = line.strip().split("\t")
        sentence = parts[0]
        in_context_examples = parts[1].split()[:example_count]

        encoded12 = rot12_encode(sentence)
        encoded13 = rot13_encode(sentence)

        # Instruction
        if example_count == 0:
            example12["task_instruction"] = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. Below is a message in rot-12. Provide the original text that this encoded message was created from.\n'
            example12["task_instruction"] += 'Rot-12 text: "%s"\n'
            example12["task_instruction"] += 'Original text:'

            example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. Below is a message in rot-13. Provide the original text that this encoded message was created from.\n'
            example13["task_instruction"] += 'Rot-13 text: "%s"\n'
            example13["task_instruction"] += 'Original text:'

        else:
            example12["task_instruction"] = 'Rot-12 is a cipher in which each letter is shifted 12 positions forward in the alphabet. Below are some messages in rot-12 along with the original text that they were created from. The last example is missing its original text; provide the original text for that example.\n\n'
            for in_context_example in in_context_examples:
                example12["task_instruction"] += 'Rot-12 text: "' + rot12_encode(in_context_example) + '"\n'
                example12["task_instruction"] += 'Original text: "' + in_context_example + '"\n\n'
            example12["task_instruction"] += 'Rot-12 text: "%s"\n'
            example12["task_instruction"] += 'Original text:'
        
            example13["task_instruction"] = 'Rot-13 is a cipher in which each letter is shifted 13 positions forward in the alphabet. Below are some messages in rot-13 along with the original text that they were created from. The last example is missing its original text; provide the original text for that example.\n\n'
            for in_context_example in in_context_examples:
                example13["task_instruction"] += 'Rot-13 text: "' + rot13_encode(in_context_example) + '"\n'
                example13["task_instruction"] += 'Original text: "' + in_context_example + '"\n\n'
            example13["task_instruction"] += 'Rot-13 text: "%s"\n'
            example13["task_instruction"] += 'Original text:'
    

        # Input
        example12["input"] = encoded12
        example13["input"] = encoded13

        # Combining the instruction and input (this is the string that should be given to the model)
        example12["instruction_plus_input"] = example12["task_instruction"] % example12["input"]
        example13["instruction_plus_input"] = example13["task_instruction"] % example13["input"]

        # The correct output
        example12["correct_output"] = sentence
        example13["correct_output"] = sentence


        jsl12.write(example12)
        jsl13.write(example13)
        

        count_encoded += 1
        if count_encoded == 100:
            break


    





