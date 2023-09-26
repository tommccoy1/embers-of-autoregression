
import json
import jsonlines
from Levenshtein import distance


for model in ["gpt-3.5-turbo-0613", "gpt-4-0613"]:
    print("")
    print(model)

    fo_initial = open("table_conversion_fwd_" + model + ".tsv", "w")
    fo_inverse = open("table_conversion_rev_" + model + ".tsv", "w")
    fo_method = open("table_conversion_method_" + model + ".tsv", "w")

    fo_initial.write("\t".join(["index", "task", "input", "output", "correct"]) + "\n")
    fo_inverse.write("\t".join(["index", "task", "input", "output", "correct"]) + "\n")
    fo_method.write("\t".join(["index", "task", "input", "output", "correct"]) + "\n")

    for condition in ["conversion_actual", "conversion_fake", "conversion_actualinverse", "conversion_fakeinverse", "conversion_actualprimed", "conversion_actualprimedcontrol"]:

        inputs = []
        with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
            for obj in reader:
                inputs.append(obj["input"])

        fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
        data = json.load(fi)

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

            if res[-1] == ".":
                res = res[:-1]

            if res.startswith("The answer is "):
                res = res.replace("The answer is ", "")

            res_parts = res.split("\n")
            if res_parts[-1].startswith("Answer: "):
                res = res_parts[-1].split()[-1]

            res_words = res.split()
            if len(res_words) > 2 and res_words[-2] == "=":
                res = res_words[-1]

            if len(res_words) > 3 and res_words[-4:-1] == ["the", "answer", "of"] or res_words[-4:-1] == ["an", "answer", "of"] or res_words[-4:-1] == ["final", "answer", "of"] or res_words[-4:-1] == ["the", "answer", "is"]: 
                res = res_words[-1]
            
            elif len(res_words) > 2 and res_words[-2] == "degrees" and res_words[-1] == "Fahrenheit":
                res = res_words[-3]
          
            if len(res.split("/")) == 2:
                parts = res.split("/")
                res = float(parts[0]) / float(parts[1])
            res = float(res)


            gt = float(gt)

            if gt == res:
                count_correct += 1
                correct = "1"
            else:
                correct = "0"

            if model == "gpt-4-0613" and gt != res and condition == "conversion_fake":
                print(inp)
                print(gt)
                print(res)
                print("")
                pass
            #else:
            #    print(gt, res)
            #else:
                #print(gt)
                #print(res)
                #print("")
            count_total += 1


            data = [str(index), condition, inp, str(gt), correct]
            if condition in ["conversion_actual", "conversion_fake"]:
                fo_initial.write("\t".join(data) + "\n")
            elif condition in ["conversion_actualinverse", "conversion_fakeinverse"]:
                fo_inverse.write("\t".join(data) + "\n")

            if condition in ["conversion_actual", "conversion_actualprimed", "conversion_actualprimedcontrol"]:
                fo_method.write("\t".join(data) + "\n")




        print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total)


