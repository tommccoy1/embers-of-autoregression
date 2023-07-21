
import random

common_chars = "abcdefghijklmnopqrstuvwxyz"
rare_chars = "😀😡😬👻🤖🎃👍🎩👑🐣🦆🐢🐙🐋🐎🦔🌲🌛🔥🚀🗻🏠⏳🔑🎁📆"

emoji_names = ["smiling face", "angry face", "grimacing face", "ghost", "robot", "jack-o'-lantern",
        "thumbs up", "top hat", "crown", "chick", "duck", "tortoise", "squid", "whale", "horse", "hedgehog",
        "tree", "moon", "fire", "rocket", "mountain", "house", "hourglass", "key", "present", "calendar"]

fo_common = open("../examples/counting_chars_common.txt", "w")
fo_rare = open("../examples/counting_chars_rare.txt", "w")


for length in range(1,101):
    for _ in range(30):
        chars_common = []
        chars_rare = []

        common_char = random.choice(list(common_chars))
        rare_char, emoji_name = random.choice(list(zip(rare_chars, emoji_names)))

        for _ in range(length):
            chars_common.append(common_char)
            chars_rare.append(rare_char)

        joined = " ".join(chars_common)
        joined2 = " ".join(chars_rare)

        fo_common.write("".join(chars_common) + "\n")
        fo_rare.write(emoji_name + "\t" + "".join(chars_rare) + "\n")








