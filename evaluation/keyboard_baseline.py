

import statistics

fi = open("../examples/sentences_high_probability.txt", "r")

seen_letters = "phelowrd"
alphabet = "abcdefghijklmnopqrstuvwxyz"

errors_list = []
for line in fi:
    errors = 0
    sentence = line.strip().lower()
    for char in sentence:
        if char in alphabet and char not in seen_letters:
            errors += 25.0/26.0

    errors_list.append(errors)


print("MEDIAN ERRORS:", statistics.median(errors_list))
print("MEAN ERRORS:", statistics.mean(errors_list))




