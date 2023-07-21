
import json
from Levenshtein import distance
import statistics


# Number to text
n2t = {}
n2t[1] = "one"
n2t[2] = "two"
n2t[3] = "three"
n2t[4] = "four"
n2t[5] = "five"
n2t[6] = "six"
n2t[7] = "seven"
n2t[8] = "eight"
n2t[9] = "nine"
n2t[10] = "ten"
n2t[11] = "eleven"
n2t[12] = "twelve"
n2t[13] = "thirteen"
n2t[14] = "fourteen"
n2t[15] = "fifteen"
n2t[16] = "sixteen"
n2t[17] = "seventeen"
n2t[18] = "eighteen"
n2t[19] = "nineteen"
for digit, tens in [(20, "twenty"), (30, "thirty"), (40, "forty"), (50, "fifty"), (60, "sixty"), (70, "seventy"), (80, "eighty"), (90, "ninety")]:
    n2t[digit] = tens

    for i in range(1,10):
        n2t[digit+i] = tens + "-" + n2t[i]

# Text to number
t2n = {}
for key in n2t:
    t2n[n2t[key]] = key
    t2n[n2t[key].replace("-"," ")] = key




for model in ["gpt-3.5-turbo"]:
    for condition in ["capitalize_third"]:
        print("")
        print(model)
        for inner in ["common", "rare"]:
            count_by_number = {}

            fi = open("../logs/" + condition + "_" + inner + "_" +  model + "_temp=0.0_n=1.json", "r")
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

                
                dist = distance(res, gt)
                total_dist += dist
                dists.append(dist)

                if res == gt:
                    count_correct += 1
                count_total += 1

                if len(gt.split()) not in count_by_number:
                    count_by_number[len(gt.split())] = [0,0]

                if res == gt:
                    count_by_number[len(gt.split())][0] += 1
                #else:
                #    print(gt)
                #    print(res)
                #    print("")
                count_by_number[len(gt.split())][1] += 1

                
            print(condition + "_" + inner, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
            

            for number in count_by_number:
                print(number, count_by_number[number][0]*1.0/count_by_number[number][1])




