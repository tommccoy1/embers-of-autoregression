import logging
import json
import argparse
from tqdm import tqdm
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import time
logging.getLogger().setLevel(logging.ERROR)

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])



def edit_distance(s1: str, s2: str) -> int:
    """Compute the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

my_safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }


def gemini_responses(prompt_list, model="gemini-1.0-pro-001", max_tokens=1000, temperature=0.0):
    responses = []
    my_generation_config = genai.GenerationConfig(temperature=temperature, max_output_tokens=max_tokens)
    model_to_call = genai.GenerativeModel(model, safety_settings=my_safety_settings, generation_config=my_generation_config)
    for prompt in tqdm(prompt_list):
        output = None
        for repeat in range(15):
            try:
                completion = model_to_call.generate_content(prompt)
                #print(completion)
                output = completion.text
                if output is None:
                    output = ""
            except Exception as e:
                string_exception = str(e)
                if "but none was returned" in string_exception: 
                    output = ""
                else:
                    print("WAITING", repeat, string_exception)
                    if repeat < 5:
                        time.sleep(10)
                    else:
                        time.sleep(180)
            
            if not (output is None):
                break

        if output is None:
            output = ""
        responses.append(output)
    return responses

    


def solve_file(name, model, temperature, max_tokens):
    file = f'./stimuli/{name}.jsonl'
    if not os.path.exists(file):
        print(f'File {file} does not exist')
        return None
    with open(file, 'r') as f:
        lines = f.readlines()
    lines = [json.loads(line) for line in lines]
    prompts = [line['instruction_plus_input'] for line in lines]
    gts = [line['correct_output'] for line in lines]
    
    # Using max_tokens = None because otherwise we get no response
    res = gemini_responses(prompts, model=model, temperature=0.0, max_tokens=None)

    # These accs are not what we use in the paper - they're just for quick estimates. 
    # The stats used in the paper are computed in the evaluation/ folder
    accs = [(gt.replace('"', "") in r.replace('"', "")) for r, gt in zip(res, gts)]
    eds = [edit_distance(r, gt) for r, gt in zip(res, gts)]
    acc = sum(accs) / len(accs)
    ed = sum(eds) / len(eds)
    # print(f'Accuracy: {acc}', f'Edit distance: {ed}')

    d = {'prompts': prompts, 'gts': gts, 'res': res, 'accs': accs, 'acc': acc, 'eds': eds, 'ed': ed}

    output_file = f'./logs/{name}_{model}_temp={temperature}_n=1.json'
    with open(output_file, 'w') as f:
        json.dump(d, f)
    
    return d


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--tasks', type=str, required=True, help='split by comma')
    args.add_argument('--conditions', type=str, required=True, help='split by comma')
    args.add_argument('--model', type=str, required=True, choices=['gemini-1.0-pro-001'])
    args.add_argument('--max_tokens', type=int, help='default = 1000', default=1000)
    args = args.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    tasks = args.tasks.split(',')
    conditions = args.conditions.split(',')
    model = args.model
    max_tokens = args.max_tokens

    for task in tasks:
        for condition in conditions:
            name = f'{task}_{condition}'
            d = solve_file(name, model=model, temperature=0.0, max_tokens=max_tokens)
            if d is not None:
                print(f'{name}, {model}: {d["acc"]:.2f} ({d["ed"]:.2f})')

