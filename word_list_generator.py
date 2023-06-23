
from nltk.corpus import wordnet as wn

vocab = {}
for synset in wn.all_synsets():
    lemmas = synset.lemmas()

    for lemma in lemmas:
        name = lemma.name()
        if name.isalpha() and name.islower():
            if name not in vocab:
                vocab[name] = 1

fo = open("sentence_outputs/vocab.txt", "w")
for word in vocab:
    fo.write(word + "\n")

