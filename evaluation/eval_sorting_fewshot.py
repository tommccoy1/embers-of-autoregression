
import json
import jsonlines
from Levenshtein import distance


saved_stats = {}
first = True
fi = open("../stimuli/saved_stimuli_statistics.tsv", "r")
index2label = {}
label2index = {}
for line in fi:
    parts = line.strip().split("\t")
    if first:
        for index, label in enumerate(parts):
            index2label[index] = label
            label2index[label] = index
        first = False

    else:
        this_obj = {}
        for index, part in enumerate(parts):
            this_obj[index2label[index]] = part
        saved_stats[this_obj["sentence"]] = this_obj

gemini_tokens = {}
fi = open("../stimuli/saved_gemini_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    gemini_tokens[parts[0]] = parts[1]

llama3_tokens = {}
fi = open("../stimuli/saved_llama3_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    llama3_tokens[parts[0]] = parts[1]



manual_dict = {}

unhandled = 0



for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "claude-3-opus-20240229", "ft_gpt-3.5_10shot", "ft_gpt-3.5_100shot"]:

    for nshot in ["0shot", "5shot", "10shot"]:

        fo_words = open("table_few_sortwords_" + model + "_" + nshot + ".tsv", "w")
        fo_words.write("\t".join(["index", "task", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")


        for direction in ["fwd", "rev"]:
            condition = "sorting_" + direction

            if nshot != "0shot":
                condition = condition + "_" + nshot
            elif nshot == "0shot" and model.startswith("ft"):
                condition = condition + "_" + nshot
            


            if model.startswith("ft") and nshot != "0shot":
                continue

            print("")
            print(model, condition)

            if model == "ft_gpt-3.5_10shot":
                if direction == "fwd":
                    fi = open("../logs/" + condition + "_" + "ft:gpt-3.5-turbo-0613:personal:fwd-10shot:9S9lmcHt" + "_temp=0.0_n=1.json", "r")
                elif direction == "rev":
                    fi = open("../logs/" + condition + "_" + "ft:gpt-3.5-turbo-0613:personal:rev-10shot:9S9uQlp7" + "_temp=0.0_n=1.json", "r")
            elif model == "ft_gpt-3.5_100shot":
                if direction == "fwd":
                    fi = open("../logs/" + condition + "_" + "ft:gpt-3.5-turbo-0613:personal:fwd-100shot:9S9sz3um" + "_temp=0.0_n=1.json", "r")
                elif direction == "rev":
                    fi = open("../logs/" + condition + "_" + "ft:gpt-3.5-turbo-0613:personal:rev-100shot:9S9vpZRp" + "_temp=0.0_n=1.json", "r")
            else:
                fi = open("../logs/" + condition + "_" + model + "_temp=0.0_n=1.json", "r")
            data = json.load(fi)

            count_correct = 0
            count_total = 0
            total_dist = 0

            pairwise_correct = 0
            pairwise_total = 0

            inputs = []
            with jsonlines.open("../stimuli/" + condition + ".jsonl") as reader:
                for obj in reader:
                    inputs.append(obj["input"])

            for index, (inp, gt, res) in enumerate(zip(inputs, data["gts"], data["res"])):
                if gt[0] == '"':
                    gt = gt[1:]
                if gt[-1] == '"':
                    gt = gt[:-1]

                if len(res) > 0:
                    if res[0] == '"':
                        res = res[1:]
                if len(res) > 0:
                    if res[-1] == '"':
                        res = res[:-1]

                res = res.replace("* ", "")
                res = res.replace("- ", "")
                res = ", ".join(res.split("\n"))
                if res in manual_dict:
                    res = manual_dict[res]
            
                res = res.replace("The list of numbers in descending order is as follows:, , ", "").strip()
                res = res.replace("Here is the list of numbers sorted in descending order:", "").strip()
                res = res.replace("**", "")
                res = res.replace("\"", "")
                res = res.replace(" , ", " ")
                res = res.replace(" &rarr; ", ", ")
                res = res.replace("I have sorted the list from largest to smallest. Let me know if you need any further assistance.", "")
                res = res.replace("12 21 55", "122155")
                res = res.replace("If you need any further assistance, please let me know.", "").strip()
                res = res.replace("I have sorted the list from largest to smallest.", "").strip()
                res = res.replace("I have sorted the list using the sort() method with a descending order (reverse=True) and then converted the list to string using the join() method with an empty string as separator.", "").strip()
                res = res.replace("I have sorted the list according to the last digit of each number, in descending order. This will give you the largest and most significant digits first.", "").strip()
                res = res.replace("I have sorted the list using the `sort()` method with a descending order (descendings sort) and a comparison function that compares each pair of elements and returns `True` if the first element is greater than the second element, and `False` otherwise. The `reverse()` method is then used to apply the sort in descending order.", "").strip()
                res = res.replace("Let me know if you need any further assistance.", "").strip()
                res = res.replace("I have sorted the given list of numbers in descending order for you.", "").strip()
                res = res.replace("If you need any further assistance, please don't hesitate to ask!", "").strip()
                res = res.replace("I've sorted the list using the descending order.", "").strip()
                res = res.replace("I have sorted the list using the `sort()` method with a descending order (reverse order) and a comparison function that compares each pair of elements and returns `True` if the first element is greater than the second element, and `False` otherwise. The `reverse()` method is used to apply the sort in descending order.", "").strip()
                res = res.replace("  ", " ")
                res = res.replace("I hope this helps! Let me know if you have any other questions.", "").strip()
                res = res.replace("I have sorted the list according to the largest number first.", "").strip()
                res = res.replace("Sorting the given list of numbers in descending order:", "").strip()
                res = res.replace("If you need the list sorted in ascending order instead, please let me know.", "").strip()
                res = res.replace("I have sorted the list in descending order, which means the largest number is at the beginning of the list, and the smallest number is at the end of the list.", "").strip()
                if res == "66058 (from the input list) 13160 15955 12779 3 7038 8613 6414 9276 435 4728 8613, , 66058 (last number), 13160, 15955, 15954 (next number), 3, 7038, 8613, 8613, 6414, 9276, 4729, 660, 986, 4728, 435, 9275, 12779, 3321, 2409, 6414, 9276, 3, 7038, 8613, 8613":
                    res = "3, 7038, 8613, 8613, 6414, 9276, 4729, 660, 986, 4728, 435, 9275, 12779, 3321, 2409, 6414, 9276, 3, 7038, 8613, 8613"
                if res.strip() == "99845 699 8913 5124 5233 6449 5382 8706 2510 5571 1806 4798 6480 3258 5373 2705 9807,".strip() or res.strip() == "they ungrateful bickering volatile werewolf inquisitive blunder may tenacious people live emergency tempestuous complicit shadowy word my never this what your tempest thisis this that whimsical whimsy whimsicality whimsicalities whimsicality whimsy whims whim whimsey whim wicked wickedness wickedly wickednesses wickedness wicked wickedly wickedly wickedly wicked wickednesses wicked":
                    res = ", ".join(res.split())[:-1]
                res = res.replace("Here is the list of numbers sorted in ascending order:", "").strip()
                res = res.replace("`", "").strip()
                res = res.replace("[", "").strip()
                res = res.replace("]", "").strip()
                res = res.replace("Here's the list of numbers sorted in ascending order:", "").strip()
                res = res.replace("I've sorted the list using the built-in sorted() function in Python. The sorted() function takes a list of numbers as an argument and returns a new list with the numbers sorted in ascending order. In this case, I passed the list of numbers as an argument to the sorted() function, and it returned a new list with the numbers sorted.", "").strip()
                res = res.replace("I sorted the list using the built-in sorted() function in Python. The sorted() function takes a list of numbers as an argument and returns a new list containing the same numbers in ascending order. In this case, I passed the list of numbers as an argument to the sorted() function, and it returned a new list with the same numbers but in ascending order.", "").strip()
                res = res.replace("I have sorted the list using the built-in sorted() function in Python. The sorted() function takes a list of numbers as an argument and returns a new list containing the same numbers in ascending order. In this case, I passed the list of numbers as an argument to the sorted() function, and it returned a new list with the same numbers but in ascending order.", "").strip()
                res = res.replace("here is the list of words sorted in reverse alphabetical order:", "").strip()
                res = res.replace("for (let i = words.length 1; i >= 0; i--) {, const word = wordsi;, if (isAdjective(word) || isVerb(word)) {, continue;, }, return sortByCaseInsensitive(word) || word;, }, return words;, }, function isAdjective(word) {, return adjectiveWords.some(w => word.toLowerCase() === w);, }, function isVerb(word) {, return verbWords.some(w => word.toLowerCase() === w);, }, function sortByCaseInsensitive(word) {, return word.toLowerCase() === word.toLowerCase();, }, function isAdjectiveOrVerb(word) {, return isAdjective(word) || isVerb(word);, }, function isAdjective(word) {", "").strip()
                res = res.replace("for (let i = 0; i < myList.length; i++) {,  let currentWord = myListi;,  let isReverseOrder = myList.slice(i + 1).includes(currentWord);,  if (isReverseOrder === true) {,   myList.splice(i, 1);,  } else {,   i++;,  }, }, myList = myList.sort((a, b) => {,  return b.split(' ').length a.split(' ').length;, });, console.log(myList); // ", "").strip()
                res = res.replace("for (let i = 0; i < words.length; i++) {, for (let j = words.length 1; j > i; j--) {, if (wordsj < wordsi) {, let temp = wordsi;, wordsi = wordsj;, wordsj = temp;, }, }, }, console.log(words); // Output: ", "").strip()
                res = res.replace("Here's the list of words sorted in reverse alphabetical order:", "").strip()
                res = res.replace("The words in this list are sorted from the least alphabetically to the most alphabetically.", "").strip()
                res = res.replace("Here are the same words, sorted in reverse alphabetical order:", "").strip()
                res = res.replace("The words are sorted in reverse order, with the last word being the one closest to the beginning of the alphabet.", "").strip()
                res = res.replace("The words are sorted in reverse alphabetical order, with the last word first (shenanigans) and the first word last (fair).", "").strip()
                res = res.replace("Here are the words sorted in alphabetical order:", "").strip()
                res = res.replace("Here is the list of numbers in descending order:", "").strip()
                res = res.replace("Here is the list of words in reverse alphabetical order:", "").strip()
                res = res.replace("Sorted in reverse alphabetical order:", "").strip()
                res = res.replace("wonderful ,", "wonderful,").strip()
                res = res.replace("Please note that the reverse alphabetical order means that the words will be sorted in ascending order by default, but with a reverse order.", "").strip()
                res = res.replace("The words are sorted in reverse alphabetical order, with the last word being the one closest to the alphabetical end.", "").strip()
                res = res.replace("Here are the words sorted in reverse alphabetical order:", "").strip()
                res = res.replace("The words are now sorted in reverse alphabetical order.", "").strip()
                res = res.replace("The words are sorted in reverse alphabetical order, with the last word being donky, followed by big, evergreen, clean, exalted, normative, fair, better, bountiful, archaic and illegal.", "").strip()
                res = res.replace("The words are sorted in reverse alphabetical order, with the letters of each word arranged in a descending order of the alphabet.", "").strip()
                res = res.replace("The words are sorted in reverse order, so thrash comes before indelible, and stilted comes before hallowed.", "").strip()
                res = res.replace("The words in this list are sorted in reverse alphabetical order. This means that the first word in the list is the most alphabetically distant from cutesy, and the last word in the list is the most alphabetically distant from bittersweet.", "").strip()
                res = res.replace("The words are sorted in reverse alphabetical order, with the letters that are not in the English alphabet or do not appear before the English alphabet letters coming first.", "").strip()
                res = res.replace("here are the words sorted in reverse alphabetical order:", "").strip()
                res = res.replace("Note: Since the list contains multiple words with the same letter, the order of the words with the same letter might not be in alphabetical order.", "").strip()
                res = res.replace("Let me know if you need help with anything else!", "").strip()
                res = res.replace("mercurial, wondrous, special, excitable, our, public, expedited, epistemology, karaoke, serious, open, epistemic, The sorted list in reverse alphabetical order is:", "").strip()
                res = res.replace("Please note that reverse alphabetical order means that the words will be sorted in ascending order by their position in the alphabet, but starting from the last letter.", "").strip()
                res = res.replace("The words are sorted in reverse alphabetical order, with the last word being the one that differs the most from the first word.", "").strip()
                res = res.replace("halted, shoddy, emergency, irreplaceable, made, universal, hasty, shoddy, halted, epiphany, evergreen, incessant, serpentine, audacious, evergreen, nuance, serenity, capricious, evergreen, evergreen, evergreen, The words sorted in reverse alphabetical order are:", "").strip()
                res = res.replace("Please let me know if you need any further assistance or if there is anything else I can help you with.", "").strip()
                res = res.replace("Please note that in reverse alphabetical order, the comes after irrefutable.", "").strip()
                res = res.replace(" and ", " ").strip()
                res = res.replace("Please note that the reverse alphabetical order means that the words will be sorted in ascending order by default, but with a reverse order of the sort key.", "").strip()
                res = res.replace("words sorted in reverse alphabetical order.", "").strip()
                res = res.replace("In this case, haphazard is the word that differs the most from pancake, making it the last word in the list.", "").strip()
                res = res.replace("The words are sorted in reverse alphabetical order, with the last word (big) first, followed by the second-last word (stoic), so on, until the first word (political)", "").strip()
                res = res.replace("for (let i = 0; i < words.length; i++) {, for (let j = words.length 1; j > i; j--) {, if (wordsj < wordsi) {, let temp = wordsj;, wordsj = wordsi;, wordsi = temp;, }, }, }, console.log(words); // Output: happy, new, right, happy, beautiful, mischievous, willful, criminal, flagrant, the, reverse_order = true;, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }, }", "").strip()
                if "Output:" in res:
                    res = res[res.index("Output:")+7:]
                res = res.replace("This code uses a for loop to iterate through the list compare each word with the current word. If the words are not the same", "").strip()
                res = res.replace("The words are sorted in reverse order, so insidious comes before political, shabby comes before big. The others follow alphabetical order, but in reverse.", "").strip()
                if "fake gilded uncontrolled demagogue boomerang modesty bickering touchy human special man hubris monolith" in res:
                    res = ", ".join(res.split())
                res = res.replace("Please note that the reverse alphabetical order starts from the last letter of the word goes backwards.", "").strip()
                res = res.replace("The words are sorted in reverse alphabetical order, with the last word (penguin) first the first word (still) last.", "").strip()
                if "shabby old devious deft disingenuous disfavorably disquieting disregarding disrespectful disquiet disparaging dispassionate displeased displeasedly displeasedness displeasednesses displeasednesses- displeasednesses-of displeasednesses-on displeasednesses-to displeasednesses-with displeasednesses-you displeasednesses-you-are displeasednesses-you-are-not displeasednesses-you-are-not-to displeasednesses-you-are-not-to-be" in res:
                    res = ", ".join(res.split())
                res = res.replace("here are the words in alphabetical order:", "").strip()
                res = res.replace("Here are the words in alphabetical order:", "").strip()
                res = res.replace("still pithy", "").strip()
                res = res.replace("The remaining words remain sorted:", "").strip()
                res = res.replace("'", "").strip()
                res = res.replace("Please note that invoice invoice are considered as the same word in this context.", "").strip()
                res = res.replace("Ive sorted them according to the English alphabet.", "").strip()
                res = res.replace("gallows humor", "gallows, humor").strip()
                res = res.replace("sure, here are the words sorted in alphabetical order:", "").strip()
                res = res.replace("subliminal messages", "subliminal, messages").strip()
                res = res.replace("like, deep, enchantment, experience, extreme, feisty, man, social, transparent, uneventful, willfully, willing, secret, Sorting the given list of words in alphabetical order, the output would be:,", "").strip()
                res = res.replace("Note: The word scruples is already in alphabetical order. The other words were sorted alphabetically to make the list consistent.", "").strip()
                res = res.replace(" (corrected from 6207)", "").strip()
                res = res.replace(" (none of these numbers were in the original list, I assume it was a mistake)", "").strip()
                res = res.replace(" (note: there is no 7791 in the original list, I assume its a typo you meant 779)", "").strip()
                res = res.replace(" (not in the original list, error?)", "").strip()
                res = res.replace(" (none, typo?)", "").strip()
                res = res.replace(" (none in the list)", "").strip()
                res = res.replace("Here is the list of numbers in ascending order:", "").strip()
                res = res.replace("Here is the sorted list in ascending order:", "").strip()
                res = res.replace(" (wait, no... there is no 8192)", "").strip()
                res = res.replace(" (wait, no... there is no 7837 in the original list!)", "").strip()
                res = res.replace(" (wait, no... thats not in the list!)", "").strip()
                res = res.replace(" (wait, no... there is no 4420 in the original list!)", "").strip()
                res = res.replace(" (oops, out of order!)", "").strip()
                res = res.replace("Corrected: ", "").strip()
                res = res.replace("Here is the list of words in alphabetical order:", "").strip()
                res = res.replace("I have tried a variety of ways to sort this list, but I keep getting an error message. Can you help me?, Comment: Sure, Id be happy to help! Heres the sorted list in descending order:", "").strip()
                for letter in "abcdefghijklmnopqrstuvwxyz":
                    res = res.replace(letter.upper() + ") ", "").strip()
                res = res.replace("Therefore, the correct answer is:", "").strip()
                res = res.replace("The correct order is:", "").strip()
                res = res.replace("Here is the list sorted in descending order:", "").strip()
                res = res.replace("The list of numbers in descending order is:", "").strip()
                res = res.replace("Answer: Sure! Heres the list of numbers in descending order:", "").strip()
                res = res.replace("Answer: Sure! ", "").strip() 
                res = res.replace("I need to sort the list in descending order, so the largest number should be at the bottom of the list., Heres the sorted list:", "").strip()
                res = res.replace(" Is this correct?", "").strip()
                res = res.replace("To sort the list of numbers in descending order, we can use the following steps:, Identify the largest number in the list, which is 8538., Place the number 8538 at the end of the list., Identify the next largest number in the list, which is 7885., Place the number 7885 at the end of the list, but before 8538., Identify the next largest number in the list, which is 6445., Place the number 6445 at the end of the list, but before 7885., Continue this process until all numbers have been placed in descending order., Here is the sorted list of numbers in descending order:", "").strip()
                if "Here is the sorted list of numbers in descending order:" in res:
                    res = res[res.index("Here is the sorted list of numbers in descending order:")+len("Here is the sorted list of numbers in descending order:"):]
                res = res.replace("Answer: Sure, heres the list of numbers in descending order:", "").strip()
                res = res.replace("The list can be sorted in descending order as follows:", "").strip()
                res = res.replace("Here are the numbers in descending order:", "").strip()
                res = res.replace("I need to sort the list in descending order., Answer: Sure, heres the sorted list of numbers in descending order:", "").strip()
                res = res.replace("I need to know the sorted list of numbers in descending order., Heres the sorted list of numbers in descending order:", "").strip()
                res = res.replace("How do I do this?, Answer:, Heres the list of numbers in descending order:", "").strip()
                res = res.replace("I need to get the list sorted in descending order., ", "").strip()
                res = res.replace("I hope that helps! Let me know if you have any other questions.", "").strip() 
                res = res.replace("Im not sure how to sort the list of numbers in descending order. Can you help me?, Sure, Id be happy to help! Heres the list of numbers you provided, sorted in descending order:", "").strip()
                res = res.replace("The sorted list in descending order is:", "").strip()
                res = res.replace("The numbers in the list in descending order are:", "").strip()
                res = res.replace("Im not sure how to do this, can you please help me?, Comment: Sure, I can help you with that! Heres the list of numbers you provided, sorted in descending order:", "").strip()
                res = res.replace("Answer:", "").strip()
                res = res.replace("The number 1417 should be at the top of the list the number 61 should be at the bottom.", "").strip()
                res = res.replace("Here are the numbers you provided, sorted in descending order:", "").strip()
                res = res.replace("Here is the sorted list for the last set of words:", "").strip()
                res = res.replace("Here is the last list sorted in reverse alphabetical order:", "").strip()

                
                res = res.replace("  ", " ").strip()

                if len(res) > 0:
                    if res[0] == ",":
                        res = res[1:].strip()
                if len(res) > 0:
                    if res[-1] == ",":
                        res = res[:-1].strip()

                for list_index in range(30):
                    res = res.replace(str(list_index) + ". ", "")
                res = res.replace(".", "").strip()
               
                words_gt = gt.split(", ")
                words_res = res.split(", ")

                for index1, word1 in enumerate(words_gt[:-1]):
                    for index2, word2 in enumerate(words_gt[index1+1:]):
                        if word1 not in words_res or word2 not in words_res:
                            correct = False
                        else:
                            index1_res = words_res.index(word1)
                            index2_res = words_res.index(word2)

                            if index1_res < index2_res:
                                correct = True
                            else:
                                correct = False

                        if correct:
                            pairwise_correct += 1
                        pairwise_total += 1
                        


 
                dist = distance(gt.split(), res.split())
                total_dist += dist

               

                if gt in res:
                    if len(res.split(", ")) == len(gt.split(", ")):
                        count_correct += 1
                        correct_answer = "1"

                    if len(res.split(", ")) != len(res.split(" ")):
                        print(gt)
                        print(res)
                        print("")
                        unhandled += 1

                else:
                    correct_answer = "0"
                    if len(res.split(", ")) != len(res.split(" ")):
                        print(gt)
                        print(res)
                        print("")
                        unhandled += 1
                        if len(res.split(" ")) != len(res.split(", ")) and "llama-3" in model:
                            #print(gt)
                            #print(res)
                            #print("")
                            pass
                    # Uncomment to show errors
                    if model == "gpt-4-0613" and len(words_gt) == 13 and "rev" in condition and distance(gt.split(), res.split()) > 2:
                        #print(gt)
                        #print(res)
                        #print(inp)
                        #print("")
                        pass
                    pass

                if inp.startswith("big, evergreen") and model == "gpt-4-0613":
                    #print(gt)
                    #print(res)
                    #print(inp)
                    #print("")
                    pass

                count_total += 1


                if "gpt" in model:
                    data = [str(index), direction, saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct_answer]
                elif model == "llama-3-70b-chat-hf":
                    data = [str(index), direction, saved_stats[inp]["n_characters"], llama3_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], llama3_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct_answer]
                elif model == "gemini-1.0-pro-001":
                    data = [str(index), direction, saved_stats[inp]["n_characters"], gemini_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], gemini_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct_answer]
                elif model == "claude-3-opus-20240229":
                    data = [str(index), direction, saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"],
                            saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct_answer]
                else:
                    #pass
                    14/0


                if direction in ["fwd", "rev"]:
                    fo_words.write("\t".join(data) + "\n")
                elif direction in ["ascending", "descending"]:
                    fo_numbers.write("\t".join(data) + "\n")


            print(direction, condition, "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, "pairwise:", pairwise_correct*1.0/pairwise_total, pairwise_correct, pairwise_total)


print(unhandled)
