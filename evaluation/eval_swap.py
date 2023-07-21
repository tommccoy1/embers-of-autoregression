
import json
from Levenshtein import distance



for model in ["gpt-3.5-turbo"]:
    print("")
    print(model)
    for condition in ["swap_base_next", "swap_base_prev", "swap_next_base", "swap_prev_base"]:
        
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
                # Uncomment to see what models are doing
                #print(keyboard_decode(gt))
                #print(keyboard_decode(res))
                #print("")
                pass
            count_total += 1

        print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total)
