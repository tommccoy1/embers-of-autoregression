

from nltk.tokenize import sent_tokenize, word_tokenize
import math

# Articles to extract sentences from
filenames = ["turtles_16jun2023",
             "erdogan_15jun2023",
             "wildfires_14jun2023",
             "chavez_14jun2023",
             "mariupol_14jun2023",
             "poetry_14jun2023",
             "thailand_13jun2023",
             "jersey_13jun2023",
             "zimbabwe_13jun2023",
             "kazakhstan_13jun2023",
             "fresno_12jun2023",
             "everest_12jun2023",
             "nyelade_12jun2023",
             "belize_12jun2023",
             "climate_12jun2023",
             "jaguar_10jun2023",
             "taiwan_09jun2023",
             "oleshky_09jun2023",
             "indonesia_09jun2023",
             "kyrgyzstan_09jun2023",
             "trinidad_09jun2023",
             "montalvo_08jun2023",
             "counter_08jun2023",
             "unfreedom_08jun2023",
             "uganda_08jun2023",
             "ngos_07jun2023",
             "hongkong_07jun2023",
             "spain_07jun2023",
             "sidorenko_07jun2023",
             "ukraine_07jun2023",
             "serbia_06jun2023",
             "divisions_06jun2023",
             "boomerang_06jun2023",
             "ecuador_06jun2023",
             "spread_06jun2023",
             "tajikistan_06jun2023",
             "srilanka_06jun2023",
             "donuts_05jun2023",
             "migration_05jun2023",
             "unfreedom_05jun2023",
             "amazigh_05jun2023",
             "taiwan_05jun2023",
             "swatch_04jun2023",
             "hongkong_04jun2023",
             "atlantic_03jun2023",
             "graduation_03jun2023",
             "turkey_03jun2023",
             "moldova_02jun2023",
             "unions_02jun2023",
             "marathon_02jun2023"
             ]

# Compute the minimum log probability for each sentence
# in each of these files
count_1 = 0
count_2 = 0
for filename in filenames:
    fi = open("global_voices/" + filename + ".txt", "r")
    for line in fi:

        # Split into sentences
        sentences = sent_tokenize(line)

        for sentence in sentences:
            words = word_tokenize(sentence)
            count_articles = 0
            for word in words:
                if word in ["a", "an", "the"]:
                    count_articles += 1

            if count_articles == 1:
                count_1 += 1
            elif count_articles > 1:
                count_2 += 1


print("count_1", count_1)
print("count_2", count_2)


