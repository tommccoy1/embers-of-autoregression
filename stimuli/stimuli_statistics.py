


import statistics
import torch
import tiktoken
import jsonlines

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--fi", help="file to process", type=str, default=None)
parser.add_argument("--use_model", help="use model; necessary if this dataset is not already in saved_stimuli_statistics", action="store_true")
args = parser.parse_args()



if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

if args.use_model:
    from transformers import AutoTokenizer, RobertaForMaskedLM, GPT2LMHeadModel, GPT2Tokenizer
    gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
    gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2-xl").to(device)

gpt4_enc = tiktoken.get_encoding("cl100k_base")

# Get logprob using GPT-2
def logprob_gpt2(sentence):

    # Tokenize the sentence
    tokens = gpt2_tokenizer.encode(sentence)

    targets = tokens[:]

    # Compute average log likelihood for the generation
    input_ids = torch.LongTensor(tokens).to(device)
    target_ids = torch.LongTensor(targets).to(device)

    with torch.no_grad():
        outputs = gpt2_model(input_ids, labels=target_ids)
        log_likelihood = -1*outputs[0]*len(tokens)

    return log_likelihood.item()


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

            inp_logprob = logprob_gpt2(inp)
            input_logprobs.append(inp_logprob)

            # Save to output file
            this_obj = {}
            this_obj["sentence"] = inp
            this_obj["n_characters"] = str(len(inp))
            this_obj["n_gpt4_tokens"] = str(len(inp_tokens))
            this_obj["gpt2_logprob"] = str(inp_logprob)

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

            outp_logprob = logprob_gpt2(outp)
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
#print("MEDIAN INPUT CHARACTER COUNT", statistics.median(input_character_counts))
print("MEAN OUTPUT CHARACTER COUNT", statistics.mean(output_character_counts))
#print("MEDIAN OUTPUT CHARACTER COUNT", statistics.median(output_character_counts))

print("")

print("MEAN INPUT TOKEN COUNT", statistics.mean(input_token_counts))
#print("MEDIAN INPUT TOKEN COUNT", statistics.median(input_token_counts))
print("MEAN OUTPUT TOKEN COUNT", statistics.mean(output_token_counts))
#print("MEDIAN OUTPUT TOKEN COUNT", statistics.median(output_token_counts))

print("")

print("MEAN INPUT LOGPROB", statistics.mean(input_logprobs))
#print("MEDIAN INPUT LOGPROB", statistics.median(input_logprobs))
print("MEAN OUTPUT LOGPROB", statistics.mean(output_logprobs))
#print("MEDIAN OUTPUT LOGPROB", statistics.median(output_logprobs))




