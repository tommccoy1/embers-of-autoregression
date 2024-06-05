
import json
import jsonlines
from Levenshtein import distance


def article_count(sentence):
    words = sentence.split()

    count = 0

    for word in words:
        if word in ["a", "an", "the"]:
            count += 1

    return count

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



for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]: 
    print("")
    print(model)
    
    for task in ["base_next", "base_prev", "next_base", "prev_base"]:

        print("")
    
        
        fo = open("table_swap_" + task + "_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        for condition in ["swap_" + task + "_highprob", "swap_" + task + "_mediumprob", "swap_" + task + "_lowprob"]:
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

                if " the a " in gt or " a the " in gt or " a an " in gt or " an a " in gt or " an the " in gt or " the an " in gt:
                    print(gt)

                if gt in res:
                    correct = "1"
                    count_correct += 1
                    if model == "gpt-4-0613" and condition in ["swap_next_base_highprob", "swap_next_base_highprob"] and len(gt) < 70 and article_count(gt) > 1:
                        #print(inp)
                        #print(gt)
                        #print(res)
                        #print("")
                        pass
                else:
                    correct = "0"
                    if model == "gpt-4-0613" and condition in ["swap_next_base_lowprob", "swap_next_base_prob"] and len(gt) < 70 and article_count(gt) > 1:
                        #print(inp)
                        #print(gt)
                        #print(res)
                        #print("")
                        pass

                    if "claude" in model:
                        #print(gt)
                        #print(res)
                        #print("\n\n\n")
                        pass

                #if len(gt) < 40 and "moment" in gt:
                #    print(inp)
                #    print(gt)
                #    print("")

                count_total += 1

                if model.startswith("gpt"):
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
                    #pass
                    14/0
                fo.write("\t".join(data) + "\n")



            print(model, condition, count_correct*1.0/count_total)

            




