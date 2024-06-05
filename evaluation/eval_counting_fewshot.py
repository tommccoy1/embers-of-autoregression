
import json
import jsonlines
from Levenshtein import distance
import re
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


palm_tokens = {}
fi = open("../stimuli/saved_palm_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    palm_tokens[parts[0]] = parts[1]

llama_tokens = {}
fi = open("../stimuli/saved_llama_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    llama_tokens[parts[0]] = parts[1]


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
manually_specified["the list provided does not contain any emojis, so the answer is 0."] = 0
manually_specified["the list does not provide any angry face emojis to count."] = 0
manually_specified["the list provided does not show any emojis. please provide a list for evaluation."] = 0
manually_specified["the list provided does not show any emojis. please provide a list."] = 0
manually_specified["the list provided does not contain any chick emojis. it only contains one hatching chick emoji."] = 1
manually_specified["the list does not contain any chick emojis."] = 0
manually_specified["a 10 b 15 c 20 d 25"] = 0
manually_specified["2016/11/19 00:00:00 |  | 1"] = 0
manually_specified["only one letter, \"j\", repeated 2"] = 1
manually_specified["i'm not sure about this one i'm thinking there are 26 letters in the list,"] = 26
manually_specified["i've tried using the `strlen()` function, but it returns 16 instead of 26"] = 16
manually_specified["i got the answer as 40 but the correct answer is 28 can someone explain why?"] = 40
manually_specified["i tried to count them and i got 22 letters but the answer i'm looking for is 2"] = 22
manually_specified["i would say 27, but the answer i was given is 28\n\ni'm"] = 27
manually_specified["20 letters: 19 'p's and 1 's'"] = 20
manually_specified["32\n\ncomment: yes, you are correct! there are 3"] = 32
manually_specified["15 letters in this list: 14 \"i\"s and 1"] = 15
manually_specified["17 letters in the list, but the answer i'm given is 2"] = 17
manually_specified["11 letters: 10 '"] = 11
manually_specified["i would say that there are 20 letters in the list, but the actual answer is 21"] = 20
manually_specified["i would say 13, but that is not one of the choices\n\nthe choices are:"] = 13
manually_specified["20 letters: 19 r's and 1 s"] = 20
manually_specified["11\n\nexplanation: there are 11 letters in the list: 1"] = 11
manually_specified["2632\n2560"] = 2632
manually_specified["10 letters: 9 w"] = 10
manually_specified["i can do this!\n\nthere are 11 letters in the list: 10 a's"] = 11
manually_specified["the correct answer is 10 each letter in the list is a \"p\", so there are 1"] = 10
manually_specified["10 letters: 9 \"u"] = 10
manually_specified["i don't think it's 10, because there are two 'k's in the list"] = 0
manually_specified["i am not sure how to count the letters in this list is it 10 letters, 20"] = 0
manually_specified["11 letters (10 \"s\"s and 1 space)"] = 11
manually_specified["10 letters: 9"] = 10
manually_specified["9 letters in the list, but the answer i'm looking for is 1"] = 9
manually_specified["i'm having trouble with this one i know there are 8 \"l\"s in the word,"] = 8
manually_specified["7\n\nexplanation: there are 7 letters in the list: 6 \"l"] = 7
manually_specified["[a] 7\n[b] 8\n[c] 9\n[d] 1"] = 0
manually_specified["i would say 6, but the answer key says 5 why?\n\ni would appreciate it if"] = 6
manually_specified["i would say that there are 6 letters in the list: 5 a's and 1 space"] = 6
manually_specified["i am having trouble determining if this is 1 letter or 5\n\nanswer:"] = 5
manually_specified["5 how many letters are in the following list? \"zzzzz\"\n6 how many letters are in"] = 0
manually_specified["i would say 4, but the program i'm using says 1 how can this be?"] = 4
manually_specified["pp\" \"pp\" \"p\"\n\ni would say 4 letters, but the answer key says 3"] = 4




end_after_strings = ["the list contains", "the number of words in the list is ", "i have counted the words in the list and there are ", "the number of words in the list you provided is ", "the answer is ", "this is a list of ", "the answer to your question is ", "answer:\n\nthere are ", "answer: ", "i would expect the answer to be ", "i'm thinking it's ", "i think there are ", "the list has ", "i would say there are "] 
delete_after_strings = ["here's the list", "the words in the list are:", "the following is a list of words", "\n1", "words, not", "\na ", "\na:", "are not in the list", "asked by khansam13 10 iminy"] 


def find_unique_number(answer):
    words = answer.replace(".", "").replace(",", "").replace(":", "").split()
    numbers = []
    for word in words:
        if word.isnumeric():
            numbers.append(int(word))
        elif word in t2n:
            numbers.append(t2n[word])

    numbers = list(set(numbers))
    return numbers



number_counts_0shot = {}
number_counts_5shot = {}
number_counts_10shot = {}
number_counts_100shot = {}

for i in range(101):
    number_counts_0shot[i] = 0
    number_counts_5shot[i] = 0
    number_counts_10shot[i] = 0
    number_counts_100shot[i] = 0

for count, count_dict in [("5", number_counts_5shot), ("10", number_counts_10shot), ("100", number_counts_100shot)]:
    fi = open("../examples/counting_words_" + count + "shot.txt", "r")

    for line in fi:
        length = len(line.strip().split())
        count_dict[length] += 1

    fi.close()


unfinished = 0
for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "claude-3-opus-20240229", "ft:gpt-3.5-turbo-0613:personal:count-10shot:9NYCyc4X", "ft:gpt-3.5-turbo-0613:personal:count-100shot:9NYN8hZQ"]:
    for condition in ["counting_words", "counting_words_5shot", "counting_words_10shot"]:
    #for condition in ["counting_words"]:

        if model.startswith("ft"):
            if condition != "counting_words":
                continue
        #    elif "10shot" in model:
        #        condition = "counting_words_10shot"
        #    elif "100shot" in model:
        #        condition = "counting_words_100shot"
        #    model = "ft-gpt-3.5-turbo-0613"

        n_examples = None
        count_dict = None
        if model.startswith("ft"):
            if "10shot" in model:
                n_examples = 10
                count_dict = number_counts_10shot
            elif "100shot" in model:
                n_examples = 100
                count_dict = number_counts_100shot
        elif condition == "counting_words_5shot":
            n_examples = 5
            count_dict = number_counts_5shot
        elif condition == "counting_words_10shot":
            n_examples = 10
            count_dict = number_counts_10shot
        else:
            n_examples = 0
            count_dict = number_counts_0shot

        print("")
        print(model)

        fo = open("table_few_" + condition + "_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "demonstration_count", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        for inner in ["common"]:
            count_by_number = {}


            inputs = []
            with jsonlines.open("../stimuli/" + condition.replace("words", "words" + "_" + str(inner)) + ".jsonl") as reader:
                for obj in reader:
                    inputs.append(obj["input"])

    
            fi = open("../logs/" + condition.replace("words", "words" + "_" + str(inner)) + "_" +  model + "_temp=0.0_n=1.json", "r")
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

                if len(res) > 0:
                    if res[0] == '"':
                        res = res[1:]
                if len(res) > 0:
                    if res[-1] == '"':
                        res = res[:-1]

                res = res.lower()
                res = res.replace(" letters.", "")
                res = res.replace(".", "")

                for delete_after_string in delete_after_strings:
                    if delete_after_string in res:
                        starts = [m.start() for m in re.finditer(delete_after_string, res)]
                        res = res[:starts[0]].strip()
                        
                for end_after_string in end_after_strings:
                    if end_after_string in res:
                        ends = [m.end() for m in re.finditer(end_after_string, res)]
                        res = res[ends[-1]:].strip()
 
                words = res.split()


                answer = None
                if len(words) > 5 and words[0] == "there" and words[1] == "are" and (words[3] == "words" or words[3] == "letters" or words[4] == "emojis" or words[5] == "emojis"):
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
                        if words[2] == "no":
                            answer = 0
                        else:
                            answer = int(words[2])

                elif len(words) >= 5 and (words[0] == "the" and words[1] == "list" and words[3] == "contains"):
                    if words[4] in t2n:
                        answer = t2n[words[4]]
                    else:
                        if words[4] != "only":
                            answer = int(words[4])
                        else:
                            if words[5] in t2n:
                                answer = t2n[words[5]]
                            else:
                                answer = int(words[5])

                elif len(words) >= 4 and (words[0] == "the" and words[1] == "list" and words[2] == "contains"):
                    if words[3] in t2n:
                        answer = t2n[words[3]]
                    else:
                        answer = int(words[3])

                elif res.strip().startswith("i'm not sure how"):
                    answer = 0

                elif res.strip().startswith("there are a total of"):
                    answer = int(res.strip().split()[5])

                elif res.strip().startswith("this list contains"):
                    answer = int(res.strip().split()[3])

                elif res.strip().startswith("i have the answer as"):
                    answer = int(res.strip().split()[5].replace(",", "").replace(".", ""))

                elif len(res.split()) > 3 and (res.strip().startswith("i count") and res.strip().split()[3] == "words"):
                    answer = int(res.strip().split()[2].replace(",", "").replace(".", ""))

                elif res.strip().startswith("i have tried to count the words, but"):
                    answer = 0

                elif res.strip().startswith("this is a list of") and len(res.strip().split()) > 6 and res.strip().split()[6]in ["words", "words."]:
                    answer = int(res.strip().split()[5].replace(",", "").replace(".", ""))
               
                elif res.strip() in manually_specified:
                    answer = manually_specified[res.strip()]

                elif "a)" in res:
                    answer = 0

                if "words" in res:
                    split_res = res.replace("words.", "words").replace("words:", "words").split()
                    if "words" in split_res:
                        index_words = split_res.index("words")
                        index_num = index_words - 1

                        try:
                            answer = int(split_res[index_num])
                        except:
                            pass
                
                unique_numbers = find_unique_number(res)
                if len(unique_numbers) == 1:
                    answer = unique_numbers[0]
                elif len(unique_numbers) == 0:
                    answer = 0
                elif int(gt) not in unique_numbers:
                    # If correct answer isn't there, we don't need
                    # to check it
                    answer = 0

                gt = int(gt)
              
                if res.strip().startswith("i would say 6\n"):
                    answer = 6
                if res.strip().startswith("the answer is: 4\n"):
                    answer = 4
                if res.startswith("3\n4\n"):
                    answer = 3
                if res.startswith("50 thumbs up emojis"):
                    answer = 50
                if res.startswith("10 there are"):
                    answer = 10
                if res.strip().startswith("what is the sum of 3 and 5?"):
                    answer = 0
                if len(res.split()) > 2:
                    words = res.split()
                    if words[1] == "there" and words[2] in ["is", "are"]:
                        try:
                            answer = int(words[0])
                        except:
                            pass
                if res.strip() == "what is the sum of 2 + 3 + 4 + 5 + 6?":
                    answer = 0
                if res.startswith("26 letters"):
                    answer = 26
                if res.startswith("27 letters"):
                    answer = 27
                if res.strip().startswith("i would say 26,"):
                    answer = 26
                if res.strip().startswith("answer: 26"):
                    answer = 26
                if res.strip().startswith("* 1\n* 2\n* 3\n* 4\n* 5\n\n"):
                    answer = 0
                if res.startswith("1, because"):
                    answer = 1
                if res.strip().startswith("i tried to count the letters and i got 42,"):
                    answer = 42
                if res.strip().startswith("42 however, the answer provided by the website says 26"):
                    answer = 42
                words = res.split()
                if len(words) > 0:
                    if words[0].endswith(","):
                        try:
                            answer = int(words[0][:-1])
                        except:
                            pass
                if res.strip().startswith("i would say 1,"):
                    answer = 1
                if res.strip().startswith("the list has 26"):
                    answer = 26
                if "consists of 4 quarters" in res:
                    answer = 4
                if "contains 6 it is a sequence of" in res:
                    answer = 6
                if "there are a total of 10 letters" in res:
                    answer = 10
                if 'contains 22 "z" letters' in res:
                    answer = 22
                if "there are 2 chick emojis" in res:
                    answer = 2
                if "is one of the basic seven pronominal adjectives" in res:
                    answer = 7
                if "contains 13 words" in res:
                    answer = 2
                if res.startswith('the word "gullible" occurs 2 times'):
                    answer = 2
                if "is the only one of the three in the given list" in res:
                    answer = 3
                if "the number of words in the given list is 9" in res:
                    answer = 9
                if 'the number of words in the list "kingfishers" is 6' in res:
                    answer = 6
                if 'the word "intermingle" appears 2 times and' in res:
                    answer = 2
                if 'the word "keywords" is two words' in res:
                    answer = 2
                if 'the number of words in the given list is 14' in res:
                    answer = 14

                if answer is None:
                    print("ANSWER", res)
                    16/0
                    answer = 0
                    unfinished += 1

                dist = abs(answer - gt)
                total_dist += dist
                dists.append(dist)

                if answer == gt:
                    count_correct += 1
                count_total += 1

                if gt not in count_by_number:
                    count_by_number[gt] = [0,0]

                #print(answer, gt)
                if answer == gt:
                    count_by_number[gt][0] += 1
                    correct = "1"
                    if model == "gpt-4-0613" and gt == 30 and condition == "counting_chars" and len(inp) < 300:
                        #print(inp)
                        #print(gt)
                        #print(answer)
                        #print("")
                        pass
                else:
                    correct = "0"
                    if model == "gpt-4-0613" and gt == 29 and condition == "counting_chars" and len(inp) < 300:
                        #print(inp)
                        #print(gt)
                        #print(answer)
                        #print("")
                        pass
                count_by_number[gt][1] += 1

                #if count_by_number[gt][1] < 10:
                #    print(model, condition, inner, gt, res)


                if inner == "common":

                    if "gpt" in model:
                        data = [str(gt), str(count_dict[gt]), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"], 
                                saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    elif model == "claude-3-opus-20240229":
                        data = [str(gt), str(count_dict[gt]), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    else:
                        #pass
                        14/0
 
                    fo.write("\t".join(data) + "\n")

            print(condition + "_" + inner, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
            
            accs_by_number = []
            for number in count_by_number:
                #print(number, count_by_number[number][0]*1.0/count_by_number[number][1])
                accs_by_number.append(count_by_number[number][0]*1.0/count_by_number[number][1])
            output_str = ",".join([str(x) for x in accs_by_number])
            print(output_str)
            print("")
            #print(number, count_by_number[number][0]*1.0/count_by_number[number][1])



print(unfinished)
