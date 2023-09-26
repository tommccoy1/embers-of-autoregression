
import json
import jsonlines
from Levenshtein import distance
import statistics

saved_stats = {}
first = True
fi = open("../stimuli/saved_stimuli_statistics.tsv", "r")
index2label = {}
label2index = {}
for line in fi:
    parts = line.strip().split("\t")
    if first:
        for index, label in enumerate(parts):
            index2label[index] = label
            label2index[label] = index
        first = False

    else:
        this_obj = {}
        for index, part in enumerate(parts):
            this_obj[index2label[index]] = part
        saved_stats[this_obj["sentence"]] = this_obj


manually_recognized_answers = {}
manual_answers = ["UNCLE SAM", "THE ROADSTER", "BE LATE D", "BAC KIN GI", "THE RIVES", "NO NCO", "TRAN SIT", "CR EAT OR", "SHORTE R", "TEACH ER", "APP LIED" "STAR TREK", "APP LIDE", "PRUDE NT", "STAR TRE", "MATC HUP", "STAR TREK", "POPU LAR", "HIPS TER", "AME RICA", "SP ECIES", "NEAR EST", "REC LAM", "APP LIED", "PRINTE D", "STAR TUP", "SHA TTER", "UNCLE AR", "NEAR EAST", "CONE SLOE", "PAS SIV VE", "SP EC IE S", "PAS SIVE", "CLIC KER", "DRI LLED", "COND CERT", "SMARTE R", "AR RIV AL", "ROUN DUP", "MARKE RS", "ROTA TED", "COUNTE D", "HAS HING", "STAR TREKS", "BLUE RED", "LIGH TEN", "HAS HING", "STAR TED", "FAR RIRE", "ANNA BEL", "COUNTE D", "HAS HING", "PAS SING", "STAN GER", "BRA TTLE", "CHES TER", "LES SING", "BLAC KEN", "ARCHE RS", "STEALE R", "STEA MED", "STAC KER", "BAC KERS", "BAC KM AN", "BACKE RS", "BAC KERS", "SPELLE R", "LES SIGN", "MANS HIP", "MAD DING", "TRAN SOM", "ONE TIME", "EARS HOT", "MAR KMAN", "SEL ECTS", "PAT CHIN", "NEW SMAN", "CEN TIME", "POPP ELL", "OVE RUSE", "CARDO NE", "FIRS TAR", "TORS TAR", "RAIN GER", "HAS H MAN", "ROSA BEL", "HAN DIER", "ATTA CHE", "WRATH ER", "RECR OSS", "ARMR EST", "PATCHE N", "NEW SOME", "SEC LUDE", "GERS TER", "INCS TAR", "INS CORE", "DEC HANT", "MARKE RT"]
for answer in manual_answers:
    manually_recognized_answers[answer] = 1



for model in ["gpt-3.5-turbo-0613", "gpt-4-0613"]:
    for variable in ["vary_task"]:

        fo = open("table_acronym_varytask_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "task", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        for condition in ["acronym1", "acronym2"]:

            inner_end = 2
            outer_end = 2


            print("")
            print(model)
            for inner in range(1,inner_end):
                print("")
                for outer in range(1,outer_end):

                    if condition == "acronym2" and (inner != 1 or outer != 1):
                        continue
    
                    if inner != 1 and outer != 1:
                        continue

                    inputs = []
                    with jsonlines.open("../stimuli/" + condition + "_" + str(inner) + str(outer) + ".jsonl") as reader:
                        for obj in reader:
                            inputs.append(obj["input"])
        

                    fi = open("../logs/" + condition + "_" + str(inner) + str(outer) + "_" +  model + "_temp=0.0_n=1.json", "r")
                    data = json.load(fi)
                    fi.close()


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
                        res = res.replace("the sequence of letters created when combining the first letters of the words in the given sequence is ", "")
                        res = res.replace("the sequence of letters created when combining the first letters of the words in the given sequence is: ", "")
                        res = res.replace("the sequence of letters created when you combine the second letters of the words in the given sequence is ", "")
                        res = res.replace("the sequence of letters is: ", "")
                        res = res.replace("the abbreviation created when you combine the first letters of the words in the given sequence is ", "")
                        res = res.replace("the abbreviation created when combining the first letters of the words in the given sequence is ", "")
                        res = res.replace("the first letters spell ", "")
                        res = res.replace("answer: ", "")
                        res = res.replace("the sequence of letters created is: ", "")
                        res = res.replace("the sequence of letters created when you combine the second letters of the words in the given sequence is: ", "")
                    
                        res = res.replace("\"", "")
                        res = res.replace(".", "")
                        res = res.replace("\n", "")
                        res = res.replace(", ", "")
                        res = res.replace(",", "")
                        res = res.replace("-", "")
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

                        if res == "PRIMATE REDRESS IGNOBLE MANATEE ANNULAR TAUNTED ERASINGTHEREFORETHE ANSWER IS: PRIMATEGRESSIMATATETE":
                            res = "PRIMATEGRESSIMATATETE"

                        if res == "I + N + S + W + E + S + T = INSWEST":
                            res = "INSWEST"


                        if res in manually_recognized_answers:
                            res = res.replace(" ", "")
                        elif len(res.split()) != 1:
                            print(res)
    

                        dist = distance(gt, res)
                        total_dist += dist
                        dists.append(dist)

                        if res == gt:
                            count_correct += 1
                            correct = "1"
                        else:
                            correct = "0"
                        #    print(res, gt)
                        count_total += 1

                        data = [str(index), condition, saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct]
                        fo.write("\t".join(data) + "\n")

                    print(condition + "_" + str(inner) + str(outer), "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))


