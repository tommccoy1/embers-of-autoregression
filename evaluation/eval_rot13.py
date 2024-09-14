
import json
from Levenshtein import distance
import re
import statistics

def second_not_first_contains(first, second, wordlist):
    for word in wordlist:
        if word in second and word not in first:
            return True
    return False


for task in ["enc", "dec"]:
    
    print("")
    print("")
    print("")
    print("TASK:", task)

    for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]:
        print("")
        print(model)
        for condition in ["rot13" + task + "_highprob", "rot13" + task + "_mediumprob", "rot13" + task + "_lowprob", "rot12" + task + "_highprob"]:

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

                if "llama" in model:
                    if len(res) > 0:
                        if res[0] == "?":
                            res = res[1:]

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
                    if condition == "rot13dec_highprob" and model == "gpt-4-0613" and len(gt) < 80 and len(gt) < 80:
                        #print(gt)
                        #print(res)
                        #print("")
                        pass
                else:
                    if condition == "rot13dec_highprob" and model == "gpt-4-0613" and len(gt) < 80 and len(gt) < 80 and distance(gt.split(), res.split()) >= 2:
                        #print(gt)
                        #print(res)
                        #print("")
                        pass

                #elif condition == "rot13dec_highprob" and model == "gpt-4":
                if task == "dec" and "highprob" in condition and model == "gpt-4-0613" and  second_not_first_contains(gt, res, ["cipher", "code", "crypt", " rot", "shift"]):
                #elif task == "dec" and "rot13" in condition and model == "gpt-4":
                    #print(gt)
                    #print(res)
                    #print("")
                    pass
                count_total += 1

            print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
            #print(dists)
