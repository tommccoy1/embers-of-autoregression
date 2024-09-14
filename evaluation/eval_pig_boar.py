
import json
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


for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]:
    print("")
    print(model)
    for suffix in ["ay", "uv"]:
        print("")
        for condition in ["pigdec_" + suffix + "_highprob", "pigdec_" + suffix + "_mediumprob", "pigdec_" + suffix + "_lowprob", "pigenc_" + suffix + "_highprob", "pigenc_" + suffix + "_mediumprob", "pigenc_" + suffix + "_lowprob"]:
       
            if suffix == "uv" and ("medium" in condition or "low" in condition):
                continue

            fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            count_correct = 0
            count_total = 0
            total_dist = 0
            for gt, res in zip(data["gts"], data["res"]):
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
                dist = distance(gt, res)
                total_dist += dist
            
                # If decoding, allow for nondeterminism (multiple possible answers)
                if gt.lower() in res.lower() or ("dec" in condition and pig_encode(gt.lower()) in pig_encode(res.lower())):
                    count_correct += 1
                    #if model == "gpt-4-0613" and "dec_ay_highprob" in condition and len(gt) < 80:
                    #    print(gt)
                    #    print(res)
                    #    print("")
                else:
                    if model == "gpt-4-0613" and "dec_ay_mediumprob" in condition: # and len(gt) < 90 and distance(gt.split(), res.split()) > 1:
                        #print(gt)
                        #print(res)
                        #print("")
                        pass

                    if "claude" in model and "dec" in condition:
                        #print(gt)
                        #print(res)
                        #print("\n\n\n")
                        pass

                    if model == "gpt-4":
                        if ("yay" in res and "yay" not in gt) or ("way" in res and "way" not in gt):
                            pass
                            #print(gt)
                            #print(res)
                            #print("")
                count_total += 1

                if len(gt) < 50 and "dec_ay_highprob" in condition and gt == res:
                    #print(gt)
                    #print(res)
                    #print("")
                    pass

            print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total)
