

TRANSFORMERS_PATH = '/scratch/gpfs/tm4633/transformers'
import os
os.environ['TRANSFORMERS_CACHE'] = TRANSFORMERS_PATH

import torch
from transformers import AutoTokenizer, RobertaForMaskedLM, GPT2LMHeadModel, GPT2Tokenizer

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2-xl").to(device)

# Get perplexity using GPT-2
def perplexity_gpt2(sentence):

    # Tokenize the sentence
    tokens = gpt2_tokenizer.encode(sentence)

    targets = tokens[:]

    # Compute average log likelihood for the generation
    input_ids = torch.LongTensor(tokens).to(device)
    target_ids = torch.LongTensor(targets).to(device)

    with torch.no_grad():
        outputs = gpt2_model(input_ids, labels=target_ids)
        log_likelihood = outputs[0]
    perplexity = torch.exp(log_likelihood)

    return perplexity


def bertify(sentence):
    encoding = roberta_tokenizer(sentence)
    tokens = encoding["input_ids"]

    new_sentence = []
    for index, token in enumerate(tokens[:-1]):
        if index == 0:
            continue
       
        # Don't change punctuation (usually results in errors)
        if roberta_tokenizer.decode(token) in [".", "?", "!", ","]:
            new_sentence.append(token)
            continue

        masked_tokens = tokens[:]
        masked_tokens[index] = mask_id
        
        roberta_outputs = roberta_model(input_ids=torch.LongTensor(masked_tokens).unsqueeze(0).to(device), attention_mask=torch.LongTensor(encoding["attention_mask"]).unsqueeze(0).to(device))
        masked_logits = roberta_outputs["logits"][0][index]
        
        # Filter to only the tokens between 0.90 and 0.95 in the token probability distribution
        sorted_logits, sorted_indices = torch.sort(masked_logits, descending=True)
        cumulative_probs = torch.cumsum(torch.nn.Softmax(dim=-1)(sorted_logits), dim=-1)
        sorted_indices_to_remove1 = cumulative_probs < 0.90
        sorted_indices_to_remove2 = cumulative_probs > 0.95
        sorted_indices_to_remove = torch.logical_or(sorted_indices_to_remove1, sorted_indices_to_remove2)
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        
        # If no tokens remain, reinstate the highest-probability token
        if torch.sum(torch.logical_not(sorted_indices_to_remove)) == 0:
            sorted_indices_to_remove[..., 0] = 0
        
        # Perform the actual filtering
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        masked_logits[indices_to_remove] = -float('Inf')

        # Sample a new token from the filtered distribution
        temperature = 1.0
        probs = torch.nn.Softmax(dim=-1)(masked_logits/temperature)
        probs = torch.distributions.Categorical(probs)
        next_token_id = probs.sample()
        new_sentence.append(next_token_id)
        tokens[index] = next_token_id

    new_sentence = roberta_tokenizer.decode(new_sentence)
    return new_sentence



roberta_tokenizer = AutoTokenizer.from_pretrained('roberta-large', use_fast=True)
roberta_model = RobertaForMaskedLM.from_pretrained('roberta-large').to(device)
mask_id = roberta_tokenizer.encode("[MASK]")[1]

checked = {}
fi1 = open("sentence_outputs/high_probability.txt", "r")
fi2 = open("sentence_outputs/low_probability.txt", "r")

#for line1, line2 in zip(fi1, fi2):
#    checked[line1] = line2


fi = open("sentence_outputs/high_probability_piglatin_redo.txt", "r")
fo = open("sentence_outputs/low_probability_piglatin_redo.txt", "w")
for line in fi:
    if line in checked:
        fo.write(checked[line])
        continue

    sentence = line.strip()
    fo.write("\n")
    print("")
    print(perplexity_gpt2(sentence).item(), sentence)

    candidates = []

    # Produce 20 candidates
    for _ in range(100):
        new_sentence = bertify(sentence)
        candidates.append([perplexity_gpt2(new_sentence).item(), new_sentence])
    
    # Print the candidates, sorted by decreasing perplexity
    for candidate in sorted(candidates)[::-1]:
        print(candidate[0], candidate[1])
        fo.write(candidate[1] + "\n")











