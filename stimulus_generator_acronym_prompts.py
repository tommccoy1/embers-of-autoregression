
import jsonlines


task_list = []
for fi_name, fo_name in [("sentence_outputs/acronyms_first_word.txt", "stimuli/acronym1_highprob.jsonl"), ("sentence_outputs/acronyms_first_random.txt", "stimuli/acronym1_random.jsonl"), ("sentence_outputs/acronyms_frequent_first_word.txt", "stimuli/acronym1_highprobfreq.jsonl"), 
        ("sentence_outputs/acronyms_second_word.txt", "stimuli/acronym2_highprob.jsonl"), ("sentence_outputs/acronyms_second_random.txt", "stimuli/acronym2_random.jsonl"), ("sentence_outputs/acronyms_frequent_second_word.txt", "stimuli/acronym2_highprobfreq.jsonl")]:
    print(fi_name, fo_name)

    for prompt_style, prompt_text in [("plain", 'What sequence of letters is created when you combine the first letters of the words in the following sequence? "%s"'),
            ("plainabbrev", 'What abbreviation is created when you combine the first letters of the words in the following sequence? "%s"'),
            ("capital_last", 'What sequence of letters is created when you combine the first letters of the words in the sequence below? Write your answer in uppercase letters, with no spaces or punctuation.\n\nThe input sequence is: "%s"'),
            ("capital_first", 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in uppercase letters, with no spaces or punctuation.'),
            ("lower_last", 'What sequence of letters is created when you combine the first letters of the words in the sequence below? Write your answer in lowercase letters, with no spaces or punctuation.\n\nThe input sequence is: "%s"'),
            ("lower_first", 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in lowercase letters, with no spaces or punctuation.'),

            ("capitalcomma_last", 'What sequence of letters is created when you combine the first letters of the words in the sequence below? Write your answer in uppercase letters, with a comma after each letter.\n\nThe input sequence is: "%s"'),
            ("capitalcomma_first", 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in uppercase letters, with a comma after each letter.'),
            ("capitalspace_last", 'What sequence of letters is created when you combine the first letters of the words in the sequence below? Write your answer in uppercase letters, with a space after each letter.\n\nThe input sequence is: "%s"'),
            ("capitalspace_first", 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in uppercase letters, with a space after each letter.'), 

            ("lowercomma_last", 'What sequence of letters is created when you combine the first letters of the words in the sequence below? Write your answer in lowercase letters, with a comma after each letter.\n\nThe input sequence is: "%s"'),
            ("lowercomma_first", 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in lowercase letters, with a comma after each letter.'),
            ("lowerspace_last", 'What sequence of letters is created when you combine the first letters of the words in the sequence below? Write your answer in lowercase letters, with a space after each letter.\n\nThe input sequence is: "%s"'),
            ("lowerspace_first", 'What sequence of letters is created when you combine the first letters of the words in the sequence "%s"? Write your answer in lowercase letters, with a space after each letter.'),
            ]:

    
        fo_name_to_use = fo_name.replace("acronym", "prompt_" + prompt_style + "_acronym")
        task = "_".join(fo_name_to_use.split("_")[:-1])[8:]
        if task not in task_list:
            task_list.append(task)
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
        
            # To balance:
            # - clarity to human
            # - not too long
            # - don't bias toward "it must be the first letter" (using "acronym" definitely does this, "abbreviation" might also)
            # - don't bias toward it being a sensible word ("what does it spell?")
            #
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





