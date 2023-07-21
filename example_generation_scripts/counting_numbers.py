
from collections import Counter


fi = open("../wikitext-103/wiki.train.tokens", "r")

numbers = Counter()
for i in range(1,105):
    numbers[i] = 0

for line in fi:
    words = line.strip().split()

    for word in words:
        if word.isnumeric() and "." not in word and "-" not in word and "," not in word:
            try:
                number = int(word)
                if number in numbers:
                    numbers[number] += 1
            except:
                pass



fo = open("../wikitext-103/counting_numbers.txt", "w")
for number in numbers:
    fo.write(str(number) + "\t" + str(numbers[number]) + "\n")



