
import json
import jsonlines
from Levenshtein import distance


letters = "abcdefghijklmnopqrstuvwxyz'’"
def is_roman(word):
    for char in word:
        if char.lower() not in letters:
            return False

    return True



# Function for converting a sentence to Pig Latin or Boar Etruscan
def pig_encode(sentence, suffix="ay", vowel_consonant=""):
    words = sentence.lower().split()
    new_sentence = []
    for word in words:
        if word == "world-renowned":
            new_sentence.append("orld-renownedway")
            continue

        punct = ""
        while len(word) > 0 and word[-1] in [".", "?", "!", ",", ";", ":", "”", '"']:
            punct = word[-1] + punct
            word = word[:-1]

        prefix = ""
        while len(word) > 0 and word[0] in ["“", '"', "-"]:
            prefix = prefix + word[0]
            word = word[1:]

        if (not word.isalpha() or word[0] == "q") and not (word == "—" or word == "–"):

            usable = True
            for char in word:
                if char.isalpha() or char in ["'", "’", "“", "”"]:
                    continue
                else:
                    #print(word, char)
                    #print(sentence)
                    return "UNUSABLE"

        if word == "—" or word == "–":
            new_word = word
        elif len(word) > 0 and word[0] in ["a", "e", "i", "o", "u"]:
            if is_roman(word):
                new_word = prefix + word + vowel_consonant + suffix
            elif word == "eíthuv":
                new_word = "eíthuv" + suffix
            elif word == "ivésluv":
                new_word = "ivésluv" + suffix
            else:
                print("UNHANDLED WORD VOWEL-INITIAL", word)
                15/0

        elif len(word) > 0 and word[0] == "y":
            if is_roman(word):
                new_word = prefix + word[1:] + "y" + suffix
            else:
                #print("UNHANDLED WORD Y-INITIAL", word)
                15/0
        else:
            if is_roman(word):
                if len(word) > 0:
                    index_vowel = 0
                    no_vowel = False
                    while word[index_vowel] not in ["a", "e", "i", "o", "u", "y"]:
                        index_vowel += 1
                        if index_vowel == len(word):
                            no_vowel = True
                            break
                else:
                    no_vowel = True

                if no_vowel:
                    new_word = prefix + word + suffix
                else:
                    new_word = prefix + word[index_vowel:] + word[:index_vowel] + suffix
            elif word == "héthuv":
                new_word = "éthuvh" + suffix
            elif word == "ītsuv":
                new_word = "ītsuv" + suffix
            else:
                print("UNHANDLED WORD CONSONANT-INITIAL", word)
                15/0

        new_sentence.append(new_word + punct)

    return " ".join(new_sentence)




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


for task in ["enc", "dec"]:
    
    for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]:  
        
        fo = open("table_pig_boar_" + task + "_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "task", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        for variant in ["ay", "uv"]:
            condition = "pig" + task + "_" + variant + "_highprob"

            inputs = []
            with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
                for obj in reader:
                    inputs.append(obj["input"])
        
            fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            count_correct = 0
            count_total = 0
            for index, (inp, gt, res) in enumerate(zip(inputs, data["gts"], data["res"])):
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

                if gt.lower() in res.lower() or ("dec" in condition and pig_encode(gt.lower()) in pig_encode(res.lower())):
                    correct = "1"
                    count_correct += 1
                else:
                    correct = "0"
                count_total += 1


                if model.startswith("gpt"):
                    data = [str(index), variant, saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct]
                elif model == "llama-3-70b-chat-hf":
                    data = [str(index), variant, saved_stats[inp]["n_characters"], llama3_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], llama3_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct]
                elif model == "gemini-1.0-pro-001":
                    data = [str(index), variant, saved_stats[inp]["n_characters"], gemini_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], gemini_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct]
                elif model == "claude-3-opus-20240229":
                    data = [str(index), variant, saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct]
                else:
                    14/0
 
                fo.write("\t".join(data) + "\n")

            print(model, condition, count_correct*1.0/count_total)

            




