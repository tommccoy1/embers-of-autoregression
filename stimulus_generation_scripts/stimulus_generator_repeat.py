
import jsonlines



for fi_name, fo_name in [("../examples/sentences_high_probability.txt", "../stimuli/repeat_highprob.jsonl"), ("../examples/sentences_low_probability.txt", "../stimuli/repeat_lowprob.jsonl"), ("../examples/sentences_adversarial.txt", "../stimuli/repeat_adversarial.jsonl"), ("../examples/sentences_random.txt", "../stimuli/repeat_random.jsonl")]:
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        example["task_name"] = "repeat"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example["example_type"] = example_type


        sentence = line.strip()

        
        # Instruction
        example["task_instruction"] = 'Repeat back the following text, unchanged: "%s"'

        # Input
        example["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = sentence


        jsl.write(example)
        

        count_encoded += 1
        if count_encoded == 100:
            break


    





