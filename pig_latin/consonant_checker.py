

from nltk.tokenize import sent_tokenize, word_tokenize

fi = open("/Users/tommccoy/Documents/tommccoy/xword_programs/cmudict.txt", "r", encoding="latin")

cmu = {}
for line in fi:
    parts = line.strip().split("\t")
    cmu[parts[0].lower()] = parts[1].replace("0", "").replace("1", "").replace("2", "")

ignorable = [".", ",", "'", "?", "!", ":", ";", "’", "—", "–"]

def contains_vowel(word):
    vowels = ["a", "e", "i", "o", "u"]
    for vowel in vowels:
        if vowel in word:
            return True

    if "y" in word[1:]:
        return True

def first_cluster(word):
    index_vowel = 0
    while (index_vowel > 0 and word[index_vowel] not in ["a", "e", "i", "o", "u", "y"]) or (index_vowel == 0 and word[index_vowel] not in ["a", "e", "i", "o", "u"]):
        index_vowel += 1

    return word[:index_vowel]

cmu_vowels = ["AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"]
def first_cluster_cmu(word):
    index_vowel = 0
    phonemes = cmu[word].split()
    while phonemes[index_vowel] not in cmu_vowels:
        index_vowel += 1

    return phonemes[:index_vowel]

def first_vowel_cmu(word):
    index_vowel = 0
    phonemes = cmu[word].split()
    while phonemes[index_vowel] not in cmu_vowels:
        index_vowel += 1

    return phonemes[index_vowel]

manually_verified_british_y = ["boosts", "boot", "crucial", "do", "doing", "food", "group", "groups", "loom", "looms", "looming", "move", "movements", "moving", "room", "root", "rule", "rules", "ruling", "rune", "runes", "soon", "through", "throughout", "to", "too", "truly", "truth", "you"]
manually_verified = ["n't", "instagram", "'s", "headscarf", "ethnicities", "unlevel", "steamships", "impactful", "optimisation", "kyrgyz", "digitisation", "fundraise", "ll", "didn", "“", "”", "fandom", "scholarships", "poetical", "offsite", "limpet", "mooing", "equably", "leasers", "risible", "versified", "measurers", "busying"] + manually_verified_british_y 

phoneme_dict = {}
phoneme_dict["B"] = ["b"]
phoneme_dict["D"] = ["d"]
phoneme_dict["F"] = ["f"]
phoneme_dict["G"] = ["g"]
phoneme_dict["HH"] = ["h"]
phoneme_dict["JH"] = ["j"]
phoneme_dict["K"] = ["c", "k"]
phoneme_dict["L"] = ["l"]
phoneme_dict["M"] = ["m"]
phoneme_dict["N"] = ["n"]
phoneme_dict["P"] = ["p"]
phoneme_dict["R"] = ["r"]
phoneme_dict["S"] = ["s"]
phoneme_dict["T"] = ["t"]
phoneme_dict["V"] = ["v"]
phoneme_dict["W"] = ["w"]
phoneme_dict["Y"] = ["y"]
phoneme_dict["Z"] = ["z"]

cluster_dict = {}
cluster_dict[("CH",)] = ["ch"]
cluster_dict[("DH",)] = ["th"]
cluster_dict[("TH",)] = ["th"]
cluster_dict[("SH",)] = ["sh"]
cluster_dict[("W",)] = ["wh"]
cluster_dict[("R",)] = ["wr", "rh"]
cluster_dict[("N",)] = ["kn"]
cluster_dict[("TH", "R",)] = ["thr"]
cluster_dict[("TH", "W",)] = ["thw"]
cluster_dict[("F",)] = ["ph"]
cluster_dict[("K", "R",)] = ["chr"]
cluster_dict[("S", "F",)] = ["sph"]

def phonemes_match_letters(word):

    phoneme_cluster = first_cluster_cmu(word)
    letter_cluster = first_cluster(word)

    if phoneme_cluster == []:
        return True
    elif len(phoneme_cluster) == len(letter_cluster):
        all_match = True
        for phoneme, letter in zip(phoneme_cluster, letter_cluster):
            if letter not in phoneme_dict[phoneme]:
                all_match = False
        
        if all_match:
            return True
        else:
            return False
    elif tuple(phoneme_cluster) in cluster_dict:
        if letter_cluster in cluster_dict[tuple(phoneme_cluster)]:
            return True
        else:
            return False
    else:
        return False

fi_list = ["high_probability_piglatin.txt", "low_probability_piglatin.txt", "adversarial_piglatin.txt"]
fi2 = open("sentence_outputs/adversarial_piglatin.txt", "r")
for filename in fi_list:
    fi = open("sentence_outputs/" + filename, "r")
    for line in fi:
        words = word_tokenize(line.lower().strip())

        for index, word in enumerate(words):
            if word in ignorable:
                continue

            if word in manually_verified:
                pass
            elif word not in cmu:
                print("NOT IN CMU", word)
            elif not contains_vowel(word):
                if index != 0 and words[index-1] in ["'", "’"] and word in ["m", "s", "t", "ll"]:
                    pass
                else:
                    print("NO VOWEL", word, words[index-1])
        
            elif first_vowel_cmu(word) == "UW":
                print("OO", word)
            else:
                if phonemes_match_letters(word):
                    #print("GOOD", word)
                    pass
                else:
                    print("BAD", word)


