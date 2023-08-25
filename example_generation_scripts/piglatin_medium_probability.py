


import torch
import tiktoken
from transformers import AutoTokenizer, RobertaForMaskedLM, GPT2LMHeadModel, GPT2Tokenizer
from nltk.tokenize import word_tokenize


# Function for converting a sentence to Pig Latin
def pig_encode(sentence, suffix="ay"):
    words = sentence.lower().split()
    new_sentence = []
    for word in words:
        punct = ""
        if word[-1] in [".", "?", "!", ",", ";", ":"] and word[:-1].isalpha():
            punct = word[-1]
            word = word[:-1]

        if (not word.isalpha() or word[0] == "q") and not (word == "—" or word == "–"):

            usable = True
            for char in word:
                if char.isalpha() or char in ["'", "’", "“", "”"]:
                    continue
                else:
                    print("\"" + word + "\"", char)
                    return "UNUSABLE"

        if word == "—" or word == "–":
            new_word = word
        elif word[0] in ["a", "e", "i", "o", "u"]:
            new_word = word + suffix
        elif word[0] == "y":
            new_word = word[1:] + "y" + suffix
        else:
            index_vowel = 0
            has_vowel = True
            while word[index_vowel] not in ["a", "e", "i", "o", "u", "y"]:
                index_vowel += 1
                if index_vowel == len(word):
                    has_vowel = False
                    break
        
            if has_vowel:
                new_word = word[index_vowel:] + word[:index_vowel] + suffix
            else:
                new_word = word + suffix

        new_sentence.append(new_word + punct)

    return " ".join(new_sentence)



if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2-xl").to(device)

# Get logprob using GPT-2
def logprob_gpt2(sentence):

    # Tokenize the sentence
    tokens = gpt2_tokenizer.encode(sentence)

    targets = tokens[:]

    # Compute log likelihood for the generation
    input_ids = torch.LongTensor(tokens).to(device)
    target_ids = torch.LongTensor(targets).to(device)

    with torch.no_grad():
        outputs = gpt2_model(input_ids, labels=target_ids)
        log_likelihood = -1*outputs[0]*len(tokens)

    return log_likelihood






# Replace each token with a new token sampled from RoBERTa (with restrictions)
def bertify(sentence):
    encoding = roberta_tokenizer(sentence)
    tokens = encoding["input_ids"]
    saved_tokens = tokens[:]

    found = False
    attempts = 0
    while not found and attempts < 50:
        attempts += 1
        tokens = saved_tokens[:]
        new_sentence = []
        for index, token in enumerate(tokens[:-1]):
            if index == 0:
                continue
       
            # Don't change punctuation (usually results in errors)
            if roberta_tokenizer.decode(token) in [".", "?", "!", ","]:
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
            sorted_indices_to_remove1 = cumulative_probs < 0.90
            sorted_indices_to_remove2 = cumulative_probs > 0.95
            sorted_indices_to_remove = torch.logical_or(sorted_indices_to_remove1, sorted_indices_to_remove2)
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        
            # If no tokens remain, reinstate the highest-probability token
            if torch.sum(torch.logical_not(sorted_indices_to_remove)) == 0:
                new_sentence.append(tokens[index])
                continue

                sorted_indices_to_remove[..., 0] = 0
       
            # Perform the actual filtering
            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            
            # Only allow new tokens that contain the same number of letters
            # as the old ones
            length_indices_to_remove = (decoded_tokens != len(roberta_tokenizer.decode([token])))
            
            if torch.sum(torch.logical_not(indices_to_remove)) == 0:
                new_sentence.append(tokens[index])
                continue
            
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

        new_sentence = roberta_tokenizer.decode(new_sentence).lower()
        if len(new_sentence) == len(sentence) and len(gpt4_enc.encode(new_sentence)) == len(gpt4_enc.encode(sentence)):
            contains_invalid_word = False

            # Check for common cases that cannot be Pig-Latin-ified unambiguously
            words = word_tokenize(new_sentence)
            for word in words:
                if word == "one" or word == "two":
                    contains_invalid_word = True
                if (not (word.replace("'", "").isalpha() or word in [".", ",", "!", ":", ";", "\"", "(", ")", "’", '“', '”', '—'])) or (word.isupper() and len(word) > 1):
                    contains_invalid_word = True
                if word.lower().startswith("eu"):
                    contains_invalid_word = True
                if word[0].lower() in ["c", "g"] and len(word) > 1:
                    if word[1].lower() in ["e", "i", "y"]:
                        contains_invalid_word = True

            if not contains_invalid_word:
                found = True
    
    if attempts == 100:
        return "NONE FOUND"
    else:
        return new_sentence



roberta_tokenizer = AutoTokenizer.from_pretrained('roberta-large', use_fast=True)
roberta_model = RobertaForMaskedLM.from_pretrained('roberta-large').to(device)
mask_id = roberta_tokenizer.encode("[MASK]")[1]
decoded_tokens = torch.LongTensor([len(roberta_tokenizer.decode([x])) for x in range(50265)]).to(device)
gpt4_enc = tiktoken.get_encoding("cl100k_base")


fi = open("../examples/piglatin_high_probability.txt", "r")
fo = open("../examples/piglatin_medium_probability.txt", "w")
for index, line in enumerate(fi):
    sentence = line.strip().lower()
    fo.write("\n")
    print("")
    print("LINE INDEX", index)
    print(logprob_gpt2(sentence).item(), logprob_gpt2(pig_encode(sentence)).item(), logprob_gpt2(rot2_encode(sentence)).item(), sentence)

    candidates = []

    # Produce 20 candidates
    for _ in range(20):
        new_sentence = bertify(sentence)
        candidates.append([logprob_gpt2(new_sentence).item(), logprob_gpt2(pig_encode(new_sentence)).item(), logprob_gpt2(rot2_encode(new_sentence)).item(), new_sentence])
    
    # Print the candidates, sorted by decreasing logprob
    for candidate in sorted(candidates)[::-1]:
        print(candidate[0], candidate[1], candidate[2], candidate[3])
        fo.write(candidate[3] + "\n")











