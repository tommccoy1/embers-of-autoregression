


import torch
import tiktoken
from transformers import AutoTokenizer, RobertaForMaskedLM, GPT2LMHeadModel, GPT2Tokenizer

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

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



# Replace each token with a new token sampled from RoBERTa (with restrictions)
def bertify(sentence):
    encoding = roberta_tokenizer(sentence)
    tokens = encoding["input_ids"]
    saved_tokens = tokens[:]

    # Try 100 times; if you haven't found one by then, that may mean
    # there are none that meet all the restrictions
    found = False
    match1 = False
    match2 = False
    attempts = 0
    while not found and attempts < 20:
        attempts += 1
        tokens = saved_tokens[:]
        new_sentence = []
        for index, token in enumerate(tokens[:-1]):
            if index == 0:
                continue
       
            # Don't change punctuation (usually results in errors)
            if roberta_tokenizer.decode(token) in [".", "?", "!", ","] or roberta_tokenizer.decode(token).strip() in ["a", "an", "the"]:
                new_sentence.append(token)
                continue

            # Mask out the token to replace
            masked_tokens = tokens[:]
            masked_tokens[index] = mask_id
        
            roberta_outputs = roberta_model(input_ids=torch.LongTensor(masked_tokens).unsqueeze(0).to(device), attention_mask=torch.LongTensor(encoding["attention_mask"]).unsqueeze(0).to(device))
            masked_logits = roberta_outputs["logits"][0][index]
        
            # Filter to only the tokens between 0.90 and 0.95 in the token probability distribution
            sorted_logits, sorted_indices = torch.sort(masked_logits, descending=True)
            cumulative_probs = torch.cumsum(torch.nn.Softmax(dim=-1)(sorted_logits), dim=-1)
            if match2:
                sorted_indices_to_remove1 = cumulative_probs < 0.90
                sorted_indices_to_remove2 = cumulative_probs > 1.00
            elif match1:
                sorted_indices_to_remove1 = cumulative_probs < 0.90
                sorted_indices_to_remove2 = cumulative_probs > 0.99
            else:
                sorted_indices_to_remove1 = cumulative_probs < 0.90
                sorted_indices_to_remove2 = cumulative_probs > 0.95
            sorted_indices_to_remove = torch.logical_or(sorted_indices_to_remove1, sorted_indices_to_remove2)
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        
            # If no tokens remain, reinstate the highest-probability token
            if torch.sum(torch.logical_not(sorted_indices_to_remove)) == 0:
                new_sentence.append(tokens[index])
                continue
            elif attempts > 10 and torch.sum(torch.logical_not(sorted_indices_to_remove)) < 10:
                # If we've had this many attempts, it might mean that there are no good options,
                # so here we relax the criteria a bit
                new_sentence.append(tokens[index])
                continue

            # Perform the actual filtering
            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            
            # Further filter to only include tokens of the same length as the token being replaced
            length_indices_to_remove = (decoded_tokens != len(roberta_tokenizer.decode([token])))
            
            # Zero out the tokens that fail to meet the restrictions
            masked_logits[indices_to_remove] = -float('Inf')
            masked_logits[length_indices_to_remove] = -float('Inf')
            if torch.sum(torch.exp(masked_logits)) == 0:
                new_sentence.append(tokens[index])
                continue

            # Sample a new token from the filtered distribution
            temperature = 1.0
            probs = torch.nn.Softmax(dim=-1)(masked_logits/temperature)
            probs = torch.distributions.Categorical(probs)
            next_token_id = probs.sample()
            new_sentence.append(next_token_id)
            tokens[index] = next_token_id

        new_sentence = roberta_tokenizer.decode(new_sentence)

        # Check if the new sentence matches the length of the original sentence, in
        # both letter count and token count
        if len(new_sentence) == len(sentence) and len(gpt4_tokenizer.encode(new_sentence)) == len(gpt4_tokenizer.encode(sentence)):
            if new_sentence == sentence and not match1:
                match1 = True
            elif new_sentence == sentence and match1:
                match2 = True
            else:
                found = True
        else:
            pass
            #print("MISMATCH")
            #print(sentence)
            #print(new_sentence)
            #print("")
    
    if attempts == 100:
        return "NONE FOUND"
    else:
        return new_sentence



gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2-xl").to(device)


roberta_tokenizer = AutoTokenizer.from_pretrained('roberta-large', use_fast=True)
roberta_model = RobertaForMaskedLM.from_pretrained('roberta-large').to(device)
mask_id = roberta_tokenizer.encode("[MASK]")[1]
decoded_tokens = torch.LongTensor([len(roberta_tokenizer.decode([x])) for x in range(50265)]).to(device)

gpt4_tokenizer = tiktoken.get_encoding("cl100k_base")


fi = open("../examples/swap_high_probability.txt", "r")
fo = open("../examples/swap_medium_probability.txt", "w")
for index, line in enumerate(fi):
    sentence = line.strip()
    fo.write("\n")
    print("")
    print("LINE INDEX", index)
    print(perplexity_gpt2(sentence).item(), sentence)

    candidates = []

    # Produce 20 candidates
    for _ in range(20):
        new_sentence = bertify(sentence)
        candidates.append([perplexity_gpt2(new_sentence).item(), new_sentence])
    
    # Print the candidates, sorted by decreasing perplexity
    for candidate in sorted(candidates)[::-1]:
        fo.write(candidate[1] + "\n")
        print(candidate[0], candidate[1])











