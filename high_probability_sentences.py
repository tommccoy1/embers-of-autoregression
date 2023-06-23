

from nltk.tokenize import sent_tokenize, word_tokenize
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import math

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2-xl").to(device)

# Given a sentence, returns the minimum of the log probabilities
# of the individual tokens in that sentence, as determined by GPT-2
def min_prob_gpt2(sentence):

    # Tokenize the sentence
    tokens = gpt2_tokenizer.encode(sentence)
    targets = tokens[:]
    
    # Move to device (CPU or GPU)
    input_ids = torch.LongTensor(tokens).to(device)
    target_ids = torch.LongTensor(targets).to(device)

    # Get list of log probabilities of tokens
    all_logprobs = []
    with torch.no_grad():
        outputs = gpt2_model(input_ids, labels=target_ids)
        for target, logits in zip(targets[1:], outputs["logits"][:-1]):
            logprobs = torch.nn.LogSoftmax(dim=0)(logits)
            logprob = logprobs[target]
            all_logprobs.append(logprob.item())

    if all_logprobs == []:
        return -1*math.inf
    else:
        return min(all_logprobs)




# Articles to extract sentences from
filenames = ["turtles_16jun2023",
             "erdogan_15jun2023",
             "wildfires_14jun2023",
             "chavez_14jun2023",
             "mariupol_14jun2023",
             "poetry_14jun2023",
             "thailand_13jun2023",
             "jersey_13jun2023",
             "zimbabwe_13jun2023",
             "kazakhstan_13jun2023",
             "fresno_12jun2023",
             "everest_12jun2023",
             "nyelade_12jun2023",
             "belize_12jun2023",
             "climate_12jun2023",
             "jaguar_10jun2023",
             "taiwan_09jun2023",
             "oleshky_09jun2023",
             "indonesia_09jun2023",
             "kyrgyzstan_09jun2023",
             "trinidad_09jun2023",
             "montalvo_08jun2023",
             "counter_08jun2023",
             "unfreedom_08jun2023",
             "uganda_08jun2023",
             "ngos_07jun2023",
             "hongkong_07jun2023",
             "spain_07jun2023",
             "sidorenko_07jun2023",
             "ukraine_07jun2023",
             "serbia_06jun2023",
             "divisions_06jun2023",
             "boomerang_06jun2023",
             "ecuador_06jun2023",
             "spread_06jun2023",
             "tajikistan_06jun2023",
             "srilanka_06jun2023",
             "donuts_05jun2023",
             "migration_05jun2023",
             "unfreedom_05jun2023",
             "amazigh_05jun2023",
             "taiwan_05jun2023",
             "swatch_04jun2023",
             "hongkong_04jun2023",
             "atlantic_03jun2023",
             "graduation_03jun2023",
             "turkey_03jun2023",
             "moldova_02jun2023",
             "unions_02jun2023",
             "marathon_02jun2023"
             ]

# Compute the minimum log probability for each sentence
# in each of these files
scored_sentences = [] # a list of sentences with their minimum logprobs
for filename in filenames:
    fi = open("global_voices/" + filename + ".txt", "r")
    for line in fi:

        # Split into sentences
        sentences = sent_tokenize(line)

        for sentence in sentences:
            sentence = sentence.replace("[", "").replace("]", "")

            min_prob = min_prob_gpt2(sentence)
            scored_sentences.append([sentence, min_prob])

fo = open("sentence_outputs/high_probability.txt", "w")
sorted_sentences = sorted(scored_sentences, key=lambda x: -1*x[1])
count_printed = 0
for sentence in sorted_sentences:

    # Print the 500 sentences with the maximum minimum log probability
    if count_printed >= 500:
        break

    # Exclude sentences shorter than 10 tokens
    n_words = len(word_tokenize(sentence[0]))
    if n_words < 10:
        continue
    
    print(sentence[1], sentence[0])
    fo.write(sentence[0] + "\n")
    count_printed += 1



