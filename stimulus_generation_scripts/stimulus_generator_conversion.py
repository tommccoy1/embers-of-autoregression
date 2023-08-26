
import jsonlines



for fi_name, fo_name in [("../examples/conversion_actual.txt", "../stimuli/conversion_actual.jsonl"), ("../examples/conversion_actual.txt", "../stimuli/conversion_actualprimed.jsonl"), ("../examples/conversion_actual.txt", "../stimuli/conversion_actualprimedcontrol.jsonl"),("../examples/conversion_fake.txt", "../stimuli/conversion_fake.jsonl"), ("../examples/conversion_actualinverse.txt", "../stimuli/conversion_actualinverse.jsonl"), ("../examples/conversion_fakeinverse.txt", "../stimuli/conversion_fakeinverse.jsonl"), ]:

    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        parts = line.strip().split("\t")
        question = parts[0]
        answer = parts[1]

        example = {}

        # Task
        example["task_name"] = "conversion"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example["example_type"] = example_type


        sentence = line.strip()

        
        # Instruction
        if "actualprimedcontrol" in fo_name:
            example["task_instruction"] = 'In this task, you must return an answer based on an input.\n\nBelow is a number. Multiply it by 9/5 and then add 32. Your answer should be a single number:\nInput: %s\nAnswer:'
        elif "actualprimed" in fo_name:
            example["task_instruction"] = 'In this task, you must convert a number from Celsius to Fahrenheit.\n\nBelow is a number. Multiply it by 9/5 and then add 32. Your answer should be a single number:\nInput: %s\nAnswer:'
        elif "actualinverse" in fi_name:
            example["task_instruction"] = 'Below is a number. Multiply it by 9/5 and then add 32. Your answer should be a single number rounded to the nearest integer:\nInput: %s\nAnswer:'
        elif "fakeinverse" in fi_name: 
            example["task_instruction"] = 'Below is a number. Multiply it by 7/5 and then add 31. Your answer should be a single number rounded to the nearest integer:\nInput: %s\nAnswer:'
        elif "actual" in fi_name:
            example["task_instruction"] = 'Below is a number. Multiply it by 9/5 and then add 32. Your answer should be a single number:\nInput: %s\nAnswer:'
        elif "fake" in fi_name:
            example["task_instruction"] = 'Below is a number. Multiply it by 7/5 and then add 31. Your answer should be a single number:\nInput: %s\nAnswer:'

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


    





