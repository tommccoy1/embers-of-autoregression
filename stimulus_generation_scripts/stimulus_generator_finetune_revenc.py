
import jsonlines


for prob in ["highprob", "mediumprob", "lowprob"]:
    for count in ["10", "100"]:

        fi = None
        if prob == "highprob":
            fi = open("../examples/sentences_high_probability_train.txt", "r")
        elif prob == "mediumprob":
            fi = open("../examples/sentences_medium_probability_train.txt", "r")
        elif prob == "lowprob":
            fi = open("../examples/sentences_low_probability_train.txt", "r")

        fo = open("../stimuli/revenc_" + prob + "_" + count + "shot_finetune.jsonl", "w")
        jsl = jsonlines.Writer(fo)

    
        for index, line in enumerate(fi):
            if index >= int(count):
                break

            sentence = line.strip()

            example_dict = {}
            user_dict = {}
            assistant_dict = {}

            reversed_sentence = " ".join(sentence.split()[::-1])
        
            # Instruction
            prompt = 'Below is a sequences of words. Provide the sequence that is created when you reverse this sequence. (When the sequence is being reversed, punctuation marks should be moved along with the words that they are attached to.)\n'
            prompt += 'Original text: "%s"\n'
            prompt += 'Reversed text:'


            user_dict["role"] = "user"
            assistant_dict["role"] = "assistant"
            user_dict["content"] = prompt % sentence
            assistant_dict["content"] = reversed_sentence

            message_list = [user_dict, assistant_dict]
            example_dict["messages"] = message_list

            jsl.write(example_dict)

        fi.close()

