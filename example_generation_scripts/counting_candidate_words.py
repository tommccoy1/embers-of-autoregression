

import tiktoken



gpt4_enc = tiktoken.get_encoding("cl100k_base")


wikitext = {}
fi = open("wikitext-103/wiki.train.tokens", "r")
for line in fi:
    words = line.strip().split()
    for word in words:
        if word not in wikitext:
            wikitext[word] = 0
        wikitext[word] += 1

words = []
fi = open("cmu_words_by_prob.txt", "r")
count_by_tokens = {}
for line in fi:
    word = line.strip().split("\t")[1]
    if word not in wikitext:
        continue

    if wikitext[word] < 20:
        continue

    ntokens = len(gpt4_enc.encode(word))
    ntokens_spaced = len(gpt4_enc.encode(" " + word))
    if ntokens == ntokens_spaced:
        words.append([ntokens, word])

        if ntokens not in count_by_tokens:
            count_by_tokens[ntokens] = 0
        count_by_tokens[ntokens] += 1

for ntokens in count_by_tokens:
    print(ntokens, count_by_tokens[ntokens])
print("")



common = words[:8000]
rare = words[8000:][::-1]

count_by_tokens_common = {}
count_by_tokens_rare = {}

for ntokens, _ in common:
    if ntokens not in count_by_tokens_common:
        count_by_tokens_common[ntokens] = 0
    count_by_tokens_common[ntokens] += 1

for ntokens, _ in rare:
    if ntokens not in count_by_tokens_rare:
        count_by_tokens_rare[ntokens] = 0
    count_by_tokens_rare[ntokens] += 1

print("COMMON")
for ntokens in count_by_tokens_common:
    print(ntokens, count_by_tokens_common[ntokens])
print("")

print("RARE")
for ntokens in count_by_tokens_rare:
    print(ntokens, count_by_tokens_rare[ntokens])
print("")




fo_common = open("counting_common_words.txt", "w")
fo_rare = open("counting_rare_words.txt", "w")


common_by_tokens = {}
rare_by_tokens = {}

for tokens, word in common:
    if tokens not in common_by_tokens:
        common_by_tokens[tokens] = []
    if len(common_by_tokens[tokens]) < 1000:
        common_by_tokens[tokens].append(word)


for tokens, word in rare:
    if tokens not in rare_by_tokens:
        rare_by_tokens[tokens] = []
    if len(rare_by_tokens[tokens]) < 1000:
        rare_by_tokens[tokens].append(word)


for tokens in range(1,4):
    for word in common_by_tokens[tokens]:
        fo_common.write(str(tokens) + "\t" + word + "\n")

    for word in rare_by_tokens[tokens]:
        fo_rare.write(str(tokens) + "\t" + word + "\n")

