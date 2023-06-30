
import json

def find_discrepancy_index(original, adversarial):
    orig_words = original.split()
    adv_words = adversarial.split()

    for index in range(len(orig_words)):
        if orig_words[index] != adv_words[index]:
            return index

fi = open("logs/rot13_highprob_gpt-3.5-turbo_temp=0.0_n=1.json", "r")
data = json.load(fi)

fi2 = open("sentence_outputs/high_probability.txt", "r")
original_sentences = []
for line in fi2:
    original_sentences.append(line.strip())

fi3 = open("sentence_outputs/adversarial.txt", "r")
adversarial_sentences = []
for line in fi3:
    adversarial_sentences.append(line.strip())


count_acc_orig = 0
count_acc_adv = 0

count_wordmatch_orig = 0
count_wordmatch_adv = 0
length_match = 0

word_error_total = 0
words_total = 0

word_error_critical = 0
words_critical_total = 0

for response, original, adv in zip(data["res"], original_sentences[:100], adversarial_sentences[:100]):
    if response[0] == '"':
        response = response[1:]
    if response[-1] == '"':
        response = response[:-1]

    #print(len(response.split()), len(original.split()), len(adv.split()))

    if len(response.split()) == len(original.split()):
        index = find_discrepancy_index(original, adv)
        print(original.split()[index], adv.split()[index], response.split()[index])
        if response.split()[index] == original.split()[index]:
            count_wordmatch_orig += 1
        if response.split()[index] == adv.split()[index]:
            count_wordmatch_adv += 1

        length_match += 1

        for word_correct, word_response in zip(adv.split(), response.split()):
            if word_response != word_correct:
                word_error_total += 1
            words_total += 1

        if response.split()[index] != original.split()[index]:
            word_error_critical += 1
        words_critical_total += 1


    if response == original:
        count_acc_orig += 1
    elif response ==  adv:
        count_acc_adv += 1




print("ORIG", count_acc_orig)
print("ADV", count_acc_adv)

print("")

print("WORDMATCH ORIG", count_wordmatch_orig)
print("WORDMATCH ADV", count_wordmatch_adv)
print("LENGTH MATCH", length_match)

print("")
print("ERRORS OVERALL", word_error_total*1.0/words_total)
print("ERRORS CRITICAL", word_error_critical*1.0/words_critical_total)
