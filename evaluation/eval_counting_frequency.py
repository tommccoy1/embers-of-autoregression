
import json
import jsonlines
from Levenshtein import distance
import statistics
import re
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

gemini_tokens = {}
fi = open("../stimuli/saved_gemini_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    gemini_tokens[parts[0]] = parts[1]

llama3_tokens = {}
fi = open("../stimuli/saved_llama3_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    llama3_tokens[parts[0]] = parts[1]



number_logfreq = {}
total = 0
fi = open("../corpus_analysis/numbers.txt", "r")
for line in fi:
    parts = line.strip().split()
    number = int(parts[0])
    count = int(parts[1])
    total += count

    number_logfreq[number] = count

for number in number_logfreq:
    number_logfreq[number] = math.log(number_logfreq[number]*1.0/total)




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


manually_recognized_answers = {}
manually_recognized_answers["100 letters."] = 100

end_after_strings = ["the correct answer is ", "answer: ", "the list you provided contains ", " i lost count after ", "i know there are ", "the list contains ", "i'm not sure, but it's definitely more than ", "there are ", "i know the list has ", "i tried to count them and i got ", "but it returns ", "i am not sure if the answer is ", "ans: ", "but i am getting ", "appears ", "i have a list of ", "the list has ", "i have tried to count them and i get ", "the answer is ", "the words in the list are:", "i have found ", "i count ", "i can count ", "this list contains ", "this is a list of ", "your list contains ", "i have counted ", "i have ", "if you count the words in the list you will get ", "i've counted ", "the following is a list of words:", "the number of words in the list is "]
delete_after_strings = []

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

unfinished = 0
for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]: 
    for condition in ["counting_words", "counting_chars"]:
        print("")
        print(model)

        fo = open("table_" + condition + "_binary_" + model + ".tsv", "w")
        fo_input = open("table_" + condition + "_binary_input_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")
        fo_input.write("\t".join(["index", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        for inner in ["common_common", "common_rare", "rare_common", "rare_rare"]:

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

                if len(res) > 0:
                    if res[0] == '"':
                        res = res[1:]
                if len(res) > 0:
                    if res[-1] == '"':
                        res = res[:-1]

                res = res.lower()
                words = res.split()

                answer = None
                if len(words) > 5 and words[0] == "there" and words[1] == "are" and (words[3] == "words" or words[3] == "letters" or words[4] == "emojis" or words[5] == "emojis"):
                    res = words[2]
                    if res in t2n:
                        answer = t2n[res]
                    elif res.isnumeric():
                        answer = int(res)
                elif len(words) > 5 and words[0] == "the" and words[1] == "list" and words[2] == "contains" and (words[4] == "letters." or words[5] == "emojis." or words[5] == "letters." or (len(words) >= 7 and words[6] == "emojis.")):
                    answer = int(words[3])
                elif res.startswith("there is only one word"):
                    answer = 1
                elif res.isnumeric():
                    answer = int(res)
                elif res in manually_recognized_answers:
                    answer = manually_recognized_answers[res]

                gt = int(gt)

                unique_numbers = find_unique_number(res)
                if len(unique_numbers) == 1:
                    answer = unique_numbers[0]
                elif len(unique_numbers) == 0:
                    answer = 0

                if gt not in unique_numbers:
                    answer = 0
 
                for delete_after_string in delete_after_strings:
                    if delete_after_string in res:
                        starts = [m.start() for m in re.finditer(delete_after_string, res)]
                        res = res[:starts[0]].strip()

                for end_after_string in end_after_strings:
                    if end_after_string in res:
                        ends = [m.end() for m in re.finditer(end_after_string, res)]
                        
                        try:
                            res = res[ends[-1]:].strip()
                            number = int(res.split()[0])
                            res = res.split()[0]
                        except:
                            pass

                # If the first word is a number, we say that's the answer
                try:
                    first_word = res.strip().split()[0]
                    if first_word[-1] == "." or first_word[-1] == ",":
                        first_word = first_word[:-1]
                    number = int(first_word.strip())
                    res = first_word
                except:
                    pass


                unique_numbers = find_unique_number(res)
                if len(unique_numbers) == 1:
                    answer = unique_numbers[0]
                elif len(unique_numbers) == 0:
                    answer = 0
 
              
                if res.strip().startswith("a)") or res.strip().startswith("a. "):
                    answer = 0


                if answer is None:
                    print("ANSWER", res)
                    answer = 0
                    unfinished += 1

                dist = abs(answer - gt)
                total_dist += dist
                dists.append(dist)

                if answer == gt:
                    count_correct += 1
                    correct = "1"
                else:
                    correct = "0"

                if gt == 20 and inner == "common_common" and condition == "counting_words" and model == "gpt-4":
                    #print(inp)
                    #print(gt)
                    #print(res)
                    #print("")
                    pass
                count_total += 1

                if inner.endswith("common"):

                    if model.startswith("gpt"):
                        data = [str(gt), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    elif model == "llama-3-70b-chat-hf":
                        data = [str(gt), saved_stats[inp]["n_characters"], llama3_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], llama3_tokens[str(gt)], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    elif model == "gemini-1.0-pro-001":
                        data = [str(gt), saved_stats[inp]["n_characters"], gemini_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], gemini_tokens[str(gt)], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    elif model == "claude-3-opus-20240229":
                        data = [str(gt), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    else:
                        14/0
                    
                    fo.write("\t".join(data) + "\n")


                if inner.startswith("common"):

                    if model.startswith("gpt"):
                        data = [str(gt), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    elif model == "llama-3-70b-chat-hf":
                        data = [str(gt), saved_stats[inp]["n_characters"], llama3_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], llama3_tokens[str(gt)], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    elif model == "gemini-1.0-pro-001":
                        data = [str(gt), saved_stats[inp]["n_characters"], gemini_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], gemini_tokens[str(gt)], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    elif model == "claude-3-opus-20240229":
                        data = [str(gt), saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                                saved_stats[str(gt)]["n_characters"], saved_stats[str(gt)]["n_gpt4_tokens"], saved_stats[str(gt)]["gpt2_logprob"], correct]
                    else:
                        14/0
 
                    fo_input.write("\t".join(data) + "\n")

                #print(gt, answer)
                
            print(condition + "_" + inner, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))
            

print(unfinished)
