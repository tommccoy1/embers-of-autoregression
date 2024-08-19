
import json
from Levenshtein import distance
import statistics
import re

for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]:
    print("")
    print(model)
    #for direction in ["enc", "dec"]:
    for direction in ["enc", "dec"]:
        #for condition in ["rev" + direction + "_highprob", "rev" + direction + "_mediumprob", "rev" + direction + "_lowprob", "rev" + direction + "_adversarial"]:
        for condition in ["rev" + direction + "_highprob", "rev" + direction + "_mediumprob", "rev" + direction + "_lowprob"]: 
        
            fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            count_correct = 0
            count_total = 0
            total_dist = 0
            dists = []
            for gt, res in zip(data["gts"], data["res"]):
                if gt[0] == '"':
                    gt = gt[1:]
                if gt[-1] == '"':
                    gt = gt[:-1]

                res = res.strip()

                if len(res) > 0:
                    if res[0] == '"':
                        res = res[1:]
                if len(res) > 0:
                    if res[-1] == '"':
                        res = res[:-1]

                dist = distance(gt, res)
                total_dist += dist
                dists.append(dist)
            
                if gt in res:
                    count_correct += 1
                    if model == "gpt-4-0613" and "dec_mediumprob" in condition and len(gt) < 55:
                        #print(gt)
                        #print(res)
                        #print("")
                        pass
                else:
                    # Uncomment to show errors
                    if model == "gpt-4-0613" and "dec" in condition and len(gt) < 55 and distance(gt.split(), res.split()) > 0:
                        #print(gt)
                        #print(res)
                        #print("")
                        pass
                    if "claude" in model:
                        #print(gt)
                        #print(res)
                        #print("")
                        pass
                    pass
                count_total += 1

            print(direction, condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))

