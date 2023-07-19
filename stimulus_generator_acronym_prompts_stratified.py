
import jsonlines


task_list = []

for first in ["common", "medium", "rare", "random"]:
    for second in ["common", "medium", "rare", "random"]:
        for fi_name, fo_name in [("sentence_outputs/acronyms_stratified_first_" + first + "_" + second + ".txt", "stimuli/acronym1_strat_" + first + "_" + second + ".jsonl"),]:
                #("sentence_outputs/acronyms_stratified_second_" + first + "_" + second + ".txt", "stimuli/acronym2_strat_" + first + "_" + second + ".jsonl")]:
    
            print(fi_name, fo_name)

            for prompt_style, prompt_text in [("plain", 'What sequence of letters is created when you combine the first letters of the words in the following sequence? "%s"'),
                    ("capital_first", 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in uppercase letters, with no spaces or punctuation.'),
                    ("capitalperiod_first", 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in uppercase letters, with a period after each letter.'),
                ]:

    
                fo_name_to_use = fo_name.replace("acronym", "prompt_" + prompt_style + "_acronym")
                task = "_".join(fo_name_to_use.split("_"))[8:].replace(".jsonl", "")
                if "_".join(task.split("_")[:-1]) not in task_list:
                    task_list.append("_".join(task.split("_")[:-1]))
                fi = open(fi_name, "r")
                fo = open(fo_name_to_use, "w")
                jsl = jsonlines.Writer(fo)

                count_encoded = 0
                for line in fi:
                    example = {}

                    # Task
                    if "first" in fi_name:
                        example["task_name"] = "acronym1"
                    else:
                        example["task_name"] = "acronym2"

                    # Condition
                    example_type = fo_name.split("_")[1].split(".")[0]
                    example["example_type"] = example_type


                    parts = line.strip().split("\t")
                    answer = parts[0]
                    sentence = parts[1]
        
                    # Instruction
                    if "first" in fi_name:
                        instruction = prompt_text
                    else:
                        instruction = prompt_text.replace("first", "second")
                    example["task_instruction"] = instruction

                    # Input
                    example["input"] = sentence

                    # Combining the instruction and input (this is the string that should be given to the model)
                    example["instruction_plus_input"] = example["task_instruction"] % example["input"]

                    # The correct output
                    example["correct_output"] = answer

                    jsl.write(example)
        
                    count_encoded += 1
                    if count_encoded == 100:
                        break


print(",".join(task_list))





