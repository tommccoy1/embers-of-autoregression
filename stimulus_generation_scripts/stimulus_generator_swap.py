
import jsonlines


for conditionlong, conditionshort in [("high_probability", "highprob"), ("medium_probability", "mediumprob"), ("low_probability", "lowprob")]:
    base_sentences = []
    next_sentences = []
    prev_sentences = []

    fi_base = open("../examples/swap_" + conditionlong + ".txt", "r")
    for line in fi_base:
        base_sentences.append(line.strip())

    fi_next = open("../examples/swapnext_" + conditionlong + ".txt", "r")
    for line in fi_next:
        next_sentences.append(line.strip())

    fi_prev = open("../examples/swapprev_" + conditionlong + ".txt", "r")
    for line in fi_prev:
        prev_sentences.append(line.strip())


    for input_list, output_list, fo_name, task in [(base_sentences, next_sentences, "../stimuli/swap_base_next_" + conditionshort + ".jsonl", "next"), (next_sentences, base_sentences, "../stimuli/swap_next_base_" + conditionshort + ".jsonl", "prev"), (base_sentences, prev_sentences, "../stimuli/swap_base_prev_" + conditionshort + ".jsonl", "prev"), (prev_sentences, base_sentences, "../stimuli/swap_prev_base_" + conditionshort + ".jsonl", "next")]:
    
        fo = open(fo_name, "w")
        jsl = jsonlines.Writer(fo)

        count_encoded = 0
        for inp, outp in zip(input_list, output_list):
            example = {}

            # Task
            example["task_name"] = "swap_" + task

            # Condition
            example_type = ("_".join(fo_name.split("_")[1:-1])).split(".")[0]
            example["example_type"] = example_type


            # Instruction
            if example_type == "base_next":
                example["task_instruction"] = 'Repeat the sentence listed as Input 2 below, but every time there is an article ("the", "a", or "an"), swap it with the following word. For example, if the input were Input 1, you should reply with Output 1:\nInput 1: "When we boarded the train, we saw a strange sight."\nOutput 1: "When we boarded train the, we saw strange a sight."\n\nInput 2: "%s"\nOutput 2:'
            elif example_type == "base_prev":
                example["task_instruction"] = 'Repeat the sentence listed as Input 2 below, but every time there is an article ("the", "a", or "an"), swap it with the previous word. For example, if the input were Input 1, you should reply with Output 1:\nInput 1: "When we boarded the train, we saw a strange sight."\nOutput 1: "When we the boarded train, we a saw strange sight."\n\nInput 2: "%s"\nOutput 2:'
            elif example_type == "next_base":
                example["task_instruction"] = 'Repeat the sentence listed as Input 2 below, but every time there is an article ("the", "a", or "an"), swap it with the previous word. For example, if the input were Input 1, you should reply with Output 1:\nInput 1: "When we boarded train the, we saw strange a sight."\nOutput 1: "When we boarded the train, we saw a strange sight."\n\nInput 2: "%s"\nOutput 2:'
            elif example_type == "prev_base":
                example["task_instruction"] = 'Repeat the sentence listed as Input 2 below, but every time there is an article ("the", "a", or "an"), swap it with the following word. For example, if the input were Input 1, you should reply with Output 1:\nInput 1: "When we the boarded train, we a saw strange sight."\nOutput 1: "When we boarded the train, we saw a strange sight."\n\nInput 2: "%s"\nOutput 2:'
            
        

            # Input
            example["input"] = inp

            # Combining the instruction and input (this is the string that should be given to the model)
            example["instruction_plus_input"] = example["task_instruction"] % example["input"]

            # The correct output
            example["correct_output"] = outp


            jsl.write(example)
        

            count_encoded += 1
            if count_encoded == 100:
                break


    





