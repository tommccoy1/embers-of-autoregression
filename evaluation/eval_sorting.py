
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





manual_dict = {}



for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-2-70b-chat", "text-bison-001"]:
    print("")
    print(model)

    fo_words = open("table_sortwords_" + model + ".tsv", "w")
    fo_words.write("\t".join(["index", "task", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

    fo_numbers = open("table_sortnumbers_" + model + ".tsv", "w")
    fo_numbers.write("\t".join(["index", "task", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

    for direction in ["fwd", "rev", "ascending", "descending"]:
        for condition in ["sorting_" + direction]: 
        
            fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            count_correct = 0
            count_total = 0
            total_dist = 0

            pairwise_correct = 0
            pairwise_total = 0

            inputs = []
            with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
                for obj in reader:
                    inputs.append(obj["input"])

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

                res = ", ".join(res.split("\n"))
                if res in manual_dict:
                    res = manual_dict[res]
            
                res = res.replace("The list of numbers in descending order is as follows:, , ", "").strip()
               
                words_gt = gt.split(", ")
                words_res = res.split(", ")

                for index1, word1 in enumerate(words_gt[:-1]):
                    for index2, word2 in enumerate(words_gt[index1+1:]):
                        if word1 not in words_res or word2 not in words_res:
                            correct = False
                        else:
                            index1_res = words_res.index(word1)
                            index2_res = words_res.index(word2)

                            if index1_res < index2_res:
                                correct = True
                            else:
                                correct = False

                        if correct:
                            pairwise_correct += 1
                        pairwise_total += 1
                        


 
                dist = distance(gt.split(), res.split())
                total_dist += dist

               

                if gt in res:
                    count_correct += 1
                    correct_answer = "1"
                else:
                    correct_answer = "0"
                    if len(gt.split(", ")) != len(res.split(", ")):
                        if len(res.split(" ")) != len(res.split(", ")):
                            #print(gt)
                            #print(res)
                            #print("")
                            pass
                    # Uncomment to show errors
                    if model == "gpt-4-0613" and len(words_gt) == 13 and "rev" in condition and distance(gt.split(), res.split()) > 2:
                        #print(gt)
                        #print(res)
                        #print(inp)
                        #print("")
                        pass
                    pass

                if inp.startswith("big, evergreen") and model == "gpt-4-0613":
                    #print(gt)
                    #print(res)
                    #print(inp)
                    #print("")
                    pass

                count_total += 1


                if model.startswith("gpt"):
                    data = [str(index), direction, saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"], 
                            saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct_answer]
                elif model == "llama-2-70b-chat":
                    data = [str(index), direction, saved_stats[inp]["n_characters"], llama_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], llama_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct_answer]
                elif model == "text-bison-001":
                    data = [str(index), direction, saved_stats[inp]["n_characters"], palm_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], palm_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct_answer]
                else:
                    14/0


                if direction in ["fwd", "rev"]:
                    fo_words.write("\t".join(data) + "\n")
                elif direction in ["ascending", "descending"]:
                    fo_numbers.write("\t".join(data) + "\n")


            print(direction, condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, "pairwise:", pairwise_correct*1.0/pairwise_total, pairwise_correct, pairwise_total)

