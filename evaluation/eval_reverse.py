
import json
from Levenshtein import distance


for model in ["gpt-3.5-turbo", "gpt-4"]:
    print("")
    print(model)
    for direction in ["enc", "dec"]:
        for condition in ["rev" + direction + "_highprob", "rev" + direction + "_mediumprob", "rev" + direction + "_lowprob", "rev" + direction + "_adversarial"]: 
        
            fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            count_correct = 0
            count_total = 0
            total_dist = 0
            for gt, res in zip(data["gts"], data["res"]):
                if gt[0] == '"':
                    gt = gt[1:]
                if gt[-1] == '"':
                    gt = gt[:-1]

                if res[0] == '"':
                    res = res[1:]
                if res[-1] == '"':
                    res = res[:-1]

                dist = distance(gt, res)
                total_dist += dist
            
                if gt == res:
                    count_correct += 1
                else:
                    # Uncomment to show errors
                    #if model == "gpt-4" and "dec" in condition:
                    #    print(gt)
                    #    print(res)
                    #    print("")
                    pass
                count_total += 1

            print(direction, condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total)

