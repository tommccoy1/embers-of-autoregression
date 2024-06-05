
import jsonlines


examples_high = []
examples_medium = []
examples_low = []

fi_high = open("../examples/sentences_high_probability_train.txt", "r")
fi_medium = open("../examples/sentences_medium_probability_train.txt", "r")
fi_low = open("../examples/sentences_low_probability_train.txt", "r")

for line in fi_high:
    examples_high.append(line.strip())
for line in fi_medium:
    examples_medium.append(line.strip())
for line in fi_low:
    examples_low.append(line.strip())



for fi_name, fo_name in [("../examples/sentences_high_probability_test.txt", "../stimuli/revenc_highprob_5shot.jsonl"), ("../examples/sentences_medium_probability_test.txt", "../stimuli/revenc_mediumprob_5shot.jsonl"), ("../examples/sentences_low_probability_test.txt", "../stimuli/revenc_lowprob_5shot.jsonl"),
            ("../examples/sentences_high_probability_test.txt", "../stimuli/revenc_highprob_10shot.jsonl"), ("../examples/sentences_medium_probability_test.txt", "../stimuli/revenc_mediumprob_10shot.jsonl"), ("../examples/sentences_low_probability_test.txt", "../stimuli/revenc_lowprob_10shot.jsonl"),
            ("../examples/sentences_high_probability_test.txt", "../stimuli/revenc_highprob_100shot.jsonl"), ("../examples/sentences_medium_probability_test.txt", "../stimuli/revenc_mediumprob_100shot.jsonl"), ("../examples/sentences_low_probability_test.txt", "../stimuli/revenc_lowprob_100shot.jsonl"),
        ]:
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    if "5shot" in fo_name:
        example_count = 5
    elif "10shot" in fo_name:
        example_count = 10
    elif "100shot" in fo_name:
        example_count = 100

    if "high" in fo_name:
        in_context_examples = examples_high[:example_count]
    elif "medium" in fo_name:
        in_context_examples = examples_medium[:example_count]
    elif "low" in fo_name:
        in_context_examples = examples_low[:example_count]

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        example["task_name"] = "reverse_enc"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example["example_type"] = example_type


        sentence = line.strip()
        reversed_sentence = " ".join(sentence.split()[::-1])

        
        # Instruction
        example["task_instruction"] = 'Below are some sequences of words; each sequence is followed by the reversed version of that sequence. (When a sequence is being reversed, punctuation marks are moved along with the words that they are attached to.) The last example is missing the reversed sequence; provide the reversed sequence for this example.\n'
        for in_context_example in in_context_examples:
            example["task_instruction"] += 'Original text: "' + in_context_example + '"\n'
            example["task_instruction"] += 'Reversed text: "' + " ".join(in_context_example.split()[::-1]) + '"\n\n'
        example["task_instruction"] += 'Original text: "%s"\n'
        example["task_instruction"] += 'Reversed text:'

        # Input
        example["input"] = sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = reversed_sentence


        jsl.write(example)
        

        count_encoded += 1
        if count_encoded == 100:
            break


    





