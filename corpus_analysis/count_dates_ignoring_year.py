
fi = open("c4_dates.txt", "r")

counts = {}
month_length_nonleap = {}
month_length_nonleap["01"] = 31
month_length_nonleap["02"] = 28
month_length_nonleap["03"] = 31
month_length_nonleap["04"] = 30
month_length_nonleap["05"] = 31
month_length_nonleap["06"] = 30
month_length_nonleap["07"] = 31
month_length_nonleap["08"] = 31
month_length_nonleap["09"] = 30
month_length_nonleap["10"] = 31
month_length_nonleap["11"] = 30
month_length_nonleap["12"] = 31

date_list = []
for month in range(1,13):
    month_str = str(month)
    if len(month_str) == 1:
        month_str = "0" + month_str
    month_length = month_length_nonleap[month_str]

    for i in range(1, month_length+1):
        day_str = str(i)
        if len(day_str) == 1:
            day_str = "0" + day_str
        date_list.append(month_str + "/" + day_str)


for date in date_list:
    counts[date] = 0


for line in fi:
    parts = line.strip().split()
    date = parts[0]
    date_type = parts[1]

    parts = date.split("/")
    year = parts[2]

    # Ignore leap years
    if int(year) % 4 == 0:
        continue

    if date_type == "unclear":
        month = parts[0]
        day = parts[1]

        if month + "/" + day in counts:
            counts[month + "/" + day] += 0.67

        month = parts[1]
        day = parts[0]

        if month + "/" + day in counts:
            counts[month + "/" + day] += 0.33

    elif date_type == "mmddyyyy":
        month = parts[0]
        day = parts[1]

        if month + "/" + day in counts:
            counts[month + "/" + day] += 1

    elif date_type == "ddmmyyyy":
        month = parts[1]
        day = parts[0]

        if month + "/" + day in counts:
            counts[month + "/" + day] += 1


for day in counts:
    print(day, counts[day])




