


import statistics
import torch
import tiktoken
import jsonlines
import math

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--fi", help="file to process", type=str, default=None)
args = parser.parse_args()



if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

gpt4_enc = tiktoken.get_encoding("cl100k_base")


number_logfreq = {}
total = 0
fi = open("../corpus_analysis/numbers.txt", "r")
for line in fi:
    parts = line.strip().split()
    number = int(parts[0])
    count = int(parts[1])
    total += count

    number_logfreq[number] = count

for number in number_logfreq:
    number_logfreq[number] = math.log(number_logfreq[number]*1.0/total)


word_logprobs = {}
fi_probs = open("../example_generation_scripts/cmu_words_by_prob.txt", "r")
for line in fi_probs:
    parts = line.strip().split()
    logprob = float(parts[0])
    word = parts[1]

    word_logprobs[word] = logprob

char_logprobs = {}
total_counts = 0
fi_charprobs = open("../corpus_analysis/c4_character_counts.txt", "r")
for line in fi_charprobs:
    parts = line.strip().split()
    
    char = parts[0]
    count = int(parts[1]) + 1 # Using add-1 smoothing, since some have 0 occurrences

    char_logprobs[char] = count
    total_counts += count

for char in char_logprobs:
    char_logprobs[char] = math.log(char_logprobs[char]*1.0) - math.log(total_counts)

saved_statistics = {}
fi = open("saved_stimuli_statistics.tsv", "r")
first = True
index2label = {}
label2index = {}
for line in fi:
    parts = line.strip().split("\t")
    if first:
        for index, label in enumerate(parts):
            index2label[index] = label
            label2index[label] = index
        first = False
    else:
        this_obj = {}
        for index, part in enumerate(parts):
            this_obj[index2label[index]] = part
        saved_statistics[this_obj["sentence"]] = this_obj
fi.close()


# Now reopen the file, but with "append" abilities, so
# that we can add to it as we compute new statistics
fo = open("saved_stimuli_statistics.tsv", "a")


# Compute mean and median for each of the following statistics:
# - input character count
# - output character count
# - input token count (tokenized with GPT-4's tokenizer)
# - output token count (tokenized with GPT-4's tokenizer)
# - input log probability (computed using GPT2-XL)
# - output log probability (computed using GPT2-XL)
input_character_counts = []
output_character_counts = []

input_token_counts = []
output_token_counts = []

input_logprobs = []
output_logprobs = []

with jsonlines.open(args.fi) as reader:
    for obj in reader:
        inp = obj["input"]
        outp = obj["correct_output"]

        if inp in saved_statistics:
            input_character_counts.append(float(saved_statistics[inp]["n_characters"]))
            input_token_counts.append(float(saved_statistics[inp]["n_gpt4_tokens"]))
            input_logprobs.append(float(saved_statistics[inp]["gpt2_logprob"]))
        else:
            input_character_counts.append(len(inp))

            inp_tokens = gpt4_enc.encode(inp)
            input_token_counts.append(len(inp_tokens))

            if "word" in args.fi:
                inp_logprob = 0
                count_logprobs = 0
                for word in inp.split():
                    inp_logprob += word_logprobs[word]
                    count_logprobs += 1
                input_logprobs.append(inp_logprob/count_logprobs)
            elif "char" in args.fi:
                inp_logprob = 0
                count_logprobs = 0
                for char in inp:
                    inp_logprob += char_logprobs[char]
                    count_logprobs += 1
                input_logprobs.append(inp_logprob/count_logprobs)


            # Save to output file
            this_obj = {}
            this_obj["sentence"] = inp
            this_obj["n_characters"] = str(len(inp))
            this_obj["n_gpt4_tokens"] = str(len(inp_tokens))
            this_obj["gpt2_logprob"] = str(inp_logprob/count_logprobs)

            datapoints = [None for _ in range(len(index2label))]
            for index in index2label:
                datapoints[index] = this_obj[index2label[index]]
            fo.write("\t".join(datapoints) + "\n")

        if outp in saved_statistics:
            output_character_counts.append(float(saved_statistics[outp]["n_characters"]))
            output_token_counts.append(float(saved_statistics[outp]["n_gpt4_tokens"]))
            output_logprobs.append(float(saved_statistics[outp]["gpt2_logprob"]))
        else:
            output_character_counts.append(len(outp))

            outp_tokens = gpt4_enc.encode(outp)
            output_token_counts.append(len(outp_tokens))

            outp_logprob = number_logfreq[int(outp)] 
            output_logprobs.append(outp_logprob)

            # Save to output file
            this_obj = {}
            this_obj["sentence"] = outp
            this_obj["n_characters"] = str(len(outp))
            this_obj["n_gpt4_tokens"] = str(len(outp_tokens))
            this_obj["gpt2_logprob"] = str(outp_logprob)

            datapoints = [None for _ in range(len(index2label))]
            for index in index2label:
                datapoints[index] = this_obj[index2label[index]]
            fo.write("\t".join(datapoints) + "\n")



print("MEAN INPUT CHARACTER COUNT", statistics.mean(input_character_counts))
print("MEAN OUTPUT CHARACTER COUNT", statistics.mean(output_character_counts))

print("")

print("MEAN INPUT TOKEN COUNT", statistics.mean(input_token_counts))
print("MEAN OUTPUT TOKEN COUNT", statistics.mean(output_token_counts))

print("")

print("MEAN INPUT LOGPROB", statistics.mean(input_logprobs))
print("MEAN OUTPUT LOGPROB", statistics.mean(output_logprobs))




