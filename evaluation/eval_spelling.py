
import json
import jsonlines
from Levenshtein import distance
import statistics

manually_recognized_answers = {}
manual_answers = []
for answer in manual_answers:
    manually_recognized_answers[answer] = 1


for model in ["gpt-3.5-turbo-0613", "gpt-4-0613"]:
    print("")
    print(model)

    for condition in ["all"]:

        inputs = []
        with jsonlines.open("../stimuli/spelling_" + condition + ".jsonl") as reader:
            for obj in reader:
                inputs.append(obj["input"])
        

        fi = open("../logs/spelling_" + condition + "_" +  model + "_temp=0.0_n=1.json", "r")
        data = json.load(fi)


        dists = []
        count_correct = 0
        count_total = 0
        total_dist = 0
        for index, (inp, gt, res) in enumerate(zip(inputs, data["gts"], data["res"])):
 
            if gt[0] == '"':
                gt = gt[1:]
            if gt[-1] == '"':
                gt = gt[:-1]

            if res[0] == '"':
                res = res[1:]
            if res[-1] == '"':
                res = res[:-1]

            res = res.lower()
            gt = gt.lower()

            res = res.replace(" - ", " ")
            res = res.replace("-", " ")
            

            dist = distance(gt, res)
            total_dist += dist
            dists.append(dist)

            if res == gt:
                count_correct += 1
            else:
                print(res)
                print(gt)
                print("")
                pass
            count_total += 1


        print("spelling_" + condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
            


