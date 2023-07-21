
import jsonlines



for fi_name, fo_name in [("../examples/multiplication_number.txt", "../stimuli/multiplication_number.jsonl"), ("../examples/multiplication_word.txt", "../stimuli/multiplication_word.jsonl"), ("../examples/multiplication_alternatingcaps.txt", "../stimuli/multiplication_alternatingcaps.jsonl"), ("../examples/multiplication_allcaps.txt", "../stimuli/multiplication_allcaps.jsonl"),]:

    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        parts = line.strip().split("\t")
        answer = parts[0]
        question = parts[1]

        example = {}

        # Task
        example["task_name"] = "multiplication"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example["example_type"] = example_type


        sentence = line.strip()

        
        # Instruction
        if example_type == "number":
            example["task_instruction"] = 'Evaluate the mathematical expression in Question 2. For example, if you were asked Question 1, you would answer with Answer 1.\nQuestion 1: 83 times 44\nAnswer 1: 3652\n\nQuestion 2: %s\nAnswer 2:'
        elif example_type == "word":
            example["task_instruction"] = 'Evaluate the mathematical expression in Question 2. For example, if you were asked Question 1, you would answer with Answer 1.\nQuestion 1: eighty-three times forty-four\nAnswer 1: 3652\n\nQuestion 2: %s\nAnswer 2:'
        elif example_type == "allcaps":
            example["task_instruction"] = 'Evaluate the mathematical expression in Question 2. For example, if you were asked Question 1, you would answer with Answer 1.\nQuestion 1: EIGHTY-THREE times FORTY-FOUR\nAnswer 1: 3652\n\nQuestion 2: %s\nAnswer 2:'
        elif example_type == "alternatingcaps":
            example["task_instruction"] = 'Evaluate the mathematical expression in Question 2. For example, if you were asked Question 1, you would answer with Answer 1.\nQuestion 1: eIgHtY-tHrEe times fOrTy-FoUr\nAnswer 1: 3652\n\nQuestion 2: %s\nAnswer 2:'

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


    





