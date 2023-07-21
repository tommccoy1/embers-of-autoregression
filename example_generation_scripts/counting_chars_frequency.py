
import random
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")


common_numbers = []
rare_numbers = []
fi_counts = open("../wikitext-103/counting_numbers.txt", "r")
numbers = {}
for line in fi_counts:
    parts = line.strip().split()
    numbers[int(parts[0])] = int(parts[1])

for n in numbers:
    if n >= 3 and n <= 103:
        if numbers[n] > 2*numbers[n-1] and numbers[n] > 2*numbers[n-2] and numbers[n] > 2*numbers[n+1] and numbers[n] > 2*numbers[n+2]:
            common_numbers.append(n)
            rare_numbers.append(n-2)
            rare_numbers.append(n-1)
            rare_numbers.append(n+1)
            rare_numbers.append(n+2)


common_chars = "abcdefghijklmnopqrstuvwxyz"
rare_chars = "😀😡😬👻🤖🎃👍🎩👑🐣🦆🐢🐙🐋🐎🦔🌲🌛🔥🚀🗻🏠⏳🔑🎁📆"

emoji_names = ["smiling face", "angry face", "grimacing face", "ghost", "robot", "jack-o'-lantern",
        "thumbs up", "top hat", "crown", "chick", "duck", "tortoise", "squid", "whale", "horse", "hedgehog",
        "tree", "moon", "fire", "rocket", "mountain", "house", "hourglass", "key", "present", "calendar"]



fo_common_common = open("../examples/counting_chars_common_common.txt", "w")
fo_common_rare = open("../examples/counting_chars_common_rare.txt", "w")
fo_rare_common = open("../examples/counting_chars_rare_common.txt", "w")
fo_rare_rare = open("../examples/counting_chars_rare_rare.txt", "w")


for common_number in common_numbers:
    # Each common number is repeated 100 times
    for _ in range(100):
        chars_common = []
        chars_rare = []

        common_char = random.choice(list(common_chars))
        rare_char, rare_name = random.choice(list(zip(rare_chars, emoji_names)))

        for _ in range(common_number):
            chars_common.append(common_char)
            chars_rare.append(rare_char)

        fo_common_common.write("".join(chars_common) + "\n")
        fo_common_rare.write(rare_name + "\t" + "".join(chars_rare) + "\n")


for rare_number in rare_numbers:
    # Each rare number is repeated 25 times
    for _ in range(25):
        chars_common = []
        chars_rare = []

        common_char = random.choice(list(common_chars))
        rare_char, rare_name = random.choice(list(zip(rare_chars, emoji_names)))

        for _ in range(rare_number):
            chars_common.append(common_char)
            chars_rare.append(rare_char)

        fo_rare_common.write("".join(chars_common) + "\n")
        fo_rare_rare.write(rare_name + "\t" + "".join(chars_rare) + "\n")






