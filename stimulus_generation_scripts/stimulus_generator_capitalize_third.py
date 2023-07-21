
import jsonlines


for fi_name, fo_name in [("../examples/capitalize_third_common.txt", "../stimuli/capitalize_third_common.jsonl"), ("../examples/capitalize_third_rare.txt", "../stimuli/capitalize_third_rare.jsonl"), ]:  
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        example["task_name"] = "capitalize_third"

        # Condition
        example_type = fo_name.split("_")[-1].split(".")[0]
        example["example_type"] = example_type


        sentence = line.strip()
        words = sentence.split()

        answer = []
        for index, word in enumerate(words):
            if index % 3 == 0:
                answer.append(word.upper())
            else:
                answer.append(word.lower())

        # Instruction
        example["task_instruction"] = 'Put every third word of the following list in all caps, starting with the first word:  "%s"'


        # Input
        example["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = " ".join(answer)

        jsl.write(example)



    





