
fi2 = open("vocab_tokens_upper_remote.txt", "r")
fi4 = open("filtered_vocab_tokens_upper.txt", "r")


allowed = {}

for line in fi4:
    word = line.strip().split()[-1]
    allowed[word] = 1
    if "CERTAIN" in line:
        print("'" + word + "'")


fo4 = open("vocab_tokens_upper_filterd.txt", "w")
for line in fi2:
    word = line.strip().split()[-1].upper()
    if word == "CERTAIN":
        print(word, word in allowed)
    if word in allowed:
        fo4.write(line)





