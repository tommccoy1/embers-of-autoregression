
# Stimuli

- The inputs to provide to models are in the directory `stimuli/`
- Each file is in [jsonlines](https://jsonlines.readthedocs.io/en/latest/) format
- For now, the only ones that are ready to be run are the ones that start with `rot` (a total of 8 conditions: 4 for rot2 and 4 for rot13)
- Each line in each file should be a totally separate conversation with the model. That is, provide the model with one line from the file, then record its response, then start a completely new conversation in order to process the next line. 
- These files were produced by running `python stimulus_generator_rot.py`

## UPDATE (July 13)

- We should rerun the "random" conditions for rot2 and rot13 - i.e., `rot13_random.jsonl` and `rot2_random.jsonl` 
- The Pig Latin stimuli are now ready. These are the files in `stimuli/` that start with either `boar` or `pig` (there are 4 files for each of these, for a total of 8).
- The Acronym stimuli are now ready. These are the files in `stimuli/` that start with `acronym` (6 files in total). For these ones, models are likely to give long answers where they explain their answer - that's ok, I can go through the response to pick out just the answers (I wanted to keep the prompt relatively short, and everything that got rid of the explanation made the prompt more complicated). 

# Miscellaneous notes

Running on GPU:
salloc --nodes=1 --ntasks=16 --mem=20G --time=02:00:00 --gres=gpu:1

Excluding if:
- Violence, death, or sex
- Proper names (except for very common ones, such as names of countries)
- Grammatical errors
- Not a complete sentence


# Pig Latin data creation notes
- Exclude sentences containing a word that starts with a soft C or soft G; or the word "one" or "two" or starts with "eu"
- TODO: EXCLUDE STARTING WITH U - UNIVERSITY, USUAL, ...
- Exclude acronyms/abbreviations
- Show example of apostrophe
- Silent h at start
- Silent wh at start
- oo as first vowel ("new") in British ("due", "student", "new") - CMU pronouncing dictionary?

