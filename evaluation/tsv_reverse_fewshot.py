
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


gemini_tokens = {}
fi = open("../stimuli/saved_gemini_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    gemini_tokens[parts[0]] = parts[1]

llama3_tokens = {}
fi = open("../stimuli/saved_llama3_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    llama3_tokens[parts[0]] = parts[1]



for task in ["enc", "dec"]:
    
    for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "claude-3-opus-20240229", "ft_gpt-3.5_10shot", "ft_gpt-3.5_100shot"]:

        for nshot in ["0shot", "5shot", "10shot"]:

            if model.startswith("ft") and nshot != "0shot":
                continue
        
            fo = open("table_few_rev" + task + "_" + model + "_" + nshot + ".tsv", "w")
            fo.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

            for condition in ["rev" + task + "_highprob_" + nshot, "rev" + task + "_mediumprob_" + nshot, "rev" + task + "_lowprob_" + nshot]:
                inputs = []
                with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
                    for obj in reader:
                        inputs.append(obj["input"])
        
                if model.startswith("ft"):
                    full_model = None
                    if model == "ft_gpt-3.5_10shot":
                        if task == "enc":
                            if "high" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:reh-10shot:9SALatx6" 
                            elif "medium" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rem-10shot:9SALjJuT"
                            elif "low" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rel-10shot:9SAMip7T"
                        elif task == "dec":
                            if "high" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rdh-10shot:9S9QOf6v"
                            elif "medium" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rdm-10shot:9S9QgVm4"
                            elif "low" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rdl-10shot:9S9dK7en"
                    elif model == "ft_gpt-3.5_100shot":
                        if task == "enc":
                            if "high" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:reh-100shot:9SABR6eq"
                            elif "medium" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rem-100shot:9SAEh76I"
                            elif "low" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rel-100shot:9SACHgpi"
                        elif task == "dec":
                            if "high" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rdh-100shot:9S9VZFB5"
                            elif "medium" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rdm-100shot:9S9gUIsK"
                            elif "low" in condition:
                                full_model = "ft:gpt-3.5-turbo-0613:personal:rdl-100shot:9S9gPeoH"
                    fi = open("../logs/" + condition + "_" + full_model + "_temp=0.0_n=1.json", "r")
                else:
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
    
                    if "gpt" in model:
                        data = [str(index), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"], 
                                saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct]
                    elif model == "llama-3-70b-chat-hf":
                        data = [str(index), saved_stats[inp]["n_characters"], llama3_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[gt]["n_characters"], llama3_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct]
                    elif model == "gemini-1.0-pro-001":
                        data = [str(index), saved_stats[inp]["n_characters"], gemini_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[gt]["n_characters"], gemini_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct]
                    elif model == "claude-3-opus-20240229":
                        data = [str(index), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct]
                    else:
                        14/0
                    fo.write("\t".join(data) + "\n")
    
    
                print(model, condition, count_correct*1.0/count_total)
    
            




