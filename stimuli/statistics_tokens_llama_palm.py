
from transformers import LlamaTokenizerFast
llama_tokenizer = LlamaTokenizerFast.from_pretrained("hf-internal-testing/llama-tokenizer")


import google.generativeai as palm
import os
import time

palm.configure(api_key=os.environ['PALM_API_KEY'])


def count_tokens_llama(sentence):
    return len(llama_tokenizer.encode(sentence))

def count_tokens_palm(sentence):
    return palm.count_text_tokens("models/text-bison-001", sentence)["token_count"]


fi_llama = open("saved_llama_tokenization.tsv", "r")
llama_tokenized = {}
for line in fi_llama:
    parts = line.strip().split("\t")
    llama_tokenized[parts[0]] = int(parts[1])

fi_palm = open("saved_palm_tokenization.tsv", "r")
palm_tokenized = {}
for line in fi_palm:
    parts = line.strip().split("\t")
    palm_tokenized[parts[0]] = int(parts[1])

fi = open("saved_stimuli_statistics.tsv", "r")
fo_llama = open("saved_llama_tokenization.tsv", "a")
fo_palm = open("saved_palm_tokenization.tsv", "a")

for index, line in enumerate(fi):
    if index % 1000 == 0:
        print(index)

    parts = line.strip().split("\t")
    sentence = parts[0]

    if sentence not in llama_tokenized:
        llama_tokens = str(count_tokens_llama(sentence))
        fo_llama.write(sentence + "\t" + str(llama_tokens) + "\n")

    if sentence not in palm_tokenized:
        palm_tokens = None
        for _ in range(20):
            try:
                palm_tokens = str(count_tokens_palm(sentence))
            except Exception as e:
                string_exception = str(e)
                if string_exception == "400 The requested language is not supported by models/text-bison-001":
                    palm_tokens = 0
                else:
                    print("WAITING", index, string_exception.split("\n")[0])
                    time.sleep(180)

            if not (palm_tokens is None):
                break

        
        if palm_tokens is None:
            15/0

        fo_palm.write(sentence + "\t" + str(palm_tokens) + "\n")






