import logging
import json
import argparse
from tqdm import tqdm
import os
import together
import time
logging.getLogger().setLevel(logging.ERROR)

together.api_key = os.environ['TOGETHER_API_KEY']
client = together.Together(api_key=together.api_key)

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


def llama_responses(prompt_list, model="llama-3-70b-chat-hf", max_tokens=1000, temperature=0.0):
    responses = []
    for prompt in tqdm(prompt_list):
        output = None
        for _ in range(10):
            try:
                if "chat" in model:
                    output = client.chat.completions.create(
                                messages = [{"role": "user", "content": prompt}], 
                                model = "meta-llama/" + model,
                                max_tokens = max_tokens,
                                temperature = temperature,
                            )
                else:
                    output = client.completions.create(
                                prompt=prompt,
                                model = "meta-llama/" + model,
                                max_tokens = max_tokens,
                                temperature = temperature,
                            )
            except:
                time.sleep(1)
            
            if not (output is None):
                break

        if "chat" in model:
            responses.append(output.choices[0].message.content)
        else:
            responses.append(output.choices[0].text)
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
    res = llama_responses(prompts, model=model, temperature=0.0, max_tokens=max_tokens)

    # These accs are not what we use in the paper - they're just for quick estimates. 
    # The stats used in the paper are computed in the evaluation/ folder
    accs = [(gt.replace('"', '') in r.replace('"', '')) for r, gt in zip(res, gts)]
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
    args.add_argument('--model', type=str, required=True, choices=['llama-3-70b-chat', 'llama-3-70b'])
    args.add_argument('--max_tokens', type=int, help='default = 1000', default=1000)
    args = args.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    tasks = args.tasks.split(',')
    conditions = args.conditions.split(',')
    model = args.model
    if model == 'llama-3-70b-chat':
        model = 'llama-3-70b-chat-hf'
    elif model == 'llama-3-70b':
        model = 'meta-llama-3-70b'
    max_tokens = args.max_tokens

    for task in tasks:
        for condition in conditions:
            name = f'{task}_{condition}'
            d = solve_file(name, model=model, temperature=0.0, max_tokens=max_tokens)
            if d is not None:
                print(f'{name}, {model}: {d["acc"]:.2f} ({d["ed"]:.2f})')

