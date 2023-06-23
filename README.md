
# Stimuli

- The inputs to provide to models are in the directory `stimuli/`
- For now, the only ones that are ready to be run are the ones that start with `rot` (a total of 8 conditions: 4 for rot2 and 4 for rot13)
- Each line in each file should be a totally separate conversation with the model. That is, provide the model with one line from the file, then record its response, then start a completely new conversation in order to process the next line. 

# Miscellaneous notes

Running on GPU:
salloc --nodes=1 --ntasks=16 --mem=20G --time=02:00:00 --gres=gpu:1

Excluding if:
- Violence, death, or sex
- Proper names (except for very common ones, such as names of countries)
- Grammatical errors
- Not a complete sentence


