

import jsonlines
import sys


from datasets import load_dataset
ds = load_dataset("c4", "en", split="train", streaming=True)


rot_list = []
# Only need up to 10 because the ones from 10 to 26 contain the substring rot-1 or rot1 or rot-2 or rot2
for shift in range(1,10):
    rot_list.append(" rot" + str(shift))
    rot_list.append(" rot-" + str(shift))

fo = open("c4_shifts.txt", "a")
for index, obj in enumerate(ds):
    if index % 100000 == 0:
        print(index)

    line = obj["text"].lower()
    lines = line.split("\n")
    has_cipher = False
    for inner_line in lines:

        has_cipher_inner = False
            

        if "shift cipher" in inner_line.lower() or "caesar cipher" in inner_line.lower() or "next letter in the alphabet" in inner_line.lower() or "previous letter in the alphabet" in inner_line.lower():
            has_cipher = True
            has_cipher_inner = True

        for rot in rot_list:
            if rot in inner_line.lower():
                has_cipher = True
                has_cipher_inner = True

        if has_cipher_inner:
            print(inner_line)

    if has_cipher:
        fo.write(line.lower())
        fo.write("\n")



