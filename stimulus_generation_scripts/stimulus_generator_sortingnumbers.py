
import jsonlines


for fi_name, fo_name in [("../examples/sorting_numbers.txt", "../stimuli/sorting_ascending.jsonl"), ("../examples/sorting_numbers.txt", "../stimuli/sorting_descending.jsonl")]: 
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        if "ascending" in fo_name:
            example["task_name"] = "sort_ascending"
        elif "descending" in fo_name:
            example["task_name"] = "sort_descending"

        # Condition
        example_type = fo_name.split("_")[-1].split(".")[0]
        example["example_type"] = example_type


        if example["task_name"] == "sort_ascending":
            sentence = line.strip()
            words = sentence.split(", ")
            words = [int(x) for x in words]
            answer = sorted(words)
            answer = [str(x) for x in answer]

            # Instruction
            example["task_instruction"] = 'Sort the following list of numbers in ascending order: "%s"'
        else:
            sentence = line.strip()
            words = sentence.split(", ")
            words = [int(x) for x in words]
            answer = sorted(words)[::-1]
            answer = [str(x) for x in answer]

            # Instruction
            example["task_instruction"] = 'Sort the following list of numbers in descending order: "%s"'


        # Input
        example["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = ", ".join(answer)

        jsl.write(example)



    





