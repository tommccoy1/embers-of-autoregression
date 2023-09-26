

fi = open("fahrenheit_celsius_pairs.txt", "r")


count_excluded = 0
count_total = 0

lower_bound = 500

for line in fi:
    parts = line.strip().split()
    f = float(parts[0])
    c = float(parts[1])

    if c <= lower_bound:
        count_excluded += 1
    elif f == int(f) and c == int(c) and (str(int(f)).endswith("0") or str(int(c)).endswith("0")):
        count_excluded += 1
    else:
        print(f, c)
    count_total += 1

print(count_excluded*1.0/count_total, count_excluded, count_total)



