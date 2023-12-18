
import json
from Levenshtein import distance
import statistics
import re 

end_after_strings = ["would be:", "the reversed sequence of words:", "the reversed sequence:", "The reverse of the given sequence of words is:", ":", "would be "]
delete_after_strings = ["I hope that helps!", "\"\n\nHere's", "I hope this helps!", "\"\n\nNote:", "\"\n\nIn this reversed version", "\"\n"]

for model in ["llama-2-70b-chat"]:
    print("")
    print(model)
    for direction in ["dec"]:
        for condition in ["swap_next_base_highprob"]: 
        
            fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            count_correct = 0
            count_total = 0
            total_dist = 0
            dists = []
            for gt, res in zip(data["gts"], data["res"]):

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

                
                if True: #"\n" in res:
                    print(gt)
                    print(res)
                    print("")

                dist = distance(gt, res)
                total_dist += dist
                dists.append(dist)
            
                if gt == res:
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
                    pass
                count_total += 1

            print(direction, condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))

