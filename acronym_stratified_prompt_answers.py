
import json
from Levenshtein import distance

answers = {}
fo = open("logs/acronymspromptstratified_verified.tsv", "w")
for model in ["gpt-3.5-turbo"]:
    print("")
    print(model)
    for inner in ["common", "medium", "rare", "random"]:
        for outer in ["common", "medium", "rare", "random"]:
            for condition in ["prompt_plain_acronym1_strat","prompt_capital_first_acronym1_strat","prompt_capitalperiod_first_acronym1_strat"]:
                answers[(model, condition + "_" + inner + "_" + outer)] = []
        
                fi = open("logs/" + condition + "_" + inner + "_" + outer + "_" +  model + "_temp=0.0_n=1.json", "r")
                data = json.load(fi)

                for gt, res in zip(data["gts"], data["res"]):

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


                    answers[(model, condition + "_" + inner + "_" + outer)].append(res)


first_row = []
for model, condition in answers:
    first_row.append(model + "_" + condition)
first_row = "\t".join(first_row)
fo.write(first_row + "\n")

rows = []
for index in range(100):
    this_row = []
    for key in answers:
        this_row.append(answers[key][index])
    rows.append(this_row)

for row in rows:
    fo.write("\t".join(row) + "\n")



