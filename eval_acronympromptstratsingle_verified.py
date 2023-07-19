
import json
from Levenshtein import distance
import statistics
import scipy
import numpy as np

fi = open("logs/acronymspromptstratifiedsingle_verified.tsv", "r")
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
    dists_dict = {}
    for conditiona in ["prompt_capital_first_acronym1_stratsingle"]:
        for inner in ["common", "rare"]:
            print("")
            for outer in ["common", "rare"]:
                condition = conditiona + "_" + inner + "_" + outer
        
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

                    gt = gt.lower()
                    res = res.lower()
    
                    dist = distance(gt, res)
                    total_dist += dist
                    dists.append(dist)
                    
                    if gt == res:
                        count_correct += 1
                    count_total += 1

                print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
                dists_dict[condition] = dists

            #print("Acronym 1", scipy.stats.ttest_ind(a=np.array(dists_dict["acronym1_highprob"]), b=np.array(dists_dict["acronym1_random"])))
            #print("Acronym 2", scipy.stats.ttest_ind(a=np.array(dists_dict["acronym2_highprob"]), b=np.array(dists_dict["acronym2_random"])))
