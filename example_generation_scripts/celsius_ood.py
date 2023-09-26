

import random


def conversion_actual(x):
    return 9.0/5.0*x + 32.0


def conversion_fake(x):
    return 7.0/5.0*x + 31.0


def conversion_actual_inverse(x):
    return round((x - 32.0)*5/9)

def conversion_fake_inverse(x):
    return round((x - 31.0)*5/7)

def int_divis_10(num):
    if int(num) == num:
        if str(int(num)).endswith("0"):
            return True

    return False

fo_actual = open("../examples/conversion_ood_actual.txt", "w")
fo_fake = open("../examples/conversion_ood_fake.txt", "w")

fo_actual_inverse = open("../examples/conversion_ood_actualinverse.txt", "w")
fo_fake_inverse = open("../examples/conversion_ood_fakeinverse.txt", "w")


for _ in range(100):
    found = False
    while not found:
        number_inp = random.choice(list(range(501,1000)))
        outp_actual = conversion_actual(number_inp)
        outp_fake = conversion_fake(number_inp)

        if (not int_divis_10(number_inp)) and (not int_divis_10(outp_actual)) and (not int_divis_10(outp_fake)):
            found = True

    fo_actual.write(str(number_inp) + "\t" + "{:.1f}".format(outp_actual) + "\n")
    fo_fake.write(str(number_inp) + "\t" + "{:.1f}".format(outp_fake) + "\n")

for _ in range(100):
    found = False

    while not found:
        number_outp = random.choice(list(range(501,1000)))
        inp_actual_inverse = conversion_actual_inverse(number_outp)
        inp_fake_inverse = conversion_fake_inverse(number_outp)

        if round(conversion_actual(inp_actual_inverse)) == number_outp and round(conversion_fake(inp_fake_inverse)) == number_outp and inp_actual_inverse > 0 and inp_fake_inverse > 0 and (not int_divis_10(number_outp)) and (not int_divis_10(inp_actual_inverse)) and (not int_divis_10(inp_fake_inverse)):
            found = True

    fo_actual_inverse.write(str(inp_actual_inverse) + "\t" + str(number_outp) + "\n")
    fo_fake_inverse.write(str(inp_fake_inverse) + "\t" + str(number_outp) + "\n")







