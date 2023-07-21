
import random

# Number to text
n2t = {}
n2t[1] = "one"
n2t[2] = "two"
n2t[3] = "three"
n2t[4] = "four"
n2t[5] = "five"
n2t[6] = "six"
n2t[7] = "seven"
n2t[8] = "eight"
n2t[9] = "nine"
n2t[10] = "ten"
n2t[11] = "eleven"
n2t[12] = "twelve"
n2t[13] = "thirteen"
n2t[14] = "fourteen"
n2t[15] = "fifteen"
n2t[16] = "sixteen"
n2t[17] = "seventeen"
n2t[18] = "eighteen"
n2t[19] = "nineteen"
for digit, tens in [(20, "twenty"), (30, "thirty"), (40, "forty"), (50, "fifty"), (60, "sixty"), (70, "seventy"), (80, "eighty"), (90, "ninety")]:
    n2t[digit] = tens

    for i in range(1,10):
        n2t[digit+i] = tens + "-" + n2t[i]

# Change string to alternating capital letters
def caps(string):
    new_string = ""
    cap_now = False

    for char in string:
        if char == "-":
            new_string = new_string + char
        elif cap_now:
            new_string = new_string + char.upper()
            cap_now = False
        else:
            new_string = new_string + char.lower()
            cap_now = True

    return new_string

fo_number = open("../examples/multiplication_number.txt", "w")
fo_word = open("../examples/multiplication_word.txt", "w")
fo_allcaps = open("../examples/multiplication_allcaps.txt", "w")
fo_alternatingcaps = open("../examples/multiplication_alternatingcaps.txt", "w")


# Generate 100 problems multiplying two 2-digit numbers
for _ in range(100):
    n1 = random.choice(list(range(10,100)))
    n2 = random.choice(list(range(10,100)))

    product = n1*n2

    number_eq = str(n1) + " times " + str(n2)
    word_eq = n2t[n1] + " times " + n2t[n2]
    allcaps_eq = n2t[n1].upper() + " times " + n2t[n2].upper()
    alternatingcaps_eq = caps(n2t[n1]) + " times " + caps(n2t[n2])
    
    fo_number.write(str(product) + "\t" + number_eq + "\n")
    fo_word.write(str(product) + "\t" + word_eq + "\n")
    fo_allcaps.write(str(product) + "\t" + allcaps_eq + "\n")
    fo_alternatingcaps.write(str(product) + "\t" + alternatingcaps_eq + "\n")

print(n2t[95])



