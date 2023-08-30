

import random

fo = open("../examples/sorting_numbers.txt", "w")

for _ in range(100):
    found = False
    while not found:
        length = random.choice(list(range(10,21)))

        numbers = []
        for index in range(length):
            number = random.choice(list(range(1,10001)))
            numbers.append(number)

        if len(list(set(numbers))) == len(numbers):
            found = True

    numbers = [str(x) for x in numbers]
    fo.write(", ".join(numbers) + "\n")


