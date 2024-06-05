import logging
import json
import argparse
from tqdm import tqdm
import os
import anthropic
from anthropic import HUMAN_PROMPT, AI_PROMPT
import time
logging.getLogger().setLevel(logging.ERROR)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

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


def claude_responses(prompt_list, model="claude-3-opus-20240229", max_tokens=1000, temperature=0.0):
    responses = []
    for prompt in tqdm(prompt_list):
        output = None
        for _ in range(10):
            try:
                completion = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system="Provide only your answer, without any explanation.",
                    messages=[{"role":"user", "content": prompt}]
                )

                output = completion.content[0].text
                if output is None:
                    output = ""
            except:
                time.sleep(60)
            
            if not (output is None):
                break

        if output is None:
            responses.append("")
        else:
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
    res = claude_responses(prompts, model=model, temperature=0.0, max_tokens=max_tokens)

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
    args.add_argument('--model', type=str, required=True, choices=['claude-3'])
    args.add_argument('--max_tokens', type=int, help='default = 1000', default=1000)
    args = args.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    tasks = args.tasks.split(',')
    conditions = args.conditions.split(',')
    model = args.model
    if model == "claude-3":
        model = "claude-3-opus-20240229"
    max_tokens = args.max_tokens

    for task in tasks:
        for condition in conditions:
            name = f'{task}_{condition}'
            d = solve_file(name, model=model, temperature=0.0, max_tokens=max_tokens)
            if d is not None:
                print(f'{name}, {model}: {d["acc"]:.2f} ({d["ed"]:.2f})')

