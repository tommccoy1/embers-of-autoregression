
import jsonlines


for fi_name, fo_name in [("../examples/counting_words_common.txt", "../stimuli/counting_words_common.jsonl"), ("../examples/counting_words_rare.txt", "../stimuli/counting_words_rare.jsonl"), ("../examples/counting_chars_common.txt", "../stimuli/counting_chars_common.jsonl"), ("../examples/counting_chars_rare.txt", "../stimuli/counting_chars_rare.jsonl"),]:
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        if "words" in fi_name:
            example["task_name"] = "counting_words"
        elif "chars" in fi_name:
            example["task_name"] = "counting_chars"

        # Condition
        example_type = fo_name.split("_")[-1].split(".")[0]
        example["example_type"] = example_type


        if example["task_name"] == "counting_words":
            sentence = line.strip()
            length = len(sentence.split())

            # Instruction
            example["task_instruction"] = 'How many words are in the following list? "%s"'
        elif example["task_name"] == "counting_chars":
            if "rare" in fi_name:
                parts = line.strip().split("\t")
                emoji_name = parts[0]
                sentence = parts[1]
                length = len(sentence)

                example["task_instruction"] = 'How many ' + emoji_name + ' emojis are in the following list? "%s"'
            else:
                sentence = line.strip()
                length = len(sentence)
                example["task_instruction"] = 'How many letters are in the following list? "%s"'


        # Input
        example["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = str(length)

        jsl.write(example)



    





