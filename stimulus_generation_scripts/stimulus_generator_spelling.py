
import jsonlines


fi_name = "../examples/spelling.txt"
fo_name = "../stimuli/spelling_all.jsonl"

fi = open(fi_name, "r")
fo = open(fo_name, "w")
jsl = jsonlines.Writer(fo)

print(fi_name, fo_name)

    

count_encoded = 0
for line in fi:
    example = {}

    example["task_name"] = "spelling"

    # Condition
    example["example_type"] = "spelling"


    word = line.strip()
    answer = " ".join([word[index] for index in range(len(word))])
                

    instruction = 'Spell the word "%s" by listing its letters, in order, separated by spaces.'
    example["task_instruction"] = instruction
        
    # Input
    example["input"] = word

    # Combining the instruction and input (this is the string that should be given to the model)
    example["instruction_plus_input"] = example["task_instruction"] % example["input"]

    # The correct output
    example["correct_output"] = answer

    jsl.write(example)
        
    count_encoded += 1
    if count_encoded == 1000:
        break







