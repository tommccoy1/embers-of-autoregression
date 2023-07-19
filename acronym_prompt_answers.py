
import json
from Levenshtein import distance

answers = {}
fo = open("logs/acronymsprompt_verified.tsv", "w")
for model in ["gpt-3.5-turbo"]:
    print("")
    print(model)
    for dataset in ["highprob", "highprobfreq", "random", "randomfreq"]:
        for condition in ["prompt_plain_acronym1","prompt_plainabbrev_acronym1","prompt_capital_last_acronym1","prompt_capital_first_acronym1","prompt_lower_last_acronym1","prompt_lower_first_acronym1","prompt_capitalcomma_last_acronym1","prompt_capitalcomma_first_acronym1","prompt_capitalspace_last_acronym1","prompt_capitalspace_first_acronym1","prompt_lowercomma_last_acronym1","prompt_lowercomma_first_acronym1","prompt_lowerspace_last_acronym1","prompt_lowerspace_first_acronym1"]: 
            answers[(model, condition + "_" + dataset)] = []
        
            fi = open("logs/" + condition + "_" + dataset + "_" + model + "_temp=0.0_n=1.json", "r")
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


                answers[(model, condition + "_" + dataset)].append(res)


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



