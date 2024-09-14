
import json
from Levenshtein import distance
import statistics

for task in ["dec"]:
    
    print("")
    print("")
    print("")
    print("TASK:", task)

    for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]: 
        print("")
        print(model)
        all_accs = []
        for shift in range(1,26):
            for prob in ["highprob"]:

                condition = "shift_" + str(shift)
        
                fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
                data = json.load(fi)

                count_correct = 0
                count_total = 0
                total_dist = 0
                distances = []
                for index, (gt, res) in enumerate(zip(data["gts"], data["res"])):
                    
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
                    distances.append(dist)
            
                    if gt in res:
                        count_correct += 1
                    else:
                        #if model == "gpt-4-0613" and shift == 10: # and "To be or" in res: #shift == 2 and ("crypt" in res or "code" in res): #shift == 10 and len(gt) < 160 and "To be or" in res: #shift == 12 and len(gt) < 60:
                        if model == "gpt-4-0613" and shift == 2 and ("crypt" in res or "code" in res):
                            #print(gt)
                            #print(res)
                            #print("")
                            pass

                    if model == "gpt-4-0613" and shift == 10 and gt != res and len(gt) < 800 and "humanities" in gt: # and gt == res:
                        #print(gt)
                        #print(res)
                        #print("")
                        pass

                    if model == "gpt-4-0613" and gt.startswith("It would just take"):
                        #print(shift)
                        #print(gt)
                        #print(res)
                        #print("")
                        pass

                    #if len(gt) < 100 and model == "gpt-4" and shift == 13:
                    #    print(gt)
                    count_total += 1

                print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, "median levdist:", statistics.median(distances))
                all_accs.append(str(count_correct*1.0/count_total))
        print(",".join(all_accs))


