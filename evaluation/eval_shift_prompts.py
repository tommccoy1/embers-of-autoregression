
import json
import re
from Levenshtein import distance
import statistics


end_after_strings = ["Original text: "]

for prompt_type in ["basic", "step", "cot"]:
     
    print("")
    print("")
    print("")
    print("PROMPT STYLE:", prompt_type)


    for task in ["dec"]:
        for model in ["gpt-4"]:
            print("")
            print(model)
            all_accs = []
            for shift in range(1,26):

                condition = "shift" + prompt_type + "_" + str(shift)
        
                fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
                data = json.load(fi)

                count_correct = 0
                count_total = 0
                total_dist = 0
                distances = []
                for gt, res in zip(data["gts"], data["res"]):

                    for end_after_string in end_after_strings:
                        if end_after_string in res:
                            ends = [m.end() for m in re.finditer(end_after_string, res)]
                            res = res[ends[-1]:].strip()
                        

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
                    distances.append(dist)
            
                    if gt == res:
                        count_correct += 1
                    else:
                        if False:
                        #if model == "gpt-4" and shift == 13:
                            print(gt)
                            print(res)
                            print("")
                            pass
                    count_total += 1

                print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, "median levdist:", statistics.median(distances))
                all_accs.append(str(count_correct*1.0/count_total))
            print("")
        print(",".join(all_accs))


