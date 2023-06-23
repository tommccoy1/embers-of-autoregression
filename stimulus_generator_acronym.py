



for fi_name, fo_name in [("sentence_outputs/acronyms_first_word.txt", "stimuli/acronym1_word.txt"), ("sentence_outputs/acronyms_first_adversarial.txt", "stimuli/acronym1_adversarial.txt"), ("sentence_outputs/acronyms_first_random.txt", "stimuli/acronym1_random.txt"), ("sentence_outputs/acronyms_second_word.txt", "stimuli/acronym2_word.txt"), ("sentence_outputs/acronyms_second_adversarial.txt", "stimuli/acronym2_adversarial.txt"), ("sentence_outputs/acronyms_second_random.txt", "stimuli/acronym2_random.txt")]: 
    
    fi = open(fi_name, "r")
    fo = open(fo_name, "w")

    count_written = 0
    for line in fi:
        sentence = line.strip().split("\t")[1]

        if "first" in fi_name:
            inp = 'Concatenate together the first letters of all the words in the sequence "' + sentence + '"' 
        else:
            inp = 'Concatenate together the second letters of all the words in the sequence "' + sentence + '"'
        
        fo.write(inp + "\n")
        count_written += 1
        if count_written == 100:
            break








