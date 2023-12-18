
import json
import jsonlines
from Levenshtein import distance


def find_unique_number(answer):
    words = answer.split()
    numbers = []
    for word in words:
        try:
            float_word = float(word)
            numbers.append(word)
        except:
            pass

    numbers = list(set(numbers))
    return numbers

for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-2-70b-chat", "text-bison-001"]:
    print("")
    print(model)

    fo_initial = open("table_conversion_ood_fwd_" + model + ".tsv", "w")
    fo_inverse = open("table_conversion_ood_rev_" + model + ".tsv", "w")
    fo_method = open("table_conversion_ood_method_" + model + ".tsv", "w")

    fo_initial.write("\t".join(["index", "task", "input", "output", "correct"]) + "\n")
    fo_inverse.write("\t".join(["index", "task", "input", "output", "correct"]) + "\n")
    fo_method.write("\t".join(["index", "task", "input", "output", "correct"]) + "\n")

    for condition in ["conversion_ood_actual", "conversion_ood_fake", "conversion_ood_actualinverse", "conversion_ood_fakeinverse", "conversion_ood_actualprimed", "conversion_ood_actualprimedcontrol"]:

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

            gt = float(gt)

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


            unique_numbers = find_unique_number(res)
                
            if len(unique_numbers) == 1:
                res = unique_numbers[0]
            elif len(unique_numbers) == 0:
                res = -1000000
          
            if len(str(res).split("/")) == 2:
                try:
                    parts = res.split("/")
                    res = float(parts[0]) / float(parts[1])
                except:
                    pass
 
            gt_in_res = False
            for word in str(res).split():
                try:
                    float_word = float(word)
                    if float_word == float(gt):
                        gt_in_res = True
                except:
                    pass

            if not gt_in_res:
                # Don't have to worry about finding the correct answer
                # if there's no way it is in the response
                res = -1000000

            if str(res).startswith("331\n\nHere's how"):
                res = 331
            if str(res).startswith("313\n\nInput:"):
                res = 313
            if str(res).startswith("99\n\nThe input"):
                res = 99
            if str(res).startswith("717\n\nThe number"):
                res = 717
            if str(res).startswith("1046\n\nHere's"):
                res = 1046
            if str(res).startswith("2497\n\nThe solution"):
                res = 2497

            try:
                res = float(res)
            except:
                print("RES")
                print(res)
                print("")
                res = -1000000


            gt = float(gt)

            if gt == res:
                count_correct += 1
                correct = "1"
                if model == "gpt-4-0613" and condition in ["conversion_ood_actual", "conversion_ood_actualprimedcontrol", "conversion_ood_actualprimed"] and inp in ["731", "558", "842"]:
                    #print(inp)
                    #print(gt)
                    #print(res)
                    #print("")
                    pass
            else:
                correct = "0"
                if model == "gpt-4-0613" and condition == "conversion_ood_actualprimed":
                    #print(inp)
                    pass
               
            #if model == "gpt-4-0613" and condition in ["conversion_ood_actual", "conversion_ood_actualprimedcontrol", "conversion_ood_actualprimed"] and inp in ["731", "558", "842", "977"]:
            #    print(inp)
            #    print(gt)
            #    print(res)
            #    print("")
            #    pass

            #if index == 0:
            #    print(gt)
            #    print(res)
            #    print("")
            #else:
            #    print(gt, res)
            #else:
                #print(gt)
                #print(res)
                #print("")
            count_total += 1


            data = [str(index), condition, inp, str(gt), correct]
            if condition in ["conversion_ood_actual", "conversion_ood_fake"]:
                fo_initial.write("\t".join(data) + "\n")
            elif condition in ["conversion_ood_actualinverse", "conversion_ood_fakeinverse"]:
                fo_inverse.write("\t".join(data) + "\n")

            if condition in ["conversion_ood_actual", "conversion_ood_actualprimed", "conversion_ood_actualprimedcontrol"]:
                fo_method.write("\t".join(data) + "\n")




        print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total)

