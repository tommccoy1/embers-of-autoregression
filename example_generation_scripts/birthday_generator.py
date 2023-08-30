

def in_range(number, span):
    if number >= span[0] and number < span[1]:
        return True
    return False

limits1 = [2000,100000000]
limits2 = [200,2000]
limits3 = [20,200]
limits4 = [5,20]


counts = {}
fi = open("birthday_counts.txt", "r")
for line in fi:
    count, name = line.strip().split("\t")
    counts[name] = int(count)

name2date = {}
date2name = {}
names = {}
repeats = {}
fi = open("birthday_info.txt", "r")
for line in fi:
    name, date = line.strip().split("\t")
    if name not in names:
        names[name] = 1
    else:
        repeats[name] = 1
fi.close()

fi = open("birthday_info.txt", "r")
for line in fi:
    name, date = line.strip().split("\t")
    if name not in name2date and name not in repeats:
        name2date[name] = date
        if date not in date2name:
            date2name[date] = []
        date2name[date].append(name)

verified = {}
fi = open("birthdays_verified.txt", "r")
for line in fi:
    verified[line.strip()] = 1

fo1 = open("../examples/birthdays_1.txt", "w")
fo2 = open("../examples/birthdays_2.txt", "w")
fo3 = open("../examples/birthdays_3.txt", "w")
fo4 = open("../examples/birthdays_4.txt", "w")


count_dates = 0
count_verified = 0
used_names = []
for date in date2name:
    if count_verified == 100:
        break

    has1 = False
    has2 = False
    has3 = False
    has4 = False

    if len(date2name[date]) < 4:
        continue

    name_list = [None, None, None, None]
    for name in date2name[date]:
        if name not in counts:
            continue

        if in_range(counts[name], limits1) and not has1:
            has1 = True
            name_list[0] = name
        if in_range(counts[name], limits2) and not has2:
            has2 = True
            name_list[1] = name
        if in_range(counts[name], limits3) and not has3:
            has3 = True
            name_list[2] = name
        if in_range(counts[name], limits4) and not has4:
            has4 = True
            name_list[3] = name

    if has1 and has2 and has3 and has4:
        count_dates += 1
        all_verified = True
        for name in name_list:
            if not name in verified:
                all_verified = False

        if all_verified:
            count_verified += 1
        
            fo1.write(name_list[0] + "\t" + date + "\n")
            fo2.write(name_list[1] + "\t" + date + "\n")
            fo3.write(name_list[2] + "\t" + date + "\n")
            fo4.write(name_list[3] + "\t" + date + "\n")

            for name in name_list:
                used_names.append(name)

 
        else:
            for name in name_list:
                if name not in verified:
                    print(name, date)
       
print(count_dates)
print(count_verified)

fo_used = open("birthdays_used_names.txt", "w")
for name in used_names:
    fo_used.write(name + "\n")

