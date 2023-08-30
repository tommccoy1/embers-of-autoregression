
import jsonlines



for fi_name, fo_name in [("../examples/birthdays_1.txt", "../stimuli/birthdays_1.jsonl"), ("../examples/birthdays_2.txt", "../stimuli/birthdays_2.jsonl"), ("../examples/birthdays_3.txt", "../stimuli/birthdays_3.jsonl"), ("../examples/birthdays_4.txt", "../stimuli/birthdays_4.jsonl")]:

    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        parts = line.strip().split("\t")
        answer = parts[1]
        question = parts[0]

        example = {}

        # Task
        example["task_name"] = "birthday"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example["example_type"] = example_type


        sentence = line.strip()

        
        # Instruction
        example["task_instruction"] = 'On what date was %s born? You should format your answer as "Month Day, Year"; e.g., "July 19, 1743."'

        # Input
        example["input"] = question

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = answer


        jsl.write(example)
        

        count_encoded += 1
        if count_encoded == 100:
            break


    





