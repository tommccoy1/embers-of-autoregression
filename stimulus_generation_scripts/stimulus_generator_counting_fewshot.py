
import jsonlines


for fi_name, fo_name in [("../examples/counting_words_common.txt", "../stimuli/counting_words_common_5shot.jsonl"), ("../examples/counting_words_common.txt", "../stimuli/counting_words_common_10shot.jsonl"),("../examples/counting_words_common.txt", "../stimuli/counting_words_common_100shot.jsonl")]:
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    in_context_examples = []
    if "5shot" in fo_name:
        example_file = open("../examples/counting_words_5shot.txt", "r")
    elif "10shot" in fo_name:
        example_file = open("../examples/counting_words_10shot.txt", "r") 
    else:
        example_file = open("../examples/counting_words_100shot.txt", "r")
        
    for line in example_file:
        in_context_examples.append(line.strip())
    example_file.close()


    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        example["task_name"] = "counting_words"

        instruction = 'Below are some lists of words. After each list, we have stated how many words are present in that list. For the final list, we have not specified the word count. Respond by saying how many words are in that list.\n\n'
        for in_context_example in in_context_examples:
            instruction += 'List: "' + in_context_example + '"'
            instruction += '\n'
            in_context_length = len(in_context_example.split())
            instruction += 'Number of words: ' + str(in_context_length)
            instruction += '\n\n'

        sentence = line.strip()
        length = len(sentence.split())


        instruction += 'List: "%s"'
        instruction += '\n'
        instruction += 'Number of words: '
 
           

        # Instruction
        example["task_instruction"] = instruction


        # Input
        example["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = str(length)

        jsl.write(example)



    





