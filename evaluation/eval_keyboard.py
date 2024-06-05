
import json
from Levenshtein import distance
import re
import statistics 

# Function to decode from the keyboard cipher
row1 = "qwertyuiopq"
row2 = "asdfghjkla"
row3 = "zxcvbnmz"

encoding_dict = {}
for row in [row1, row2, row3]:
    prev = None
    for char in row:
        if prev is not None:
            encoding_dict[char] = prev
            encoding_dict[char.upper()] = prev.upper()
        prev = char

def keyboard_decode(sequence):
    new_sequence = []
    for char in sequence:
        if char in encoding_dict:
            new_sequence.append(encoding_dict[char])
        else:
            new_sequence.append(char)

    return "".join(new_sequence)



for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]: 
    print("")
    print(model)
    for condition in ["keyboardcot_highprob", "keyboardcotreference_highprob", "keyboardcotdetailed_highprob"]:
        
        fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
        data = json.load(fi)

        count_correct = 0
        count_total = 0
        total_dist = 0
        dists = []
        for gt, res in zip(data["gts"], data["res"]):
            if gt[0] == '"':
                gt = gt[1:]
            if gt[-1] == '"':
                gt = gt[:-1]

            #print(res)
            #print("")

            ends = [m.end() for m in re.finditer("Keyboard cipher:", res)]
            if len(ends) != 0:
                res = res[ends[-1]:].strip()

            ends = [m.end() for m in re.finditer("in the keyboard cipher is:", res)]
            if len(ends) != 0:
                res = res[ends[-1]:].strip()

            ends = [m.end() for m in re.finditer("Encoded message:", res)]
            if len(ends) != 0:
                res = res[ends[-1]:].strip()

            if len(res) > 0:
                if res[0] == '"':
                    res = res[1:]
            if len(res) > 0:
                if res[-1] == '"':
                    res = res[:-1]


            dist = distance(gt, res)
            total_dist += dist
            dists.append(dist)
            
            if gt in res:
                count_correct += 1
            else:
                if model == "gpt-4-0613" and len(gt) < 60: # and condition == "keyboardcotreference_highprob":
                    # Uncomment to see what models are doing
                    #print(keyboard_decode(gt))
                    #print(keyboard_decode(res))
                    #print("")
                    #print(keyboard_decode(gt))
                    #print(gt)
                    #print(res)
                    #print("")
                    pass
            count_total += 1

        print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, "median dist:", statistics.median(dists))
