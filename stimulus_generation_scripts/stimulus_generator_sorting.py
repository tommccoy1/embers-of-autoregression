
import jsonlines


for fi_name, fo_name in [("../examples/sorting_words.txt", "../stimuli/sorting_fwd.jsonl"), ("../examples/sorting_words.txt", "../stimuli/sorting_rev.jsonl")]: 
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        if "fwd" in fo_name:
            example["task_name"] = "sort_alphabetical"
        elif "rev" in fo_name:
            example["task_name"] = "sort_reversealphabetical"

        # Condition
        example_type = fo_name.split("_")[-1].split(".")[0]
        example["example_type"] = example_type


        if example["task_name"] == "sort_alphabetical":
            sentence = line.strip()
            words = sentence.split(", ")
            answer = sorted(words)

            # Instruction
            example["task_instruction"] = 'Sort the following list of words in alphabetical order: "%s"'
        else:
            sentence = line.strip()
            words = sentence.split(", ")
            answer = sorted(words)[::-1]

            # Instruction
            example["task_instruction"] = 'Sort the following list of words in reverse alphabetical order: "%s"'


        # Input
        example["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = ", ".join(answer)

        jsl.write(example)



    





