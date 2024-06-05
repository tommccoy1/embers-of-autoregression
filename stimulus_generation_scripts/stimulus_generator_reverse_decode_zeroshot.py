
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



for fi_name, fo_name in [("../examples/sentences_high_probability_test.txt", "../stimuli/revdec_highprob_0shot.jsonl"), ("../examples/sentences_medium_probability_test.txt", "../stimuli/revdec_mediumprob_0shot.jsonl"), ("../examples/sentences_low_probability_test.txt", "../stimuli/revdec_lowprob_0shot.jsonl"),
        ]:
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

    count_encoded = 0
    for line in fi:
        example = {}

        # Task
        example["task_name"] = "reverse_dec"

        # Condition
        example_type = fo_name.split("_")[1].split(".")[0]
        example["example_type"] = example_type


        sentence = line.strip()
        reversed_sentence = " ".join(sentence.split()[::-1])

        
        # Instruction
        example["task_instruction"] = 'Below is a sequence of words in reversed order. Provide the original sequence that this sequence was created from. (When the sequence was reversed, punctuation marks were moved along with the words that they were attached to.)\n' 
        example["task_instruction"] += 'Reversed text: "%s"\n'
        example["task_instruction"] += 'Original text:'

        # Input
        example["input"] = reversed_sentence

        # Combining the instruction and input (this is the string that should be given to the model)
        example["instruction_plus_input"] = example["task_instruction"] % example["input"]

        # The correct output
        example["correct_output"] = sentence


        jsl.write(example)
        

        count_encoded += 1
        if count_encoded == 100:
            break


    





