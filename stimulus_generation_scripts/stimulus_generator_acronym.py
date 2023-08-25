
import jsonlines


task_list = []

for first in range(1,6):
    for second in range(1,6):
        if first == 1 or second == 1:

            for fi_name, fo_name in [("../examples/acronym1_" + str(first) + str(second) + ".txt", "../stimuli/acronym1_" + str(first) + str(second) + ".jsonl"), ("../examples/acronym2_" + str(first) + str(second) + ".txt", "../stimuli/acronym2_" + str(first) + str(second) + ".jsonl")]:

                print(fi_name, fo_name)

    
                task = str(first) + str(second) 
                if task not in task_list: 
                    task_list.append(task)
                fi = open(fi_name, "r")
                fo = open(fo_name, "w")
                jsl = jsonlines.Writer(fo)

                count_encoded = 0
                for line in fi:
                    example = {}

                    # Task
                    if "acronym1" in fi_name:
                        example["task_name"] = "acronym1"
                    elif "acronym2" in fi_name:
                        example["task_name"] = "acronym2"

                    # Condition
                    example_type = fo_name.split("_")[1].split(".")[0]
                    example["example_type"] = example_type


                    parts = line.strip().split("\t")
                    answer = parts[0]
                    sentence = parts[1]
                

                    prompt_text = 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in capital letters, with no spaces or punctuation.'
        
                    # Instruction
                    if "acronym1" in fi_name:
                        instruction = prompt_text
                    elif "acronym2" in fi_name:
                        instruction = prompt_text.replace("first", "second")
                    example["task_instruction"] = instruction

                    # Input
                    example["input"] = sentence

                    # Combining the instruction and input (this is the string that should be given to the model)
                    example["instruction_plus_input"] = example["task_instruction"] % example["input"]

                    # The correct output
                    example["correct_output"] = answer.upper()

                    jsl.write(example)
        
                    count_encoded += 1
                    if count_encoded == 1000:
                        break


print(",".join(task_list))





