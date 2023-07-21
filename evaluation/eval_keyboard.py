
import json
from Levenshtein import distance

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



for model in ["gpt-3.5-turbo", "gpt-4"]:
    print("")
    print(model)
    for condition in ["keyboard_highprob", "keyboard_lowprob", "keyboard_random"]:
        
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

            if res[0] == '"':
                res = res[1:]
            if res[-1] == '"':
                res = res[:-1]

            dist = distance(gt, res)
            total_dist += dist
            
            if gt == res:
                count_correct += 1
            else:
                # Uncomment to see what models are doing
                #print(keyboard_decode(gt))
                #print(keyboard_decode(res))
                #print("")
                pass
            count_total += 1

        print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total)
