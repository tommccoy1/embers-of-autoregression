
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import tiktoken

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

enc = tiktoken.get_encoding("cl100k_base")
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2-xl").to(device)

# Get perplexity using GPT-2
def prob_gpt2(sentence):

    # Tokenize the sentence
    tokens = gpt2_tokenizer.encode(sentence)

    targets = tokens[:]

    # Compute average log likelihood for the generation
    input_ids = torch.LongTensor(tokens).to(device)
    target_ids = torch.LongTensor(targets).to(device)

    with torch.no_grad():
        outputs = gpt2_model(input_ids, labels=target_ids)
        log_likelihood = -1*outputs[0]*(len(input_ids)-1)

    return log_likelihood.item()


letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
letter_dict = {}
for letter in letters:
    letter_dict[letter] = 1

def is_roman(word):
    for letter in word:
        if letter not in letter_dict:
            return False

    return True


checked = {}
words_with_prob_lower = []
words_with_prob_upper = []
fi = open("cmudict.txt", "r", encoding="latin")
for index, line in enumerate(fi):
    if index % 1000 == 0:
        print(index)
    word = line.strip().split("\t")[0].lower()
    if word in checked:
        continue

    checked[word] = 1
    if len(word) == 7:
        if is_roman(word):
            tokens_lower = enc.encode(word.lower())
            tokens_spaced_lower = enc.encode(" " + word.lower())

            if len(tokens_lower) == 2 and len(tokens_spaced_lower) == 2:
                logprob = prob_gpt2('The word is "' + word + '"')
                words_with_prob_lower.append([logprob, word])

            tokens_upper = enc.encode(word.upper())
            tokens_spaced_upper = enc.encode(" " + word.upper())

            if len(tokens_upper) == 2 and len(tokens_spaced_upper) == 2:
                logprob = prob_gpt2('The word is "' + word + '"')
                words_with_prob_upper.append([logprob, word])

fo_lower = open("vocab_tokens_lower.txt", "w")
fo_upper = open("vocab_tokens_upper.txt", "w")
for prob, word in sorted(words_with_prob_lower)[::-1]:
    fo_lower.write(str(prob) + "\t" + word + "\n")

for prob, word in sorted(words_with_prob_upper)[::-1]:
    fo_upper.write(str(prob) + "\t" + word + "\n")



