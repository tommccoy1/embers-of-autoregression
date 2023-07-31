
import json
from Levenshtein import distance

answers_highprob = []
fi_highprob = open("../examples/sentences_high_probability.txt", "r")
for line in fi_highprob:
    answers_highprob.append(line.strip())

for model in ["gpt-3.5-turbo", "gpt-4"]:
    print("")
    print(model)
    for condition in ["rot13dec_adversarial", "rot2dec_adversarial"]: 
        
        fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
        data = json.load(fi)

        count_correct_full = 0
        count_correct_critical = 0
        count_regularized_full = 0
        count_regularized_critical = 0
        count_total = 0

        for gt, res, regularized in zip(data["gts"], data["res"], answers_highprob):
            if gt[0] == '"':
                gt = gt[1:]
            if gt[-1] == '"':
                gt = gt[:-1]

            if res[0] == '"':
                res = res[1:]
            if res[-1] == '"':
                res = res[:-1]

            if res == gt:
                count_correct_full += 1
            if res == regularized:
                count_regularized_full += 1
            for index, (word_gt, word_regularized) in enumerate(zip(gt.split(), regularized.split())):
                if word_gt != word_regularized:
                    index_difference = index
                    correct_word = word_gt
                    regularized_word = word_regularized

            if len(res.split()) > index_difference:
                res_word = res.split()[index_difference]
            else:
                res_word = ""

            if res_word == correct_word:
                count_correct_critical += 1
            if res_word == regularized_word:
                count_regularized_critical += 1


            count_total += 1

        print(condition, "full correct:", count_correct_full*1.0/count_total, "full regularized:", count_regularized_full*1.0/count_total, "critical correct:", count_correct_critical*1.0/count_total, "critical regularized:", count_regularized_critical*1.0/count_total)



