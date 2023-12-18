
import json
import re
from Levenshtein import distance
import statistics


end_after_strings = ["Original text: ", "message is:", "original text is:", "message is ", "we get:"]
delete_after_strings = ["However, this doesn't make sense", "However, this doesn't make much sense", "This sentence still doesn't make", "However, this sentence doesn't make", "This still doesn't make sense"]

for prompt_type in ["", "step", "cot"]:
     
    print("")
    print("")
    print("")
    print("PROMPT STYLE:", prompt_type)


    for task in ["dec"]:
        for model in ["gpt-4-0613"]:
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
                    orig_res = res[:]

                    for delete_after_string in delete_after_strings:
                        if delete_after_string in res:
                            starts = [m.start() for m in re.finditer(delete_after_string, res)]
                            res = res[:starts[0]].strip()
                        
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
            
                    if gt in res:
                        count_correct += 1
                    else:
                        #if False:
                        if model == "gpt-4-0613" and shift == 12:
                            #print(gt)
                            #print(res)
                            #print("")
                            pass
                        if "\n" in res:
                            #print(gt)
                            #print(res)
                            #print(res.count(" becomes "), len(gt))
                            #print("")
                            pass
                        #if len(gt)*1.0/len(res) > 2: # or len(res)*1.0/len(gt) > 2:
                            #print(gt)
                            #print(res)
                            #print("ORIG", orig_res)
                            #print("")
                    count_total += 1

                print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, "median levdist:", statistics.median(distances))
                all_accs.append(str(count_correct*1.0/count_total))
            print("")
        print(",".join(all_accs))


