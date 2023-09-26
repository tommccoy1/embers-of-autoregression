
import json
import jsonlines
from Levenshtein import distance
import statistics


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



def is_year(string):
    if string.isnumeric() and len(string) == 4 and int(string) > 1700 and int(string) < 2020:
        return True
    else:
        return False

def is_day(string):
    if string.isnumeric() and int(string) > 0 and int(string) < 32:
        return True
    else:
        return False

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def is_month(string):
    return string in months

def is_date(string):
    words = string.split()
    if len(words) == 3 and words[1].endswith(","):
        return is_month(words[0]) and is_day(words[1][:-1]) and is_year(words[2])
    else:
        return False




for task in [""]:
    
    for model in ["gpt-3.5-turbo-0613", "gpt-4-0613"]:
        print("")
        print(model)

        fo = open("table_birthdays_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")
        for condition in ["birthdays_1", "birthdays_2", "birthdays_3", "birthdays_4"]:
        
            fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            inputs = []
            with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
                for obj in reader:
                    inputs.append(obj["input"])

            count_correct = 0
            count_total = 0
            total_dist = 0
            dists = []
            for index, (inp, gt, res) in enumerate(zip(inputs, data["gts"], data["res"])):
                if gt[0] == '"':
                    gt = gt[1:]
                if gt[-1] == '"':
                    gt = gt[:-1]

                if res[0] == '"':
                    res = res[1:]
                if res[-1] == '"':
                    res = res[:-1]

                res = res.replace(".", "")
                if "was born on" in res:
                    end_index = res.index("was born on") + 12
                    res = res[end_index:]

                dist = distance(gt, res)
                total_dist += dist
                dists.append(dist)
            
                correct_answer = "0"
                if gt == res:
                    count_correct += 1
                    correct_answer = "1"
                if condition == "birthdays_4" and gt == "September 22, 1958":
                    #print(inp)
                    #print(gt)
                    #print(res)
                    #print("")
                    pass
                elif not is_date(res) and not "is not publicly available" in res and not res.startswith("Your question lacks specific details") and not res.startswith("I'm sorry") and not "is not available" in res and not "I don't have access to" in res and not res.startswith("Without more specific information") and not res.startswith("The information provided does not specify") and not "is not readily available" in res and not "As there are several notable people" in res and not "is not sufficient" in res and not "is too vague" in res:
                    print(gt)
                    print(res)
                    print("")
                    pass
                count_total += 1

                data = [str(index), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                        saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct_answer]
                fo.write("\t".join(data) + "\n")

            print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
            #print(dists)
