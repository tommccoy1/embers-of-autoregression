
import jsonlines


fi_examples = open("../examples/sorting_words_examples.txt", "r")
all_in_context_examples = []
for line in fi_examples:
    all_in_context_examples.append(line.strip())


for fi_name, fo_name in [("../examples/sorting_words.txt", "../stimuli/sorting_fwd_0shot.jsonl"), ("../examples/sorting_words.txt", "../stimuli/sorting_rev_0shot.jsonl"),
            ("../examples/sorting_words.txt", "../stimuli/sorting_fwd_5shot.jsonl"), ("../examples/sorting_words.txt", "../stimuli/sorting_rev_5shot.jsonl"),
            ("../examples/sorting_words.txt", "../stimuli/sorting_fwd_10shot.jsonl"), ("../examples/sorting_words.txt", "../stimuli/sorting_rev_10shot.jsonl"),
        ]: 
    
    n_examples = None
    if "_0shot" in fo_name:
        n_examples = 0
    elif "_5shot" in fo_name:
        n_examples = 5
    elif "_10shot" in fo_name:
        n_examples = 10
    in_context_examples = all_in_context_examples[:n_examples]


    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        if "fwd" in fo_name:
            example["task_name"] = "sort_alphabetical"
        elif "rev" in fo_name:
            example["task_name"] = "sort_reversealphabetical"

        # Condition
        example_type = fo_name.split("_")[-1].split(".")[0]
        example["example_type"] = example_type


        if n_examples == 0:
            if example["task_name"] == "sort_alphabetical":
                sentence = line.strip()
                words = sentence.split(", ")
                answer = sorted(words)

                # Instruction
                example["task_instruction"] = 'Below is a list of words. Sort the words into alphabetical order.\nOriginal list: "%s"\nSorted list:'
            else:
                sentence = line.strip()
                words = sentence.split(", ")
                answer = sorted(words)[::-1]
    
                # Instruction
                example["task_instruction"] = 'Below is a list of words. Sort the words into reverse alphabetical order.\nOriginal list: "%s"\nSorted list:'
        
        else:
            if example["task_name"] == "sort_alphabetical":
                sentence = line.strip()
                words = sentence.split(", ")
                answer = sorted(words)

                # Instruction
                example["task_instruction"] = 'Below are several list of words, each of which is followed by the same list but sorted into alphabetical order. The sorted version of the last list has not been provided. Sort this list.\n\n'
                for in_context_example in in_context_examples:
                    example["task_instruction"] += 'Original list: "' + in_context_example + '"\n'
                    example["task_instruction"] += 'Sorted list: "' + ", ".join(sorted(in_context_example.split(", "))) + '"\n\n'
                example["task_instruction"] += 'Original list: "%s"\n'
                example["task_instruction"] += 'Sorted list:'


            else:
                sentence = line.strip()
                words = sentence.split(", ")
                answer = sorted(words)[::-1]
    
                # Instruction
                example["task_instruction"] = 'Below are several list of words, each of which is followed by the same list but sorted into reverse alphabetical order. The sorted version of the last list has not been provided. Sort this list.\n\n'
                for in_context_example in in_context_examples:
                    example["task_instruction"] += 'Original list: "' + in_context_example + '"\n'
                    example["task_instruction"] += 'Sorted list: "' + ", ".join(sorted(in_context_example.split(", "))[::-1]) + '"\n\n'
                example["task_instruction"] += 'Original list: "%s"\n'
                example["task_instruction"] += 'Sorted list:'



        # Input
        example["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = ", ".join(answer)

        jsl.write(example)



    





