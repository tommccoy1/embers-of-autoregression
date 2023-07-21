
import json
from Levenshtein import distance
import statistics


manually_recognized_answers = {}
manually_recognized_answers["HOS TILE"] = 1
manually_recognized_answers["ACC LAMI"] = 1
manually_recognized_answers["FI NANACEN"] = 1
manually_recognized_answers["CR EAT SET"] = 1
manually_recognized_answers["NO NSTO P"] = 1
manually_recognized_answers["FINE LINE"] = 1
manually_recognized_answers["ME MORI AIR"] = 1
manually_recognized_answers["ME MORI"] = 1
manually_recognized_answers["REMO TEST"] = 1

for model in ["gpt-3.5-turbo"]:
    for condition in ["acronym1", "acronym2"]:
        print("")
        print(model)
        for inner in range(1,6):
            print("")
            for outer in range(1,6):

                if condition == "acronym2" and (inner != 1 or outer != 1):
                    continue
        
                fi = open("../logs/" + condition + "_" + str(inner) + str(outer) + "_" +  model + "_temp=0.0_n=1.json", "r")
                data = json.load(fi)


                dists = []
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

                    res = res.lower()
                    res = res.replace("the sequence of letters created when combining the first letters of the words in the given sequence is ", "")
                    res = res.replace("the sequence of letters created when combining the first letters of the words in the given sequence is: ", "")
                    res = res.replace("the sequence of letters created when you combine the second letters of the words in the given sequence is ", "")
                    res = res.replace("the sequence of letters is: ", "")
                    res = res.replace("the abbreviation created when you combine the first letters of the words in the given sequence is ", "")
                    res = res.replace("the abbreviation created when combining the first letters of the words in the given sequence is ", "")
                    res = res.replace("the first letters spell ", "")
                    res = res.replace("answer: ", "")
                    res = res.replace("the sequence of letters created is: ", "")
                    
                    res = res.replace("\"", "")
                    res = res.replace(".", "")
                    res = res.replace("\n", "")
                    res = res.replace(", ", "")
                    res = res.replace(",", "")
                    words = res.split()
                    all_single = True
                    for word in words:
                        if len(word) != 1:
                            all_single = False
                    if all_single:
                        res = res.replace(" ", "")

                    words = res.split()
                    if len(words) >= 2:
                        if words[-2] == "is":
                            res = words[-1]
                        elif words[-1].startswith("is:"):
                            res = words[-1][3:]


                    res = res.upper()
                    gt = gt.upper()

                    if res in manually_recognized_answers:
                        res = res.replace(" ", "")
                    elif len(res.split()) != 1:
                        print(res)
    

                    dist = distance(gt, res)
                    total_dist += dist
                    dists.append(dist)

                    if res == gt:
                        count_correct += 1
                    count_total += 1
                
                print(condition + "_" + str(inner) + str(outer), "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
            


