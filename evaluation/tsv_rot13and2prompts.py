
import json
import jsonlines
import re
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


end_after_strings = ["Rot-2 text: ", "Rot-13 text: ", "Original text: "]
for prompt in ["basic", "step", "cot"]:
    for task in ["enc", "dec"]:
    
        for model in ["gpt-4"]:
        
            fo = open("table_rot13and2" + task + prompt + "_" + model + ".tsv", "w")
            
            # Headers
            fo.write("\t".join(["index", "task", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

            for condition in ["rot2" + task + prompt + "_highprob", "rot13" + task + prompt + "_highprob"]:
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

                    for end_after_string in end_after_strings:
                        if end_after_string in res:
                            ends = [m.end() for m in re.finditer(end_after_string, res)]
                            res = res[ends[-1]:].strip()


                    if res[0] == '"':
                        res = res[1:]
                    if res[-1] == '"':
                        res = res[:-1]

                    if gt == res:
                        correct = "1"
                        count_correct += 1
                    else:
                        correct = "0"
                    count_total += 1


                    data = [str(index), condition, saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"], 
                            saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct]
                    fo.write("\t".join(data) + "\n")

                print(model, condition, count_correct*1.0/count_total)

                




