
fi = open("../wikitext-103/counting_tokens.txt", "r")

fo_common = open("../wikitext-103/counting_common_words.txt", "w")
fo_rare = open("../wikitext-103/counting_rare_words.txt", "w")

words = []
for index, line in enumerate(fi):
    parts = line.strip().split("\t")
    count = int(parts[0])
    tokens = int(parts[1])
    word = parts[2]

    words.append([tokens, word])

common = words[:10000]
rare = words[-10000:][::-1]

common_by_tokens = {}
rare_by_tokens = {}

for tokens, word in common:
    if tokens not in common_by_tokens:
        common_by_tokens[tokens] = []
    if len(common_by_tokens[tokens]) < 400:
        common_by_tokens[tokens].append(word)


for tokens, word in rare:
    if tokens not in rare_by_tokens:
        rare_by_tokens[tokens] = []
    if len(rare_by_tokens[tokens]) < 400:
        rare_by_tokens[tokens].append(word)


for tokens in range(1,4):
    for word in common_by_tokens[tokens]:
        fo_common.write(str(tokens) + "\t" + word + "\n")

    for word in rare_by_tokens[tokens]:
        fo_rare.write(str(tokens) + "\t" + word + "\n")

  


