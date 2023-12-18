
import json
from Levenshtein import distance


for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-2-70b-chat", "text-bison-001"]:
    print("")
    print(model)
    for direction in ["enc", "dec"]:
        print("")
        for suffix in ["way", "ay", "yay", "hay", "say"]:
        
            condition = "pig" + direction + "_" + suffix + "_highprob"
        
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
   
                if len(res) > 0:
                    if res[0] == '"':
                        res = res[1:]
                if len(res) > 0:
                    if res[-1] == '"':
                        res = res[:-1]

                dist = distance(gt, res)
                total_dist += dist
            
                if gt.lower() in res.lower():
                    count_correct += 1
                else:
                    if model == "gpt-4-0613":
                        #print(gt)
                        #print(res)
                        #print("")
                        if ("yay" in res and "yay" not in gt) or ("way" in res and "way" not in gt):
                            pass
                            #print(gt)
                            #print(res)
                            #print("")
                count_total += 1

# indmay endingspay*
# othingnay ikelay*
# agmaticpray*
# omplicatedcay erethay*
# utbay isthay imetay*

                #if model == "gpt-4-0613" and "utbay isthay imetay" in gt and direction == "enc":
                #    print(gt)
                #    print(res)
                #    print("")

            print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total)
