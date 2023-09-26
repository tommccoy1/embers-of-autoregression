

import random


def conversion_actual(x):
    return 9.0/5.0*x + 32.0


def conversion_fake(x):
    return 7.0/5.0*x + 31.0


def conversion_actual_inverse(x):
    return round((x - 32.0)*5/9)

def conversion_fake_inverse(x):
    return round((x - 31.0)*5/7)


fo_actual = open("../examples/conversion_actual.txt", "w")
fo_fake = open("../examples/conversion_fake.txt", "w")

fo_actual_inverse = open("../examples/conversion_actualinverse.txt", "w")
fo_fake_inverse = open("../examples/conversion_fakeinverse.txt", "w")


for _ in range(100):
    number_inp = random.choice(list(range(1000)))
    outp_actual = conversion_actual(number_inp)
    outp_fake = conversion_fake(number_inp)


    fo_actual.write(str(number_inp) + "\t" + "{:.1f}".format(outp_actual) + "\n")
    fo_fake.write(str(number_inp) + "\t" + "{:.1f}".format(outp_fake) + "\n")

for _ in range(100):
    found = False

    while not found:
        number_outp = random.choice(list(range(1000)))
        inp_actual_inverse = conversion_actual_inverse(number_outp)
        inp_fake_inverse = conversion_fake_inverse(number_outp)

        if round(conversion_actual(inp_actual_inverse)) == number_outp and round(conversion_fake(inp_fake_inverse)) == number_outp and inp_actual_inverse > 0 and inp_fake_inverse > 0:
            found = True

    fo_actual_inverse.write(str(inp_actual_inverse) + "\t" + str(number_outp) + "\n")
    fo_fake_inverse.write(str(inp_fake_inverse) + "\t" + str(number_outp) + "\n")







