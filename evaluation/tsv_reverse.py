
import json
import jsonlines
from Levenshtein import distance


saved_stats = {}
first = True
fi = open("../stimuli/saved_stimuli_statistics.tsv", "r")
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
        saved_stats[this_obj["sentence"]] = this_obj


palm_tokens = {}
fi = open("../stimuli/saved_palm_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    palm_tokens[parts[0]] = parts[1]

llama_tokens = {}
fi = open("../stimuli/saved_llama_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    llama_tokens[parts[0]] = parts[1]



for task in ["enc", "dec"]:
    
    for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-2-70b-chat", "text-bison-001"]:
        
        fo = open("table_rev" + task + "_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        for condition in ["rev" + task + "_highprob", "rev" + task + "_mediumprob", "rev" + task + "_lowprob"]:
            inputs = []
            with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
                for obj in reader:
                    inputs.append(obj["input"])
        
            fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            count_correct = 0
            count_total = 0
            total_dist = 0
            for index, (inp, gt, res) in enumerate(zip(inputs, data["gts"], data["res"])):
                if gt[0] == '"':
                    gt = gt[1:]
                if gt[-1] == '"':
                    gt = gt[:-1]

                if len(res) > 0:
                    if res[0] == '"':
                        res = res[1:]
                if len(res) > 0:
                    if res[-1] == '"':
                        res = res[:-1]

                if gt in res:
                    correct = "1"
                    count_correct += 1
                else:
                    correct = "0"
                count_total += 1

                if model.startswith("gpt"):
                    data = [str(index), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"], 
                            saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct]
                elif model == "llama-2-70b-chat":
                    data = [str(index), saved_stats[inp]["n_characters"], llama_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], llama_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct]
                elif model == "text-bison-001":
                    data = [str(index), saved_stats[inp]["n_characters"], palm_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], palm_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct]
                else:
                    14/0
                fo.write("\t".join(data) + "\n")


            print(model, condition, count_correct*1.0/count_total)

            




