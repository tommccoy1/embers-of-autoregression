

from nltk import word_tokenize

from datasets import load_dataset
ds = load_dataset("c4", "en", split="train", streaming=True)


characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ😀😡😬👻🤖🎃👍🎩👑🐣🦆🐢🐙🐋🐎🦔🌲🌛🔥🚀🗻🏠⏳🔑🎁📆"
char_counts = {}
for character in characters:
    char_counts[character] = 0

word_count = 0
prev_milestone = 0
for index, obj in enumerate(ds):

    if word_count - prev_milestone >= 10000000:
        prev_milestone += 10000000
        print(prev_milestone // 10000000)

    if word_count >= 1000000000:
        break
    
    line = obj["text"]
    words = word_tokenize(line)

    for char in line:
        if char in char_counts:
            char_counts[char] += 1
    word_count += len(words)

fo = open("c4_character_counts.txt", "w")

for char in char_counts:
    fo.write(char + "\t" + str(char_counts[char]) + "\n")


