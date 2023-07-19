
import json
from Levenshtein import distance
import statistics

letter = "h"

fi = open("logs/acronyms" + letter + "_verified.tsv", "r")
index2name = {}
name2res = {}
first = True
for line in fi:
    if first:
        names = line.strip().split("\t")
        for index, name in enumerate(names):
            parts = name.strip().split("_")
            model = parts[0]
            condition = "_".join(parts[1:])
            index2name[index] = (model, condition)
            name2res[(model, condition)] = []
        first = False

    else:
        parts = line.strip().split("\t")
        for index, part in enumerate(parts):
            name2res[index2name[index]].append(part)



for model in ["gpt-3.5-turbo"]:
    print("")
    print(model)
    for condition in ["acronym1" + letter + "_highprob", "acronym1" + letter + "_random", "acronym2" + letter + "_highprob", "acronym2" + letter + "_random"]:
        
        fi = open("logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
        data = json.load(fi)

        dists = []
        count_correct = 0
        count_total = 0
        total_dist = 0
        for gt, res in zip(data["gts"], name2res[(model, condition)]):
            if gt[0] == '"':
                gt = gt[1:]
            if gt[-1] == '"':
                gt = gt[:-1]

            dist = distance(gt, res)
            total_dist += dist
            dists.append(dist)
            
            if gt == res:
                count_correct += 1
            count_total += 1

        print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
