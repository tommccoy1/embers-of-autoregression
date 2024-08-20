
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

word_logprobs = {}
fi = open("../example_generation_scripts/vocab_tokens_lower.txt")
for line in fi:
    parts = line.strip().split("\t")
    logprob = float(parts[0]) + 13.357776641845703
    word = parts[1]

    word_logprobs[word] = logprob

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

    for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "claude-3-opus-20240229"]: 

        for nshot in ["0shot", "5shot", "10shot"]:

            if model.startswith("ft") and nshot != "0shot":
                continue

            for suffix in ["word", "word_overlap"]:
                fo = open("table_few_rot13" + task + "_" + suffix + "_" + model + "_" + nshot + ".tsv", "w")
        
                # Headers
                fo.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

                for condition in ["rot13" + task + "_highprob_" + suffix + "_" + nshot, "rot13" + task + "_mediumprob_" + suffix + "_" + nshot, "rot13" + task + "_lowprob_" + suffix + "_" + nshot]:
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
    
                        dist = distance(gt, res)

                        if task == "enc":
                            inp_logprob = str(word_logprobs[inp])
                            outp_logprob = saved_stats[gt]["gpt2_logprob"]
                        else:
                            inp_logprob = saved_stats[inp]["gpt2_logprob"]
                            outp_logprob = str(word_logprobs[gt])

                        if "gpt" in model:
                            data = [str(index), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], inp_logprob, 
                                    saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], outp_logprob, correct]
                        elif model == "llama-3-70b-chat-hf":
                            data = [str(index), saved_stats[inp]["n_characters"], llama3_tokens[inp], inp_logprob,
                                    saved_stats[gt]["n_characters"], llama3_tokens[gt], outp_logprob, correct]
                        elif model == "gemini-1.0-pro-001":
                            data = [str(index), saved_stats[inp]["n_characters"], gemini_tokens[inp], inp_logprob,
                                    saved_stats[gt]["n_characters"], gemini_tokens[gt], outp_logprob, correct]
                        elif model == "claude-3-opus-20240229":
                            data = [str(index), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], inp_logprob,
                                    saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], outp_logprob, correct]
                        else:
                            14/0

                        fo.write("\t".join(data) + "\n")

                    print(model, nshot, suffix, condition, count_correct*1.0/count_total)

            




