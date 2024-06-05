
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

nonfloat = 0
for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]: 
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
          
            #if len(res.split("/")) == 2:
            #    parts = res.split("/")
            #    res = float(parts[0]) / float(parts[1])
            #res = float(res)

            if "So, my answer is 815." in str(res):
                res = "815"
            if res.startswith("173.8\n\nThe problem"):
                res = "173.8"
            if res.startswith("21\n\nInput: 22"):
                res = "21"
            if res.startswith("80\n\nI've been"):
                res = "80"
            if res.startswith("341\n\nHere's how"):
                res = "341"
            if res.startswith("2051\n\nMy question is"):
                res = "2051"
            if res.startswith("963\n\nExplanation:"):
                res = "963"
            if "Answer: 186.8\n" in res:
                res = "186.8"
            if res.startswith("39.2\n"):
                res = "39.2"
            if res.startswith("446\n\nNow"):
                res = "446"
            if res.startswith("9\n\nInput:"):
                res = "9"
            if res.startswith("121\n\nExplanation:"):
                res = "121"
            if res.startswith("130\n\nCan you"):
                res = "130"
            if res.startswith("80\n\nCan you"):
                res = "80"
            if res.startswith("200 × 9/5 + 32 = 200 × 1.8 + 32 = 360 + 32 = 392"):
                res = "392"
            if res.startswith("464 x 7/5 + 31 = 464 x 1.4 + 31 = 649.6 + 31 = 680.6"):
                res = "680.6"
            if "Then, add 32 to get 1121." in res:
                res = "1121"
            if res.startswith("317\n\nMy solution"):
                res = "317"
            if res.startswith("1950\n\nWhat is"):
                res = "1950"
            if res.startswith("301\n\nHere's"):
                res = "301"
            if "So, the answer is:" in res:
                if len(res[res.index("So, the answer is:"):].split()) > 4:
                    res = res[res.index("So, the answer is:"):].split()[4]
            if res.endswith("729 + 32 = 761\n\nSo, the answer is:"):
                res = "761"
            if "So, my answer would be:" in res:
                res = res[res.index("So, my answer would be:"):].split()[5]
            if "the answer is:" in res:
                res = res[res.index("the answer is:"):].split()[3]
            if "Rounded to the nearest integer:" in res:
                res = res[res.index("Rounded to the nearest integer:"):].split()[5]



            gt = float(gt)
            unique_numbers = find_unique_number(res)
                
            if len(unique_numbers) == 1:
                res = unique_numbers[0]
            elif len(unique_numbers) == 0:
                res = -1000000

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


            if str(res).endswith("1149.8\n\nSo, the final answer"):
                res = 1149.8
            if str(res).startswith("39.2\n\nNow, it's your turn."):
                res = 39.2
            if str(res).startswith("17\n\nHere's how it works:"):
                res = 17
            if str(res).startswith("1228\n\nExplanation:"):
                res = 1228
            if str(res).startswith("The number is 6."):
                res = 6

            try:
                res = float(res)
            except:
                print("RES")
                print(res)
                nonfloat += 1

            if gt == res:
                count_correct += 1
                correct = "1"
            else:
                correct = "0"

                #if "claude" in model:
                #    print(gt)
                #    print(res)
                #    print("\n\n\n")

            if model == "gpt-4-0613" and gt != res and condition == "conversion_fake":
                #print(inp)
                #print(gt)
                #print(res)
                #print("")
                pass
            #else:
            #    print(gt, res)
            #else:
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

print(nonfloat)
