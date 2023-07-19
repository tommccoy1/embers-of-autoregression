
import jsonlines


for fi_name, fo_name in [("sentence_outputs/acronyms_first_word.txt", "stimuli/acronym1e_highprob.jsonl"), ("sentence_outputs/acronyms_first_random.txt", "stimuli/acronym1e_random.jsonl"), ("sentence_outputs/acronyms_first_adversarial.txt", "stimuli/acronym1e_adversarial.jsonl"),
        ("sentence_outputs/acronyms_second_word.txt", "stimuli/acronym2e_highprob.jsonl"), ("sentence_outputs/acronyms_second_random.txt", "stimuli/acronym2e_random.jsonl"), ("sentence_outputs/acronyms_second_adversarial.txt", "stimuli/acronym2e_adversarial.jsonl")]:
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        if "first" in fi_name:
            example["task_name"] = "acronym1e"
        else:
            example["task_name"] = "acronym2e"

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
            instruction = 'What sequence of letters is created when you combine the first letters of the words in the following sequence? "%s"'
        else:
            instruction = 'What sequence of letters is created when you combine the second letters of the words in the following sequence? "%s"'
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


    





