
import json
import jsonlines
from Levenshtein import distance
import statistics
import re

alphabet = "abcdefghijklmnopqrstuvwxyz"
index2char = {}
char2index = {}
for index, char in enumerate(alphabet):
    index2char[index] = char
    char2index[char] = index

def rot_decode(sequence, n):
    new_sequence = []
    for char in sequence:
        if not char.isalpha():
            new_sequence.append(char)
        elif char.isupper():
            index = char2index[char.lower()]
            new_char = index2char[(index-n)%26]
            new_sequence.append(new_char.upper())
        else:
            index = char2index[char]
            new_char = index2char[(index-n)%26]
            new_sequence.append(new_char)

    return "".join(new_sequence)


fo = open("all_shift_examples_js.txt", "w")
fo.write("\nvar examples = {};\n")
example_index = 0
all_examples = []

end_after_strings = ["Original text: ", "message is:", "original text is:", "message is ", "we get:"]
delete_after_strings = ["However, this doesn't make sense", "However, this doesn't make much sense", "This sentence still doesn't make", "However, this sentence doesn't make", "This still doesn't make sense"]

prompt_conversion = {}
prompt_conversion["basic"] = "Basic"
prompt_conversion["step"] = "Step by step"
prompt_conversion["cot"] = "Chain of thought"

for task in ["dec", "enc"]:
    
    for shift in range(1,26):

        if task == "enc" and shift not in [2, 13]:
            continue

        for prob in ["highprob", "mediumprob", "lowprob", "adversarial"]:

            if prob != "highprob" and shift not in [2,13]:
                continue

            for prompt_style in ["basic", "step", "cot"]:
                if prob != "highprob" and prompt_style != "basic" and shift != 13:
                    continue

                if prob == "adversarial" and prompt_style != "basic":
                    continue

                res = {}

                if prob == "highprob" and task == "dec":
                    if prompt_style == "basic":
                        condition = "shift_" + str(shift)
                    else:
                        condition = "shift" + prompt_style + "_" + str(shift)
                else:
                    condition = "rot" + str(shift) + task + prompt_style.replace("basic", "") + "_" + prob

                for model in ["gpt-3.5-turbo-0613", "gpt-4-0613"]:
                    if model == "gpt-3.5-turbo-0613" and prompt_style != "basic":
                        res[model] = ["NOT AVAILABLE" for _ in range(100)]
                    else:
                        fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
                        data = json.load(fi)
                        res[model] = data["res"]
        
            
                inputs = []
                prompts = []
                with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
                    for obj in reader:
                        inputs.append(obj["input"])
                        prompts.append(obj["instruction_plus_input"])

                for index, (inp, gt, res_gpt35, res_gpt4, prompt) in enumerate(zip(inputs, data["gts"], res["gpt-3.5-turbo-0613"], res["gpt-4-0613"], prompts)):
                    
                        if gt[0] == '"':
                            gt = gt[1:]
                        if gt[-1] == '"':
                            gt = gt[:-1]

                        orig_res_gpt35 = res_gpt35[:]
                        orig_res_gpt4 = res_gpt4[:]

                        for delete_after_string in delete_after_strings:
                            if delete_after_string in res_gpt35:
                                starts = [m.start() for m in re.finditer(delete_after_string, res_gpt35)]
                                res_gpt35 = res_gpt35[:starts[0]].strip()
                        
                        for end_after_string in end_after_strings:
                            if end_after_string in res_gpt35:
                                ends = [m.end() for m in re.finditer(end_after_string, res_gpt35)]
                                res_gpt35 = res_gpt35[ends[-1]:].strip()
 
                        for delete_after_string in delete_after_strings:
                            if delete_after_string in res_gpt4:
                                starts = [m.start() for m in re.finditer(delete_after_string, res_gpt4)]
                                res_gpt4 = res_gpt4[:starts[0]].strip()
                        
                        for end_after_string in end_after_strings:
                            if end_after_string in res_gpt4:
                                ends = [m.end() for m in re.finditer(end_after_string, res_gpt4)]
                                res_gpt4 = res_gpt4[ends[-1]:].strip()
 
                        if res_gpt35[0] == '"':
                            res_gpt35 = res_gpt35[1:]
                        if res_gpt35[-1] == '"':
                            res_gpt35 = res_gpt35[:-1]

                        if res_gpt4[0] == '"':
                            res_gpt4 = res_gpt4[1:]
                        if res_gpt4[-1] == '"':
                            res_gpt4 = res_gpt4[:-1]


                        if task == "enc":
                            gpt35_dec_res = rot_decode(res_gpt35, shift)
                            gpt4_dec_res = rot_decode(res_gpt4, shift)
                        else:
                            gpt35_dec_res = "NOT APPLICABLE"
                            gpt4_dec_res = "NOT APPLICABLE"


                        example_text = 'examples[' + str(example_index+1)
                        example_text = example_text + '] = {index:"' + str(index+1) + '", shift:"' 
                        example_text = example_text + str(shift) + '", inp:"' + inp.replace('"', '\\"') 
                        example_text = example_text + '", correct:"' + gt.replace('"', '\\"') + '", gpt35:"' 
                        example_text = example_text + res_gpt35.replace('"', '\\"').replace("\n", "<br>") + '", gpt4:"' + res_gpt4.replace('"', '\\"').replace("\n", "<br>")
                        example_text = example_text + '", prompt:"' + prompt_conversion[prompt_style] + '", full_prompt:"' + prompt.replace('"', '\\"').replace("\n", "<br>")
                        example_text = example_text + '", probability:"' + prob.replace("prob", "") + '", task:"' + task + 'oding", decoded4:"' + gpt4_dec_res.replace('"', '\\"').replace("\n", "<br>") + '", decoded35:"' + gpt35_dec_res.replace('"', '\\"').replace("\n", "<br>") + '", orig_gpt35:"' + orig_res_gpt35.replace('"', '\\"').replace("\n", "<br>") + '", orig_gpt4:"' + orig_res_gpt4.replace('"', '\\"').replace("\n", "<br>") + '"};\n'

                        fo.write(example_text)
                        example_index += 1


            




