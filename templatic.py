
import random

adjectives = ["ambidextrous",
              "bellicose",
              "capricious",
              "debonair",
              "grandiloquent",
              "hoity-toity",
              "iconoclastic",
              "jingoistic",
              "klutzy",
              "loquacious",
              "magnanimous",
              "narcissistic",
              "officious",
              "pugnacious",
              "querulous",
              "supercilious",
              "ultracrepidarian",
              "vainglorious",
              "wily",
              "zealous"
              ]

nouns = ["aardvark",
         "badger",
         "coelacanth",
         "dugong",
         "echidna",
         "fennec",
         "gazelle",
         "hedgehog",
         "iguana",
         "kingfisher",
         "lemur",
         "mongoose",
         "peacock",
         "quail",
         "raven",
         "tiger",
         "vulture",
         "walrus",
         "yak",
         "zebra"
        ]

verbs = ["accompanied",
         "beguiled",
         "confronted",
         "defrauded",
         "enlightened",
         "flattered",
         "galvanized",
         "healed",
         "introduced",
         "jinxed",
         "lambasted",
         "mollified",
         "nominated",
         "perplexed",
         "questioned",
         "revealed",
         "tricked",
         "upbraded",
         "vilified",
         "welcomed",
        ]


fo = open("sentence_outputs/templatic.txt", "w")
for _ in range(112):
    found = False

    while not found:
        words = ["The", random.choice(adjectives), random.choice(nouns), random.choice(verbs), "the", random.choice(adjectives), random.choice(nouns)]
        if len(list(set(words))) == len(words):
            found = True

    sentence = " ".join(words) + "."
    fo.write(sentence + "\n")








