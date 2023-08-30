

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import tiktoken


if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


# Get perplexity using GPT-2
def prob_gpt2(word):

    sentence = 'The word is "' + word + '"'

    # Tokenize the sentence
    tokens = gpt2_tokenizer.encode(sentence)

    targets = tokens[:]

    # Compute average log likelihood for the generation
    input_ids = torch.LongTensor(tokens).to(device)
    target_ids = torch.LongTensor(targets).to(device)

    with torch.no_grad():
        outputs = gpt2_model(input_ids, labels=target_ids)
        log_likelihood = -1*outputs[0]*len(input_ids)

    # 17.81036949157715 = logprob('The word is"'); removing this to just get
    # the word prob
    return log_likelihood.item() + 17.81036949157715


wiki_counts = {}
fi = open("wikitext-103/wiki.train.tokens", "r")
for line in fi:
    words = line.lower().strip().split()
    for word in words:
        if word not in wiki_counts:
            wiki_counts[word] = 0
        wiki_counts[word] += 1


gpt4_enc = tiktoken.get_encoding("cl100k_base")
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2-xl").to(device)

fi = open("cmudict.txt", "r", encoding="latin")


chars = "abcdefghijklmnopqrstuvwxyz"
def is_roman(word):
    for char in word:
        if char not in chars:
            return False
    return True


words = []
for index, line in enumerate(fi):
    if index % 1000 == 0:
        print(index)
    parts = line.strip().split("\t")
    word = parts[0].lower()

    if word in wiki_counts:
        if wiki_counts[word] >= 20 and is_roman(word):

            n_tokens = len(gpt4_enc.encode(word))
            if n_tokens < 4:
                logprob = prob_gpt2(word)
                words.append([logprob, n_tokens, word])

words = sorted(words, key=lambda x: -1*x[0])
fo = open("cmu_words_by_prob.txt", "w")
for prob, tokens, word in words:
    fo.write(str(prob) + "\t" + word + "\n")


