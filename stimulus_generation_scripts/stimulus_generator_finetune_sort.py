
import jsonlines

fi_examples = open("../examples/sorting_words_examples.txt", "r")
all_in_context_examples = []
for line in fi_examples:
    all_in_context_examples.append(line.strip())
fi_examples.close()


for direction in ["fwd", "rev"]:
    for count in ["10", "100"]:

        fo = open("../stimuli/sorting_" + direction + "_" + count + "shot_finetune.jsonl", "w")
        jsl = jsonlines.Writer(fo)


        n_examples = int(count)

    
        for index, line in enumerate(all_in_context_examples[:n_examples]):

            sentence = line.strip()
            words = sentence.split(", ")
            if direction == "fwd":
                answer = sorted(words)
            else:
                answer = sorted(words)[::-1]
            answer = ", ".join(answer)

            example_dict = {}
            user_dict = {}
            assistant_dict = {}

            # Instruction
            prompt = 'Below is a list of words. Sort the words into alphabetical order.\nOriginal list: "%s"\nSorted list:'


            user_dict["role"] = "user"
            assistant_dict["role"] = "assistant"
            user_dict["content"] = prompt % sentence
            assistant_dict["content"] = answer

            message_list = [user_dict, assistant_dict]
            example_dict["messages"] = message_list

            jsl.write(example_dict)


