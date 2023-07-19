
fi = open("sentence_outputs/two_articles.txt", "r")
fo_plain = open("sentence_outputs/articles_base.txt", "w")
fo_next = open("sentence_outputs/articles_next.txt", "w")
fo_prev = open("sentence_outputs/articles_prev.txt", "w")
for line in fi:
    words = line.strip().split()
    
    for word in words:
        if word.lower() in ["a", "an", "the"] and word not in ["a", "an", "the"]:
            print(line)

    # Skip if second word is an article, so we don't have to
    # worry about sentence-initial capitalization
    if words[1] not in ["a", "an", "the"]:
        avoid_sentence = False

        next_words = []
        skip = False
        for index, word in enumerate(words):
            if skip:
                skip = False
            elif word in ["a", "an", "the"]:
                next_word = words[index+1]
                if next_word.isalpha():
                    next_words.append(words[index+1])
                    next_words.append(word)
                elif next_word[-1] in [".", ",", "?"]:
                    next_words.append(next_word[:-1])
                    next_words.append(word + next_word[-1])
                else:
                    print(next_word)
                    avoid_sentence = True
                skip = True
            else:
                next_words.append(word)

        prev_words = []
        skip = False
        for index, word in enumerate(words):
            if skip:
                skip = False
            elif index == len(words) - 1:
                prev_words.append(word)
            elif words[index+1] in ["a", "an", "the"]:
                next_word = words[index+1]
                if word.isalpha():
                    prev_words.append(next_word)
                    prev_words.append(word)
                else:
                    print(word)
                    avoid_sentence = True
                skip = True
            else:
                prev_words.append(word)


        if not avoid_sentence:
            fo_plain.write(line)
            fo_next.write(" ".join(next_words) + "\n")
            fo_prev.write(" ".join(prev_words) + "\n")

        

