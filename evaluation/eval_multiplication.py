
import json
import jsonlines
from Levenshtein import distance
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

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



for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-3-70b-chat-hf", "claude-3-opus-20240229", "gemini-1.0-pro-001"]: 
    print("")
    print(model)

    fo = open("table_multiplication_" + model + ".tsv", "w")
    fo.write("\t".join(["index", "method", "correct"]) + "\n")

    for condition in ["multiplication_number", "multiplication_word", "multiplication_allcaps", "multiplication_alternatingcaps"]: 

       
        inputs = []
        with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
            for obj in reader:
                inputs.append(obj["input"])

        fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
        data = json.load(fi)

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

            res_words = res.split()
            res = res_words[-1].replace(",", "")
            res = res.replace(".", "")

            dist = distance(gt, res)
            total_dist += dist
           
            if gt == "226860" and model == "gpt-4-0613":
                #print(inp)
                #print(gt)
                #print(res)
                #print("")
                pass

            if gt in res:
                count_correct += 1
                correct = "1"
            else:
                correct = "0"

                #if condition == "multiplication_number":
                    #print(inp)
                    #print(gt)
                    #print(res)
                    #print("")

                if "claude" in model:
                    #print(gt)
                    #print(res)
                    #print("\n\n\n")
                    pass

                try:
                    value = int(res)
                except:
                    pass
                    #print(res)
                    #if condition == "multiplication_number":
                        #print(inp)
                        #print(gt)
                        #print(res)
                        #print("")
            count_total += 1

            nchars_input = len(inp)
            ntokens_input = len(enc.encode(inp))
            data = [str(index), condition, correct]
            fo.write("\t".join(data) + "\n")

        print(condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total)
