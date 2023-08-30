
from datasets import load_dataset

df = load_dataset("wiki_bio")

alphabet = "abcdefghijklmnopqrstuvwxyz "
alpha_dict = {}
for char in alphabet:
    alpha_dict[char] = 1

def is_roman(string):
    for char in string:
        if char not in alpha_dict:
            return False

    return True

def is_year(string):
    if string.isnumeric() and len(string) == 4 and int(string) > 1700 and int(string) < 2020:
        return True
    else:
        return False

def is_day(string):
    if string.isnumeric() and int(string) > 0 and int(string) < 32:
        return True
    else:
        return False

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
def is_month(string):
    return string in months

def is_date(string):
    words = string.split()
    if len(words) == 3:
        return is_day(words[0]) and is_month(words[1]) and is_year(words[2])
    elif len(words) == 4 and words[2] == ",":
        return is_month(words[0]) and is_day(words[1]) and is_year(words[3])


def standardize_name(string):
    words = string.split()
    new_words = [x.capitalize() for x in words]
    return " ".join(new_words)


def standardize_date(string):
    words = string.split()
    if len(words) == 3:
        return words[1].capitalize() + " " + str(int(words[0])) + ", " + words[2]
    else:
        return words[0].capitalize() + " " + str(int(words[1])) + ", " + words[3]

fo = open("birthday_info.txt", "w")
for person in df["train"]:
    header2index = {}
    for index, header in enumerate(person["input_text"]["table"]["column_header"]):
        header2index[header] = index

    content = person["input_text"]["table"]["content"]
    if "name" in header2index and "birth_date" in header2index:
        name = content[header2index["name"]]
        birth_date = content[header2index["birth_date"]]

        if is_date(birth_date) and is_roman(name):
            fo.write(standardize_name(name) + "\t" + standardize_date(birth_date) + "\n")





