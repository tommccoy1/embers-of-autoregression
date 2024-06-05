

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

import os
import time

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

my_safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }


gemini_model = genai.GenerativeModel("gemini-1.0-pro-001", safety_settings=my_safety_settings)


from transformers import AutoTokenizer
llama3_tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-70B-Instruct")

def count_tokens_gemini(sentence):
    return gemini_model.count_tokens(sentence).total_tokens

def count_tokens_llama3(sentence):
    return len(llama3_tokenizer.encode(sentence))


fi_llama3 = open("saved_llama3_tokenization.tsv", "r")
llama3_tokenized = {}
for line in fi_llama3:
    parts = line.strip().split("\t")
    llama3_tokenized[parts[0]] = int(parts[1])

fi_gemini = open("saved_gemini_tokenization.tsv", "r")
gemini_tokenized = {}
for line in fi_gemini:
    parts = line.strip().split("\t")
    gemini_tokenized[parts[0]] = int(parts[1])

fi = open("saved_stimuli_statistics.tsv", "r")
fo_llama3 = open("saved_llama3_tokenization.tsv", "a")
fo_gemini = open("saved_gemini_tokenization.tsv", "a")

for index, line in enumerate(fi):
    if index % 1000 == 0:
        print(index)

    parts = line.strip().split("\t")
    sentence = parts[0]

    if sentence not in llama3_tokenized:
        llama3_tokens = str(count_tokens_llama3(sentence))
        fo_llama3.write(sentence + "\t" + str(llama3_tokens) + "\n")

    if sentence not in gemini_tokenized:
        gemini_tokens = None
        for _ in range(20):
            try:
                gemini_tokens = str(count_tokens_gemini(sentence))
            except Exception as e:
                string_exception = str(e)
                if "not supported" in string_exception:
                    palm_tokens = 0
                else:
                    print("WAITING", index, string_exception.split("\n")[0])
                    time.sleep(180)

            if not (gemini_tokens is None):
                break

        
        if gemini_tokens is None:
            15/0

        fo_gemini.write(sentence + "\t" + str(gemini_tokens) + "\n")






