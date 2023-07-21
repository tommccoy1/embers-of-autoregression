

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

fi1 = open("../examples/counting_words_common.txt", "r")
fi2 = open("../examples/counting_words_rare.txt", "r")

for line1, line2 in zip(fi1, fi2):
    words1 = line1.strip().split()
    words2 = line2.strip().split()


    for word1, word2 in zip(words1, words2):
        if len(word1) != len(word2):
            print("ERROR: MISMATCHED LENGTHS", word1, word2)
    
        tokens1 = enc.encode(word1)
        tokens2 = enc.encode(word2)

        signature1 = ""
        signature2 = ""

        for token1 in tokens1:
            signature1 = signature1 + str(len(enc.decode([token1])))
            
        for token2 in tokens2:
            signature2 = signature2 + str(len(enc.decode([token2])))

        if signature1 != signature2:
            print(signature1, signature2)


