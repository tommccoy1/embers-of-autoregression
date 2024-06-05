
import jsonlines


prompt = 'How many words are in the following list? "%s"'
for count in ["5", "10", "100"]:
    fi = open("../examples/counting_words_" + count + "shot.txt", "r")

    fo = open("../stimuli/counting_words_common_" + count + "shot_finetune.jsonl", "w")
    jsl = jsonlines.Writer(fo)
    
    for line in fi:
        example = line.strip()

        example_dict = {}
        user_dict = {}
        assistant_dict = {}

        user_dict["role"] = "user"
        user_dict["content"] = prompt % example

        assistant_dict["role"] = "assistant"
        assistant_dict["content"] = str(len(example.split()))

        message_list = [user_dict, assistant_dict]

        example_dict["messages"] = message_list

        jsl.write(example_dict)


