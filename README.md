

# To-do

1. Update .gitignore


# Shift ciphers

## Example generation
- High-probability sentences: Created by `example_generation_scripts/sentences_high_probability.py`. Then used the top 100 after manually filtering to remove ones that:
    - Mentioned violence, death, or sex
    - Included proper names  (except for very common ones, such as names of countries)
    - Had grammatical errors
    - Were not complete sentences
- Medium-probability sentences: Created by `example_generation_scripts/sentences_medium_probability.py`. This generates 20 candidates; we manually selected the first (i.e., highest-perplexity) candidate that was grammatically correct (even if semantically odd). For a few sentences, we had to re-run the script to generate additional candidates because none of the 20 that were generated were grammatical; in some cases, we combined parts of two candidates in order to produce a grammatical sentence.
- Low-probability sentences: Created by `example_generation_scripts/sentences_low_probability.py`.
- Adversarial sentences: Copied the high-probability sentences into a new file, and then manually edited each line to replace a single word with another word that was grammatical but unlikely in that context. The new word was selected to be one that had a Levenshtein edit distance of either 1 or 2 from the word being replaced (where each edit could be a single-letter insertion, deletion, or substitution).

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_rot_encode.py`, `stimulus_example_generation/stimulus_generator_rot_decode.py`, and `stimulus_example_generator/stimulus_generator_shift.py`

## Model testing
- Run these commands:
```
# Rot-13
python run_openai.py --tasks rot13enc,rot13dec,rot2enc,rot2dec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200  --model gpt-4
python run_openai.py --tasks rot13enc,rot13dec,rot2enc,rot2dec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200  --model gpt-3.5-turbo

# Other shifts
python run_openai.py --tasks shift --conditions 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25 --max_tokens 200  --model gpt-4
python run_openai.py --tasks shift --conditions 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25 --max_tokens 200  --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_rot13.py
python eval_rot13_adversarial.py
python eval_shift.py 
```

## Statistics
To compute summary statistics about the stimulus sets:
```
python stimuli_statistics.py --fi rot13enc_highprob.jsonl 
python stimuli_statistics.py --fi rot13enc_mediumprob.jsonl 
python stimuli_statistics.py --fi rot13enc_lowprob.jsonl 
python stimuli_statistics.py --fi rot13enc_adversarial.jsonl 

python stimuli_statistics.py --fi rot13dec_highprob.jsonl 
python stimuli_statistics.py --fi rot13dec_mediumprob.jsonl
python stimuli_statistics.py --fi rot13dec_lowprob.jsonl 
python stimuli_statistics.py --fi rot13dec_adversarial.jsonl

python stimuli_statistics.py --fi rot2enc_highprob.jsonl
python stimuli_statistics.py --fi rot2enc_mediumprob.jsonl 
python stimuli_statistics.py --fi rot2enc_lowprob.jsonl
python stimuli_statistics.py --fi rot2enc_adversarial.jsonl 

python stimuli_statistics.py --fi rot2dec_highprob.jsonl
python stimuli_statistics.py --fi rot2dec_mediumprob.jsonl 
python stimuli_statistics.py --fi rot2dec_lowprob.jsonl 
python stimuli_statistics.py --fi rot2dec_adversarial.jsonl 
```

To produce data for regressions in R:
```
python tsv_rot13.py 
python tsv_rot13and2.py 
```

The actual regressions were run in the notebook `Regressions.ipynb`.



# Reversal task

## Example generation
- This task uses the same examples as the rot-13 task.

## Stimulus generation
- Done with `stimulus_generator_reverse_encode.py` and `stimulus_generator_reverse_decode.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks revenc,revdec --conditions highprob,mediumprob,lowprob,adversarial --model gpt-4
python run_openai.py --tasks revenc,revdec --conditions highprob,mediumprob,lowprob,adversarial --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_reverse.py
```

## Statistics
To compute summary statistics about the stimulus sets:
```
python stimuli_statistics.py --fi revenc_highprob.jsonl 
python stimuli_statistics.py --fi revenc_mediumprob.jsonl 
python stimuli_statistics.py --fi revenc_lowprob.jsonl 
python stimuli_statistics.py --fi revenc_adversarial.jsonl 

python stimuli_statistics.py --fi revdec_highprob.jsonl 
python stimuli_statistics.py --fi revdec_mediumprob.jsonl
python stimuli_statistics.py --fi revdec_lowprob.jsonl 
python stimuli_statistics.py --fi revdec_adversarial.jsonl

```

To produce the data for use in R:
```
python tsv_reverse.py
```

The actual regressions were run in the notebook `Regressions.ipynb`.



# Pig Latin and Boar Etruscan tasks

## Example generation
- High-probability sentences: Created by `example_generation_scripts/piglatin_high_probability.py`. The results were then manually filtered for the same criteria as the Rot-13 sentences, as well as the criteria specified below about initial consonant clusters; we then used the first 100 (i.e., 100 lowest perplexity) remaining examples.
- Medium-probability sentences: Created by `example_generation_scripts/piglatin_medium_probability.py`, using the same basic approach as the medium-probability sentences for rot-13.
- Adversarial sentences: Created in the same way as the rot-13 adversarial sentences.
- Pig Latin is primarily a spoken game. Since English spelling often differs from pronuncation, this means that the Pig Latin treatment of many written words is ambiguous. E.g., should "union" become "unionay" or "unionyay"? Should "hour" become "houray" or "ourhay"? To check for such cases, we excluded words whose first written consonant cluster did not parallel their first spoken consonant cluster. In addition, for each word whose first vowel was [u], we checked the word's British pronunciation in the online Cambridge dictionary (https://dictionary.cambridge.org/) to see if it was pronounced with an unwritten /j/ (e.g., "new" is pronounced /nju/); if so, we excluded it. Checking for such words was done with the aid of the CMU pronouncing dictionary. To replicate this checking:
```
wget https://raw.githubusercontent.com/Alexir/CMUdict/master/cmudict-0.7b
mv cmudict-0.7b cmudict.txt
python piglatin_consonant_check.py
```
- Low-probability sentences: Created by `example_generation_scripts/piglatin_low_probability.py`.

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_piglatin_encode.py` and `stimulus_example_generation/stimulus_generator_piglatin_decode.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks pigenc_ay,pigdec_ay,pigenc_uv,pigdec_uv --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-4
python run_openai.py --tasks pigenc_ay,pigdec_ay,pigenc_uv,pigdec_uv --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-3.5-turbo

python run_openai.py --tasks pigenc_way,pigdec_way,pigenc_yay,pigdec_yay,pigenc_hay,pigdec_hay,pigenc_say,pigdec_say --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-4
python run_openai.py --tasks pigenc_way,pigdec_way,pigenc_yay,pigdec_yay,pigenc_hay,pigdec_hay,pigenc_say,pigdec_say --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_pig_boar.py
python eval_pig_prob.py
```

## Statistics
To compute summary statistics about the stimulus sets:
```
python stimuli_statistics.py --fi pigenc_ay_highprob.jsonl 
python stimuli_statistics.py --fi pigenc_ay_mediumprob.jsonl 
python stimuli_statistics.py --fi pigenc_ay_lowprob.jsonl 
python stimuli_statistics.py --fi pigenc_ay_adversarial.jsonl 

python stimuli_statistics.py --fi pigdec_ay_highprob.jsonl 
python stimuli_statistics.py --fi pigdec_ay_mediumprob.jsonl
python stimuli_statistics.py --fi pigdec_ay_lowprob.jsonl 
python stimuli_statistics.py --fi pigdec_ay_adversarial.jsonl

python stimuli_statistics.py --fi pigenc_uv_highprob.jsonl
python stimuli_statistics.py --fi pigenc_uv_mediumprob.jsonl 
python stimuli_statistics.py --fi pigenc_uv_lowprob.jsonl
python stimuli_statistics.py --fi pigenc_uv_adversarial.jsonl 

python stimuli_statistics.py --fi pigdec_uv_highprob.jsonl
python stimuli_statistics.py --fi pigdec_uv_mediumprob.jsonl 
python stimuli_statistics.py --fi pigdec_uv_lowprob.jsonl 
python stimuli_statistics.py --fi pigdec_uv_adversarial.jsonl 



python stimuli_statistics.py --fi pigdec_way_highprob.jsonl
python stimuli_statistics.py --fi pigdec_yay_highprob.jsonl
python stimuli_statistics.py --fi pigdec_hay_highprob.jsonl
python stimuli_statistics.py --fi pigdec_say_highprob.jsonl

python stimuli_statistics.py --fi pigenc_way_highprob.jsonl
python stimuli_statistics.py --fi pigenc_yay_highprob.jsonl
python stimuli_statistics.py --fi pigenc_hay_highprob.jsonl
python stimuli_statistics.py --fi pigenc_say_highprob.jsonl
```

To generate the data that is read in by R:
```
python tsv_pig.py
python tsv_pig_boar.py
python tsv_pig_prob.py
```

The regressions were carried out in `Regressions.ipynb`.



# Acronym task

## Example generation
- First, produce candidate word lists. This was done as follows:
```
# Download wikitext-103
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip
unzip wikitext-103-v1.zip

# Find all words that appear in the CMU Pronouncing Dictionary that are 2 tokens long 
# in uppercase (whether or not there is a space before them), and similarly for 
# lowercase; this produces one file for uppercase and one for lowercase, 
# both sorted by the probability assigned to them by GPT-2. This code assumes you have
# already downloaded the CMU pronouncing dictionary, as described above under Pig Latin.
cd example_generation_scripts
python probability_cmu.py

# We then manually removed any words in the lists that included profanity
```

- Then, generate acronyms using `example_generation_scripts/acronym.py`. This controls for split points: that is, for a given line index, all generated acronym files will have at that index an output word that has the same split point as all other files do, and each input word will have the same split point as the input words at the same position in all other files. The split point is the index where the first subword token ends.
- To check that the inputs and outputs match, and that the break points are correctly controlled for, we ran `python acronym_check.py` in `example_generation_scripts/- A note about the filenames: "1" means highest probability, "5" means lowest. Each file has a 2-digit tag indicating first the output probability then the input probability. E.g., `acronym1_51` means very low-probability outputs and very high-probability inputs.

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_acronym.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks acronym1 --conditions 11,12,13,14,15,21,31,41,51  --max_tokens 100 --model gpt-4 
python run_openai.py --tasks acronym1 --conditions 11,12,13,14,15,21,31,41,51  --max_tokens 100 --model gpt-3.5-turbo

python run_openai.py --tasks acronym2 --conditions 11  --max_tokens 100 --model gpt-4 
python run_openai.py --tasks acronym2 --conditions 11  --max_tokens 100 --model gpt-3.5-turbo
```

Compute statistics about the stimuli, inside `stimuli/':
```
python stimuli_statistics_acronym.py --fi acronym1_11.jsonl 
python stimuli_statistics_acronym.py --fi acronym1_21.jsonl
python stimuli_statistics_acronym.py --fi acronym1_31.jsonl
python stimuli_statistics_acronym.py --fi acronym1_41.jsonl
python stimuli_statistics_acronym.py --fi acronym1_51.jsonl

python stimuli_statistics_acronym.py --fi acronym1_12.jsonl
python stimuli_statistics_acronym.py --fi acronym1_13.jsonl
python stimuli_statistics_acronym.py --fi acronym1_14.jsonl
python stimuli_statistics_acronym.py --fi acronym1_15.jsonl

python stimuli_statistics_acronym.py --fi acronym2_11.jsonl

```

- Then, inside `evaluation/`:
```
python eval_acronym.py 
```

## Statistics
The regressions were performed in the notebook `Regressions.py`.










# BELOW HERE IS OLD STUFF


# Counting task

## Example generation

```
# Create a file listing all words in the CMU Pronouncing Dictionary that appear at least 
# 20 times in Wikitext, ordered by log probability determined by GPT_2.
# Additional restriction: must be 1, 2, or 3 tokens long when tokenized by GPT-4's tokenizer

# Download CMU Pronouncing Dictionary
wget https://raw.githubusercontent.com/Alexir/CMUdict/master/cmudict-0.7b
mv cmudict-0.7b cmudict.txt

# Download wikitext-103
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip
unzip wikitext-103-v1.zip

# Get logprob for each words
python score_cmu_words.py

# Then create lists of candidate common and rare words: 1000 for each token count (1, 2, or 3)
python counting_candidate_words.py 
# After this, we manually filtered the candidates, down to 150 of each token count

# Count how often each number appears
python counting_numbers.py

# Create examples: 30 for each number 1 to 100, made from common or rare words; matching the tokenization
# splits and word lengths across common and rare words
python counting_words.py
python counting_chars.py

# Create examples that also vary whether the output number is common or rare
python counting_words_frequency.py
python counting_chars_frequency.py
```

## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_counting.py` and `stimulus_generation_scripts/stimulus_generator_counting_frequency.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks counting_chars,counting_words --conditions common,rare,common_common,common_rare,rare_common,rare_rare --max_tokens 25 --model gpt-4
python run_openai.py --tasks counting_chars,counting_words --conditions common,rare,common_common,common_rare,rare_common,rare_rare --max_tokens 25 --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_counting.py
python eval_counting_frequency.py
```



## Statistics
To compute summary statistics about the stimulus sets:
```
# Get character counts
python counting_character_counts.py

python stimuli_statistics_counting.py --fi counting_chars_common.jsonl
python stimuli_statistics_counting.py --fi counting_chars_rare.jsonl
python stimuli_statistics_counting.py --fi counting_words_common.jsonl
python stimuli_statistics_counting.py --fi counting_words_rare.jsonl

```


# Conversion task

## Example generation
- Done with `example_generation_scripts/celsius.py`. This generates two pairs:
    - `conversion_actual.txt` and `conversion_fake.txt` use the same inputs for the two task versions, but different outputs.
    - `conversion_actualinverse.txt` and `conversion_fakeinverse.txt` use the same outputs (after rounding) for the two task versions, but different inputs.

## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_conversion.py`. This generates stimuli for the above pairs, as well as a `primed` and `primedcontrol` versions of `actual`, both of which are the same as `actual` but with either a mention of Fahrenheit and Celsius in the prompt (`primed`) or a neutral extra sentence in the prompt (`primedcontrol`).

## Model testing
- Run these commands:
```
python run_openai.py --tasks conversion --conditions actual,actualinverse,actualprimed,actualprimedcontrol,fake,fakeinverse --max_tokens 100 --model gpt-4
python run_openai.py --tasks conversion --conditions actual,actualinverse,actualprimed,actualprimedcontrol,fake,fakeinverse --max_tokens 100 --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_conversion.py 
```




# Keyboard cipher task

## Example generation
- This task uses the same examples as the rot-13 task.

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_keyboard.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks keyboard --conditions highprob,medprob,lowprob,adversarial --max_tokens 200 --model gpt-4
python run_openai.py --tasks keyboard --conditions highprob,medprob,lowprob,adversarial --max_tokens 200 --model gpt-3.5-turbo
```

- Then, inside `evaluation/':
```
python eval_keyboard.py
``

# Multiplication task

## Example generation
- Done with `example_generation_scripts/multiplication.py`

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_multiplication.py` and `stimulus_example_generation/stimulus_generator_multiplication3.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks multiplication --conditions number,word,allcaps,alternatingcaps --max_tokens 100 --model gpt-4
python run_openai.py --tasks multiplication --conditions number,word,allcaps,alternatingcaps --max_tokens 100 --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_multiplication.py
```



# Spelling

1. Produce a list of single-token words that appear in the Pile. This file takes in a list of all
```
python spelling_candidates.py
```



















# Acronym task (5x5)

## Example generation
- First, produce candidate word lists. This was done as follows:
```
# Download wikitext-103
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip
unzip wikitext-103-v1.zip

# Find all words that are 2 tokens long in uppercase (whether or not there
# is a space before them), and similarly for lowercase; this produces one
# file for uppercase and one for lowercase, both sorted by frequency in Wikitext
cd example_generation_scripts
python acronym_tokens_double.py

# We then manually removed any words in the lists that included profanity
```

- Then, generate acronyms using `example_generation_scripts/acronym.py`. This controls for split points: that is, for a given line index, all 25 acronym files will have at that index an output word that has the same split point as all other files do, and each input word will have the same split point as the input words at the same position in all other files. The split point is the index where the first subword token ends.
- To check that the inputs and outputs match, and that the break points are correctly controlled for, we ran `python acronym_check.py` in `example_generation_scripts/`

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_acronym.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks acronym1 --conditions 11,12,13,14,15,21,22,23,24,25,31,32,33,34,35,41,42,43,44,45,51,52,53,54,55  --max_tokens 100 --model gpt-4 
python run_openai.py --tasks acronym1 --conditions 11,12,13,14,15,21,22,23,24,25,31,32,33,34,35,41,42,43,44,45,51,52,53,54,55  --max_tokens 100 --model gpt-3.5-turbo

python run_openai.py --tasks acronym2 --conditions 11  --max_tokens 100 --model gpt-4 
python run_openai.py --tasks acronym2 --conditions 11  --max_tokens 100 --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_acronym.py 
```

# Swapping task

## Example generation
- Base sentences were generated using `example_generation_scripts/swap_base.py`, the output of which was then manually filtered following the criteria used for the rot-13 sentences. The top 100 remaining sentences were then used. This gives 100 sentences that all contain at least one article. In addition, the article must be between two words that are only made of alphabetical characters (e.g., not after a comma - though they could be before a word that is followed by a comma), and they cannot be the first or second word of the sentence (to avoid capitalization issues when swapping).
- The swapped versions of sentences were then generated with `example_generation_scripts/swap_next_prev.py`

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_swap.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks swap --conditions base_prev,base_next,prev_base,next_base --model gpt-4
python run_openai.py --tasks swap --conditions base_prev,base_next,prev_base,next_base --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_swap.py
```







# Capitalize-third task

## Example generation
- Done with `example_generation_scripts/capitalize_third.py`

## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_capitalize_third.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks capitalize_third --conditions common,rare --model gpt-4
python run_openai.py --tasks capitalize_third --conditions common,rare --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_capitalize_third.py
```




 

# Miscellaneous notes

Running on GPU:
salloc --nodes=1 --ntasks=16 --mem=20G --time=02:00:00 --gres=gpu:1

Excluding if:
- Violence, death, or sex
- Proper names (except for very common ones, such as names of countries)
- Grammatical errors
- Not a complete sentence



