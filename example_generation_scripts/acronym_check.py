

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

file_list = []
for position in [1,2]:
    for outp in range(1,6):
        for inp in range(1,6):
            if outp == 1 or inp == 1:
                file_list.append("../examples/acronym" + str(position) + "_" + str(outp) + str(inp) + ".txt")


lines = []
first = True
for file in file_list:
    for index, line in enumerate(open(file, "r")):
        if first:
            lines.append([])
        parts = line.strip().split("\t")
        output = parts[0]
        words = parts[1].split()

        if "acronym1" in file:
            pred = "".join([x[0] for x in words]).upper()
        elif "acronym2" in file:
            pred = "".join([x[1] for x in words]).upper()

        if pred != output:
            print("ERROR", pred, output, file)

        words = line.strip().split()
        words[0] = words[0].upper()
        joined = " ".join(words)
        lines[index].append(joined)


    first = False


for line_list in lines:
    break_list = []
    for line in line_list:
        breaks = "".join([str(len(enc.decode([enc.encode(word)[0]]))) for word in line.split()])
        break_list.append(breaks)

    for break_seq in break_list:
        if break_seq != break_list[0]:
            print("ERROR")




