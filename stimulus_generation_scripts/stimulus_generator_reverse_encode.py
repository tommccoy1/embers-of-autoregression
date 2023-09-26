
import jsonlines



for fi_name, fo_name in [("../examples/sentences_high_probability.txt", "../stimuli/revenc_highprob.jsonl"), ("../examples/sentences_medium_probability.txt", "../stimuli/revenc_mediumprob.jsonl"), ("../examples/sentences_low_probability.txt", "../stimuli/revenc_lowprob.jsonl"), ("../examples/sentences_adversarial.txt", "../stimuli/revenc_adversarial.jsonl")]:
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")
    jsl = jsonlines.Writer(fo)

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
        example["task_instruction"] = 'Reverse the following sequence of words. Punctuation marks should be moved along with the words they are attached to; e.g., the reversed version of "Good morning, everyone!" would be "everyone! morning, Good": "%s"'

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


    





