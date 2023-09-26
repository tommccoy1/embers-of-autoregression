
import json
from Levenshtein import distance
import statistics
import re

def second_not_first_contains(first, second, wordlist):
    for word in wordlist:
        if word in second and word not in first:
            return True
    return False

end_after_strings = ["Rot-2 text: ", "Rot-13 text: ", "Original text: ", "message is:", "message is "]
delete_after_strings = ["However, this doesn't make sense", "However, this doesn't make much sense", "This sentence still doesn't make", "However, this sentence doesn't make", "This still doesn't make sense"]
for task in ["enc", "dec"]:
    
    print("")
    print("")
    print("")
    print("TASK:", task)

    for model in ["gpt-4-0613"]:
        print("")
        print(model)
        for condition in ["rot13" + task + "_highprob", "rot13" + task + "_mediumprob", "rot13" + task + "_lowprob", "rot2" + task + "_highprob"]:

            for prompt in ["", "step", "cot"]:
        
                fi = open("../logs/" + condition.replace("_", prompt + "_") + "_" + model + "_temp=0.0_n=1.json", "r")
                data = json.load(fi)

                count_correct = 0
                count_total = 0
                total_dist = 0
                dists = []
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
                    dists.append(dist)
            
                    if gt == res:
                        count_correct += 1
                    else:
                        if "\n" in res:
                            print(gt)
                            print("RES", res)
                            print("ORIG", orig_res)
                            print("")
                    #elif condition.startswith("rot13enc"):
                    #    print(gt)
                    #    print(res)
                    #    print("")
                        pass
                    #elif condition == "rot13dec_highprob" and model == "gpt-4":
                    #elif task == "dec" and "highprob" in condition and model == "gpt-4" and  second_not_first_contains(gt, res, ["cipher", "code", "crypt", " rot", "shift"]):
                    #elif task == "dec" and "rot13" in condition and model == "gpt-4":
                        #print(gt)
                        #print(res)
                        #print("")
                    #    pass
                    count_total += 1

                print(condition, prompt, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
                #print(dists)
            print("")



