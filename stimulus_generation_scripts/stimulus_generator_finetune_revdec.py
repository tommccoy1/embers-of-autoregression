
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

        fo = open("../stimuli/revdec_" + prob + "_" + count + "shot_finetune.jsonl", "w")
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
            prompt = 'Below is a sequence of words in reversed order. Provide the original sequence that this sequence was created from. (When the sequence was reversed, punctuation marks were moved along with the words that they were attached to.)\n'
            prompt += 'Reversed text: "%s"\n'
            prompt += 'Original text:'


            user_dict["role"] = "user"
            assistant_dict["role"] = "assistant"
            user_dict["content"] = prompt % reversed_sentence
            assistant_dict["content"] = sentence

            message_list = [user_dict, assistant_dict]
            example_dict["messages"] = message_list

            jsl.write(example_dict)

        fi.close()

