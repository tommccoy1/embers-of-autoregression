

fi = open("numbers.txt", "r")

number_counts = {}
for line in fi:
    parts = line.strip().split("\t")
    number_counts[int(parts[0])] = int(parts[1])

for i in range(3,101):
    if number_counts[i] > 2*number_counts[i-2] and number_counts[i] > 2*number_counts[i-1] and number_counts[i] > 2*number_counts[i+1] and number_counts[i] > 2*number_counts[i+2]:
        print(i)

