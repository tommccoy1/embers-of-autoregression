
import random

def example_from_list(word_list):
    done = False
    while not done:
        target_word = random.choice(word_list)

        in_context_list = []
        attempts = 0
        while len(in_context_list) < 10 and attempts < 10000:
            attempts += 1
            in_context = random.choice(word_list)

            no_overlap = True
            for char in in_context:
                if char in target_word:
                    no_overlap = False
        
            if no_overlap and in_context not in in_context_list:
                in_context_list.append(in_context)

        if len(in_context_list) == 10:
            done = True

    return target_word, in_context_list
    
fi = open("vocab_tokens_lower.txt", "r")
words = []

for line in fi:
    parts = line.strip().split("\t")
    word = parts[1]

    words.append(word)


highprob = words[:1000]
medprob = words[3000:4000]
lowprob = words[6000:7000]


examples_highprob = []
examples_medprob = []
examples_lowprob = []

targets_highprob = []
targets_medprob = []
targets_lowprob = []

for candidate_index in range(100):  
    done = False
    while not done:
        target_word, context = example_from_list(highprob)
        if target_word not in targets_highprob:
            done = True

    examples_highprob.append([target_word, context])
    targets_highprob.append(target_word)


for candidate_index in range(100):  
    done = False
    while not done:
        target_word, context = example_from_list(medprob)
        if target_word not in targets_medprob:
            done = True

    examples_medprob.append([target_word, context])
    targets_medprob.append(target_word)



for candidate_index in range(100):  
    done = False
    while not done:
        target_word, context = example_from_list(lowprob)
        if target_word not in targets_lowprob:
            done = True

    examples_lowprob.append([target_word, context])
    targets_lowprob.append(target_word)


fo_highprob = open("../examples/shift_fewshot_highprob.txt", "w")
for target_word, context in examples_highprob:
    fo_highprob.write(target_word + "\t" + " ".join(context) + "\n")


fo_medprob = open("../examples/shift_fewshot_medprob.txt", "w")
for target_word, context in examples_medprob:
    fo_medprob.write(target_word + "\t" + " ".join(context) + "\n")


fo_lowprob = open("../examples/shift_fewshot_lowprob.txt", "w")
for target_word, context in examples_lowprob:
    fo_lowprob.write(target_word + "\t" + " ".join(context) + "\n")



