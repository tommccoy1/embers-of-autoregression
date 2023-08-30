
import json
import jsonlines
from Levenshtein import distance
import statistics
import math

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


number_logfreq = {}
numbers_str = {}
total = 0
for i in range(1,101):
    numbers_str[str(i)] = 1
    number_logfreq[i] = 0
fi = open("../corpus_analysis/numbers.txt", "r")
for line in fi:
    parts = line.strip().split()
    word = parts[0]
    count = int(parts[1])
    if word in numbers_str:
        number_logfreq[int(word)] = count
        total += count


for number in number_logfreq:
    number_logfreq[number] = math.log(number_logfreq[number]*1.0/total)

number_by_logfreq = []
for number in number_logfreq:
    number_by_logfreq.append([number, number_logfreq[number]])
sorted_by_logfreq = sorted(number_by_logfreq, key=lambda x: -1*x[1])
with_ranks = [[index+1, pair[0]] for index, pair in enumerate(sorted_by_logfreq)]
new_ranked = sorted(with_ranks, key=lambda x: x[1])
new_ranked = [x[0] for x in new_ranked]


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


manually_specified = {}
manually_specified["the question does not provide a list to count the number of top hat emojis."] = 0
manually_specified["the list provided only contains one thumbs up emoji."] = 1
manually_specified["the list provided does not contain any emojis."] = 0
manually_specified["the list provided does not show any emojis. please provide a list."] = 0
manually_specified["the list provided does not contain any chick emojis. it only contains one hatching chick emoji."] = 1
manually_specified["the list does not contain any chick emojis."] = 0


for model in ["gpt-3.5-turbo", "gpt-4"]:
    for condition in ["counting_words", "counting_chars"]:
        print("")
        print(model)

        fo = open("table_" + condition + "_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        fo_both = open("table_" + condition + "_both_" + model + ".tsv", "w")
        fo_both.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        for inner in ["common", "rare"]:
            count_by_number = {}


            inputs = []
            with jsonlines.open("../stimuli/" + condition + "_" + str(inner) + ".jsonl") as reader:
                for obj in reader:
                    inputs.append(obj["input"])

            fi = open("../logs/" + condition + "_" + inner + "_" +  model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)


            dists = []
            count_correct = 0
            count_total = 0
            total_dist = 0
            for inp, gt, res in zip(inputs, data["gts"], data["res"]):
                if gt[0] == '"':
                    gt = gt[1:]
                if gt[-1] == '"':
                    gt = gt[:-1]

                if res[0] == '"':
                    res = res[1:]
                if res[-1] == '"':
                    res = res[:-1]

                res = res.lower()
                res = res.replace(" letters.", "")
                words = res.split()


                answer = None
                if words[0] == "there" and words[1] == "are" and (words[3] == "words" or words[3] == "letters" or words[4] == "emojis" or words[5] == "emojis"):
                    res = words[2]
                    if res in t2n:
                        answer = t2n[res]
                    elif res.isnumeric():
                        answer = int(res)
                    elif res == "no":
                        answer = 0
                
 
                elif res.isnumeric():
                    answer = int(res)

                elif res.startswith("there is only one") or res.startswith("there is only 1 "):
                    answer = 1

                elif res.startswith("the list provided only contains one"):
                    answer = 1

                elif len(words) >= 4 and (words[0] == "there" and words[1] == "is" and (words[3] == "letter" or words[3] == "word")):
                    if words[2] in t2n:
                        answer = t2n[words[2]]
                    else:
                        answer = int(words[2])

                elif len(words) >= 5 and (words[0] == "there" and words[1] == "is" and (words[4] == "emoji" or words[5] == "emoji")):
                    if words[2] in t2n:
                        answer = t2n[words[2]]
                    else:
                        answer = int(words[2])

                elif len(words) >= 5 and (words[0] == "the" and words[1] == "list" and words[3] == "contains"):
                    if words[4] in t2n:
                        answer = t2n[words[4]]
                    else:
                        answer = int(words[4])

                elif len(words) >= 4 and (words[0] == "the" and words[1] == "list" and words[2] == "contains"):
                    if words[3] in t2n:
                        answer = t2n[words[3]]
                    else:
                        answer = int(words[3])


               
                elif res in manually_specified:
                    answer = manually_specified[res]

                gt = int(gt)
                
                if answer is None:
                    print(res)

                dist = abs(answer - gt)
                total_dist += dist
                dists.append(dist)

                if answer == gt:
                    count_correct += 1
                count_total += 1

                if gt not in count_by_number:
                    count_by_number[gt] = [0,0]

                if answer == gt:
                    count_by_number[gt][0] += 1
                    correct = "1"
                else:
                    correct = "0"
                count_by_number[gt][1] += 1

                #if count_by_number[gt][1] < 10:
                #    print(model, condition, inner, gt, res)


                if inner == "common":
                    data = [str(gt), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                                            saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct] 
                    fo.write("\t".join(data) + "\n")

                data = [str(gt), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                        saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct]
                fo_both.write("\t".join(data) + "\n")


               
            print(condition + "_" + inner, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
            
            accs_by_number = []
            for number in count_by_number:
                accs_by_number.append(count_by_number[number][0]*1.0/count_by_number[number][1])
            output_str = ",".join([str(x) for x in accs_by_number])
            print(output_str)
            print("")
            #print(number, count_by_number[number][0]*1.0/count_by_number[number][1])


print("NUMBER LOG FREQUENCIES:")
freqs = []
for i in range(1,101):
    freqs.append(number_logfreq[i])
print(",".join([str(x) for x in freqs]))

print(new_ranked)
