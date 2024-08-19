


# Embers of autoregression

# TODO: CHANGE MODELS
This repository gives the stimuli and LLM predictions for the paper Embers of Autoregression. The commands given in the rest of this README show how to run the tests for GPT-3.5 and GPT-4. To extend the results to Llama 3, change `run_openai.py` to `run_llama3.py` and use `--model llama-3-70b-chat`. To extend the results to Claude 3, change `run_openai.py` to `run_claude3.py` and use `--model claude-3`. To extend the results to Gemini 1.0, change `run_openai.py` to `run_gemini.py` and use `--model gemini-1.0-pro-001`.


# TODO: ADD REQUIREMENTS


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
- Done with `stimulus_generation_scripts/stimulus_generator_rot_encode.py`, `stimulus_generation_scripts/stimulus_generator_rot_decode.py`, `stimulus_generation_scripts/stimulus_generator_rot_prompts.py`, `stimulus_example_generator/stimulus_generator_shift.py`, and `stimulus_generator_shift_prompts.py`.

## Model testing
- Run these commands:
```
# Rot-13
python run_openai.py --tasks rot13enc,rot13dec,rot12enc,rot12dec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200  --model gpt-4-0613
python run_openai.py --tasks rot13enc,rot13dec,rot12enc,rot12dec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200  --model gpt-3.5-turbo-0613

# Other shifts
python run_openai.py --tasks shift --conditions 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25 --max_tokens 200  --model gpt-4-0613
python run_openai.py --tasks shift --conditions 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25 --max_tokens 200  --model gpt-3.5-turbo-0613


# Comparing prompting styles
python run_openai.py --tasks shiftcot,shiftstep --conditions 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25 --max_tokens 2000  --model gpt-4-0613

python run_openai.py --tasks rot13encstep,rot13decstep,rot13enccot,rot13deccot --conditions highprob,mediumprob,lowprob --max_tokens 2000  --model gpt-4-0613
python run_openai.py --tasks rot12encstep,rot12decstep,rot12enccot,rot12deccot --conditions highprob --max_tokens 2000  --model gpt-4-0613

```


- Then, inside `evaluation/`:
```
python eval_rot13.py
python eval_rot13_adversarial.py
python eval_shift.py 
python eval_rot13_prompts.py
python eval_shift_prompts.py 
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

python stimuli_statistics.py --fi rot12enc_highprob.jsonl
python stimuli_statistics.py --fi rot12dec_highprob.jsonl
```

To produce data for regressions in R:
```
python tsv_rot13.py 
python tsv_rot13and12.py 
```

The actual regressions were run in the notebook `Regressions.ipynb`.

## Estimating task frequency
Done with `corpus_analysis/c4_shift_finder.py`, which generates `c4_shifts.txt`, which we analyzed manually.



# Reversal task

## Example generation
- This task uses the same examples as the rot-13 task.

## Stimulus generation
- Done with `stimulus_generator_reverse_encode.py` and `stimulus_generator_reverse_decode.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks revenc,revdec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-4-0613
python run_openai.py --tasks revenc,revdec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-3.5-turbo-0613
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





# Swapping task

## Example generation
- This sentences were generated in a similar way as the sentences for rot-13, except with the added restriction that each sentence had to contain at least one article (a, an, or the). Further, they could not have an article as the first or last word (since that could create issues when attempting to swap the article the adjacent word - in such cases there would be no adjacent word for one of the possible swapping directions).
```
python swap_high_probability.py
python swap_low_probability.py
python swap_medium_probability.py
python swap_next_prev.py
```

## Stimulus generation
- Done with `stimulus_generator_swap.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks swap_base_next,swap_base_prev,swap_next_base,swap_prev_base --conditions highprob,mediumprob,lowprob --max_tokens 200 --model gpt-4-0613
python run_openai.py --tasks swap_base_next,swap_base_prev,swap_next_base,swap_prev_base --conditions highprob,mediumprob,lowprob --max_tokens 200 --model gpt-3.5-turbo-0613
```

- Then, inside `evaluation/`. Note that `next_base` is the case we focus on in the paper; the other three are just discussed in the appendix:
```
python eval_swap.py
```

## Statistics
To compute summary statistics about the stimulus sets:
```
python stimuli_statistics.py --fi swap_base_next_highprob.jsonl
python stimuli_statistics.py --fi swap_base_next_mediumprob.jsonl 
python stimuli_statistics.py --fi swap_base_next_lowprob.jsonl

python stimuli_statistics.py --fi swap_base_prev_highprob.jsonl
python stimuli_statistics.py --fi swap_base_prev_mediumprob.jsonl 
python stimuli_statistics.py --fi swap_base_prev_lowprob.jsonl

python stimuli_statistics.py --fi swap_next_base_highprob.jsonl
python stimuli_statistics.py --fi swap_next_base_mediumprob.jsonl 
python stimuli_statistics.py --fi swap_next_base_lowprob.jsonl

python stimuli_statistics.py --fi swap_prev_base_highprob.jsonl
python stimuli_statistics.py --fi swap_prev_base_mediumprob.jsonl
python stimuli_statistics.py --fi swap_prev_base_lowprob.jsonl
```


The regressions were run in the notebook `Regressions.ipynb`.




# Pig Latin and Boar Etruscan tasks

## Example generation
- High-probability sentences: Created by `example_generation_scripts/piglatin_high_probability.py`. The results were then manually filtered for the same criteria as the Rot-13 sentences, as well as the criteria specified below about initial consonant clusters; we then used the first 100 (i.e., 100 lowest perplexity) remaining examples.
- Medium-probability sentences: Created by `example_generation_scripts/piglatin_medium_probability.py`, using the same basic approach as the medium-probability sentences for rot-13.
- Adversarial sentences: Created in the same way as the rot-13 adversarial sentences.
- Low-probability sentences: Created by `example_generation_scripts/piglatin_low_probability.py`.
- Pig Latin is primarily a spoken game. Since English spelling often differs from pronuncation, this means that the Pig Latin treatment of many written words is ambiguous. E.g., should "union" become "unionay" or "unionyay"? Should "hour" become "houray" or "ourhay"? To check for such cases, we excluded words whose first written consonant cluster did not parallel their first spoken consonant cluster. In addition, for each word whose first vowel was [u], we checked the word's British pronunciation in the online Cambridge dictionary (https://dictionary.cambridge.org/) to see if it was pronounced with an unwritten /j/ (e.g., "new" is pronounced /nju/); if so, we excluded it. Checking for such words was done with the aid of the CMU pronouncing dictionary. To replicate this checking:
```
wget https://raw.githubusercontent.com/Alexir/CMUdict/master/cmudict-0.7b
mv cmudict-0.7b cmudict.txt
python piglatin_consonant_check.py
```

## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_piglatin_encode.py` and `stimulus_generation_scripts/stimulus_generator_piglatin_decode.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks pigenc_ay,pigdec_ay,pigenc_uv,pigdec_uv --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-4-0613
python run_openai.py --tasks pigenc_ay,pigdec_ay,pigenc_uv,pigdec_uv --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-3.5-turbo-0613

python run_openai.py --tasks pigenc_way,pigdec_way,pigenc_yay,pigdec_yay,pigenc_hay,pigdec_hay,pigenc_say,pigdec_say --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-4-0613
python run_openai.py --tasks pigenc_way,pigdec_way,pigenc_yay,pigdec_yay,pigenc_hay,pigdec_hay,pigenc_say,pigdec_say --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200 --model gpt-3.5-turbo-0613
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

## Task frequency analysis
Using `corpus_analysis/c4_commonness_checker.py`, we generated `c4_piglatin.txt`. We then analyzed this manually to determine the frequency of each Pig Latin variant.








# Acronym task

## Example generation
- First, produce candidate word lists. This was done as follows:
```
# Download wikitext-103
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip
unzip wikitext-103-v1.zip

# Download CMU Pronouncing Dictionary
wget https://raw.githubusercontent.com/Alexir/CMUdict/master/cmudict-0.7b
mv cmudict-0.7b cmudict.txt

# Find all words that appear in the CMU Pronouncing Dictionary that are 2 tokens long 
# in uppercase (whether or not there is a space before them), and similarly for 
# lowercase; this produces one file for uppercase and one for lowercase, 
# both sorted by the probability assigned to them by GPT-2.
cd example_generation_scripts
python probability_cmu.py

# We then manually removed any words in the lists that included profanity
```

- Then, generate acronyms using `example_generation_scripts/acronym.py`. This controls for split points: that is, for a given line index, all generated acronym files will have at that index an output word that has the same split point as all other files do, and each input word will have the same split point as the input words at the same position in all other files. The split point is the index where the first subword token ends.
- To check that the inputs and outputs match, and that the break points are correctly controlled for, we ran `python acronym_check.py` in `example_generation_scripts/
- A note about the filenames: "1" means highest probability, "5" means lowest. Each file has a 2-digit tag indicating first the output probability then the input probability. E.g., `acronym1_51` means very low-probability outputs and very high-probability inputs.

## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_acronym.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks acronym1 --conditions 11,12,13,14,15,21,31,41,51  --max_tokens 100 --model gpt-4-0613 
python run_openai.py --tasks acronym1 --conditions 11,12,13,14,15,21,31,41,51  --max_tokens 100 --model gpt-3.5-turbo-0613

python run_openai.py --tasks acronym2 --conditions 11  --max_tokens 100 --model gpt-4-0613 
python run_openai.py --tasks acronym2 --conditions 11  --max_tokens 100 --model gpt-3.5-turbo-0613
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

# Count how often each number appears in C4
cd corpus_analysis/
python c4_number_frequency.py

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
python run_openai.py --tasks counting_chars,counting_words --conditions common,rare,common_common,common_rare,rare_common,rare_rare --max_tokens 25 --model gpt-4-0613
python run_openai.py --tasks counting_chars,counting_words --conditions common,rare,common_common,common_rare,rare_common,rare_rare --max_tokens 25 --model gpt-3.5-turbo-0613
```

- Then, inside `evaluation/`:
```
python eval_counting.py
python eval_counting_frequency.py
```

## Stimuli statistics
```
python stimuli_statistics_counting.py --fi counting_chars_common.jsonl
python stimuli_statistics_counting.py --fi counting_chars_rare.jsonl 
python stimuli_statistics_counting.py --fi counting_chars_common_common.jsonl 
python stimuli_statistics_counting.py --fi counting_chars_common_rare.jsonl 
python stimuli_statistics_counting.py --fi counting_chars_rare_common.jsonl 
python stimuli_statistics_counting.py --fi counting_chars_rare_rare.jsonl 

python stimuli_statistics_counting.py --fi counting_words_common.jsonl 
python stimuli_statistics_counting.py --fi counting_words_rare.jsonl 
python stimuli_statistics_counting.py --fi counting_words_common_common.jsonl 
python stimuli_statistics_counting.py --fi counting_words_common_rare.jsonl 
python stimuli_statistics_counting.py --fi counting_words_rare_common.jsonl
python stimuli_statistics_counting.py --fi counting_words_rare_rare.jsonl 
```

The regressions were run inside `Regressions.ipynb`. Determining which numbers count as common for our binary common/rare comparison was done with `corpus_analysis/identify_common_numbers.py`.



# Multiplication task

## Example generation
- Done with `example_generation_scripts/multiplication.py`

## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_multiplication.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks multiplication --conditions number,word,allcaps,alternatingcaps --max_tokens 100 --model gpt-4-0613
python run_openai.py --tasks multiplication --conditions number,word,allcaps,alternatingcaps --max_tokens 100 --model gpt-3.5-turbo-0613
```

- Then, inside `evaluation/`:
```
python eval_multiplication.py
```

## Statistical tests
The regressions were run in `Regressions.ipynb`.



# Conversion task

## Names for conditions
This code repository uses names for the conditions that differ somewhat from how we discuss them in the paper. Here is a guide to the terms used in the codebase:
- The function (9/5)x+32 is referred to as `actual`, while (7/5)x+31 is referred to as `fake`.
- The default setting is to control the inputs across functions. When we instead control the outputs, it is referred to as `inverse`. In some files, this distinction is referred to as `fwd` (the default setting) vs.\ `rev` (the inverse setting).
- The case where the inputs are sampled uniformly from the integers 0 to 999 is referred to as `conversion`, while the case where the inputs are constrained to be greater than 500 and not divisible by 10 is referred to as `conversion_ood`.


## Example generation
- Done with `example_generation_scripts/celsius.py`. This generates two pairs:
    - `conversion_actual.txt` and `conversion_fake.txt` use the same inputs for the two task versions, but different outputs.
    - `conversion_actualinverse.txt` and `conversion_fakeinverse.txt` use the same outputs (after rounding) for the two task versions, but different inputs.
- And then we also ran `example_generation_scripts/celsius_ood.py`, which similarly generates two pairs but labeled `conversion_ood` instead of `conversion`.


## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_conversion.py` and `stimulus_generation_scripts/stimulus_generator_conversion_ood.py`. This generates stimuli for the above pairs, as well as a `primed` and `primedcontrol` versions of `actual`, both of which are the same as `actual` but with either a mention of Fahrenheit and Celsius in the prompt (`primed`) or a neutral extra sentence in the prompt (`primedcontrol`).

## Model testing
- Run these commands:
```
python run_openai.py --tasks conversion --conditions actual,actualinverse,actualprimed,actualprimedcontrol,fake,fakeinverse --max_tokens 100 --model gpt-4-0613
python run_openai.py --tasks conversion --conditions actual,actualinverse,actualprimed,actualprimedcontrol,fake,fakeinverse --max_tokens 100 --model gpt-3.5-turbo-0613

python run_openai.py --tasks conversion_ood --conditions actual,actualinverse,actualprimed,actualprimedcontrol,fake,fakeinverse --max_tokens 100 --model gpt-4-0613
python run_openai.py --tasks conversion_ood --conditions actual,actualinverse,actualprimed,actualprimedcontrol,fake,fakeinverse --max_tokens 100 --model gpt-3.5-turbo-0613
```

- Then, inside `evaluation/`:
```
python eval_conversion.py 
python eval_conversion_ood.py
```

## Statistics

Statistical tests were perfomed in `Regressions.ipynb`. For deciding what temperatures were OOD, we used `corpus_analysis/c4_fahrenheit_celsius.py` and `corpus_analysis/temp_analysis.py`.



# Keyboard cipher task

## Example generation
- This task uses the same examples as the rot-13 task.

## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_keyboard.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks keyboardcot,keyboardcotreference,keyboardcotdetailed --conditions highprob --max_tokens 4000 --model gpt-4-0613
python run_openai.py --tasks keyboardcot,keyboardcotreference,keyboardcotdetailed --conditions highprob --max_tokens 3000 --model gpt-3.5-turbo-0613
```

- Then, inside `evaluation/':
```
python eval_keyboard.py
``

# Sorting tasks

## Example generation
- For sorting words: The length of the list had to be from 10 to 20 inclusive. There could not be any repeats. The words were selected randomly (without replacement) from the set of common words used for the counting task.
- For sorintg numbers: The length of the list had to be from 10 to 20 inclusive. There could not be any repeats. The numbers were selected randomly (without replacement) from the set of integers from 1 to 10,000 inclusive.

```
python sort_words.py
python sort_numbers.py 
```

## Stimulus generation
- Done with `stimulus_generation_scripts/python stimulus_generator_sorting.py` and `stimulus_generation_scripts/stimulus_generator_sortingnumbers.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks sorting --conditions fwd,rev,ascending,descending --max_tokens 200 --model gpt-4-0613
python run_openai.py --tasks sorting --conditions fwd,rev,ascending,descending --max_tokens 200 --model gpt-3.5-turbo-0613
```

- Then, inside `evaluation/':
```
python eval_sorting.py
``

## Stimulus statistics

```
python stimuli_statistics.py --fi sorting_fwd.jsonl
python stimuli_statistics.py --fi sorting_rev.jsonl 
python stimuli_statistics.py --fi sorting_ascending.jsonl
python stimuli_statistics.py --fi sorting_descending.jsonl
```

Statistical tests are run in `Regressions.ipynb`.


# Birthdays

## Example generation
Only consider names that are made of the 26 Roman letters. Use this script to extract all birthdays from the WikiBio dataset:
```
python birthdays.py
```

Count the occurrences of the names in the first 100,000,000 lines of C4 (approximately 3.6 billion words):
```
python birthday_counter.py
```

Generate examples. This refers to a file `birthdays_verified.txt`, which we manually generated by checking each name on Wikipedia to make sure it is unambiguous and has the correct birthday listed. This produces four files in `examples/` (`birthdays_1.txt`, `birthdays_2.txt`, `birthdays_3.txt`, `birthdays_4.txt`), split by the frequency with which the names are mentioned in C4 (`birthdays_1.txt` has the most frequently-mentioned names, while `birthdays_4.txt` has the least frequently-mentioned names). The people's birthdays are matched across the four files; e.g., the first person in each file was born on March 2, 1985.
```
python birthday_generator.py
```


## Stimulus generation
- Done with `stimulus_generation_scripts/stimulus_generator_birthdays.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks birthdays --conditions 1,2,3,4 --max_tokens 100 --model gpt-4-0613
python run_openai.py --tasks birthdays --conditions 1,2,3,4 --max_tokens 100 --model gpt-3.5-turbo-0613
```

- Then, inside `evaluation/':
```
python eval_birthdays.py
```

## Stimulus statistics

```
python stimuli_statistics_birthdays.py --fi birthdays_1.jsonl 
python stimuli_statistics_birthdays.py --fi birthdays_2.jsonl 
python stimuli_statistics_birthdays.py --fi birthdays_3.jsonl
python stimuli_statistics_birthdays.py --fi birthdays_4.jsonl 
```

Statistical tests are run in `Regressions.ipynb`.



# Spelling

1. We started by producing a list of single-token words that appeared in the first 1 billion tokens of the Pile. They had to be a single token whether preceded by a space or not and were ranked by frequency in the Pile. This list is: `single_tokens_by_freq.txt`

2. We then generated examples to be spelled: `python spelling.py`

3. Then produce stimuli: `python stimulus_generator_spelling.py`

4. Then evaluate models:
```
python run_openai.py --tasks spelling --conditions all --max_tokens 100 --model gpt-4-0613
python run_openai.py --tasks spelling --conditions all --max_tokens 100 --model gpt-3.5-turbo-0613
```

5. Then evaluate models:
```
python eval_spelling.py
```










# Zero-shot cases

## Swapping
```
python stimulus_generator_zeroshot_swap.py 

python run_openai.py --tasks zeroshot_swap_next_base,zeroshot_swap_prev_base --conditions highprob,mediumprob,lowprob --max_tokens 200 --model gpt-4-0613
python run_openai.py --tasks zeroshot_swap_next_base,zeroshot_swap_prev_base --conditions highprob,mediumprob,lowprob --max_tokens 200 --model gpt-3.5-turbo-0613

```

## Rot-13
```
python stimulus_generator_zeroshot_rot_decode.py
python stimulus_generator_zeroshot_rot_encode.py

python run_openai.py --tasks zeroshot_rot13enc,zeroshot_rot13dec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200  --model gpt-4-0613
python run_openai.py --tasks zeroshot_rot13enc,zeroshot_rot13dec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200  --model gpt-3.5-turbo-0613
```

## Reversal
```
python stimulus_generator_zeroshot_reverse_decode.py
python stimulus_generator_zeroshot_reverse_encode.py

python run_openai.py --tasks zeroshot_revenc,zeroshot_revdec --conditions highprob,mediumprob,lowprob --max_tokens 200  --model gpt-4-0613
python run_openai.py --tasks zeroshot_revenc,zeroshot_revdec --conditions highprob,mediumprob,lowprob --max_tokens 200  --model gpt-3.5-turbo-0613
```

## Pig Latin
```
python stimulus_generator_zeroshot_piglatin_decode.py
python stimulus_generator_zeroshot_piglatin_encode.py

python run_openai.py --tasks zeroshot_pigenc_ay,zeroshot_pigdec_ay --conditions highprob,mediumprob,lowprob --max_tokens 200  --model gpt-4-0613
python run_openai.py --tasks zeroshot_pigenc_ay,zeroshot_pigdec_ay --conditions highprob,mediumprob,lowprob --max_tokens 200  --model gpt-3.5-turbo-0613
```







# Few-shot

## Example generation
counting_words_fewshot.py


python stimulus_generator_counting_fewshot.py
python stimulus_generator_finetune_count.py

python stimulus_generator_rot_encode_zeroshot.py
python stimulus_generator_rot_decode_zeroshot.py
python stimulus_generator_rot_encode_fewshot.py
python stimulus_generator_rot_decode_fewshot.py
python stimulus_generator_finetune_rot.py

python stimulus_generator_rot_encode_word_fewshot.py
python stimulus_generator_rot_decode_word_fewshot.py
python stimulus_generator_rot_encode_word_overlap_fewshot.py
python stimulus_generator_rot_decode_word_overlap_fewshot.py

python stimulus_generator_reverse_decode_zeroshot.py
python stimulus_generator_reverse_encode_zeroshot.py
python stimulus_generator_reverse_decode_fewshot.py
python stimulus_generator_reverse_encode_fewshot.py

python stimulus_generator_sorting_fewshot.py
python stimulus_generator_finetune_sort.py 


python run_openai.py --tasks counting_words_common --conditions 5shot,10shot --max_tokens 25 --model gpt-4-0613
python run_openai.py --tasks counting_words_common --conditions 5shot,10shot --max_tokens 25 --model gpt-3.5-turbo-0613
python run_claude3.py --tasks counting_words_common --conditions 5shot,10shot --max_tokens 25 --model claude-3

python run_openai.py --tasks rot13enc,rot13dec --conditions highprob_0shot,mediumprob_0shot,lowprob_0shot,highprob_5shot,mediumprob_5shot,lowprob_5shot,highprob_10shot,mediumprob_10shot,lowprob_10shot --max_tokens 200  --model gpt-3.5-turbo-0613
python run_openai.py --tasks rot13enc,rot13dec --conditions highprob_0shot,mediumprob_0shot,lowprob_0shot,highprob_5shot,mediumprob_5shot,lowprob_5shot,highprob_10shot,mediumprob_10shot,lowprob_10shot --max_tokens 200  --model gpt-4-0613
python run_claude3.py --tasks rot13enc,rot13dec --conditions highprob_0shot,mediumprob_0shot,lowprob_0shot,highprob_5shot,mediumprob_5shot,lowprob_5shot,highprob_10shot,mediumprob_10shot,lowprob_10shot --max_tokens 200  --model claude-3
 
python run_openai.py --tasks rot12enc,rot12dec --conditions highprob_0shot,highprob_5shot,highprob_10shot --max_tokens 200  --model gpt-3.5-turbo-0613
python run_openai.py --tasks rot12enc,rot12dec --conditions highprob_0shot,highprob_5shot,highprob_10shot --max_tokens 200  --model gpt-4-0613
python run_claude3.py --tasks rot12enc,rot12dec --conditions highprob_0shot,highprob_5shot,highprob_10shot --max_tokens 200  --model claude-3




python run_openai.py --tasks rot12dec,rot12enc,rot13dec,rot13enc --conditions highprob_word_overlap_0shot,highprob_word_overlap_5shot,highprob_word_overlap_10shot,highprob_word_0shot,highprob_word_5shot,highprob_word_10shot --max_tokens 200  --model gpt-4-0613
python run_openai.py --tasks rot13dec,rot13enc --conditions mediumprob_word_0shot,mediumprob_word_5shot,mediumprob_word_10shot,lowprob_word_0shot,lowprob_word_5shot,lowprob_word_10shot,mediumprob_word_overlap_0shot,mediumprob_word_overlap_5shot,mediumprob_word_overlap_10shot,lowprob_word_overlap_0shot,lowprob_word_overlap_5shot,lowprob_word_overlap_10shot --max_tokens 200  --model gpt-4-0613


python run_openai.py --tasks rot12dec,rot12enc,rot13dec,rot13enc --conditions highprob_word_overlap_0shot,highprob_word_overlap_5shot,highprob_word_overlap_10shot,highprob_word_0shot,highprob_word_5shot,highprob_word_10shot --max_tokens 200  --model gpt-3.5-turbo-0613
python run_openai.py --tasks rot13dec,rot13enc --conditions mediumprob_word_0shot,mediumprob_word_5shot,mediumprob_word_10shot,lowprob_word_0shot,lowprob_word_5shot,lowprob_word_10shot,mediumprob_word_overlap_0shot,mediumprob_word_overlap_5shot,mediumprob_word_overlap_10shot,lowprob_word_overlap_0shot,lowprob_word_overlap_5shot,lowprob_word_overlap_10shot --max_tokens 200  --model gpt-3.5-turbo-0613



python run_claude3.py --tasks rot12dec,rot12enc,rot13dec,rot13enc --conditions highprob_word_overlap_0shot,highprob_word_overlap_5shot,highprob_word_overlap_10shot,highprob_word_0shot,highprob_word_5shot,highprob_word_10shot --max_tokens 200  --model claude-3
python run_claude3.py --tasks rot13dec,rot13enc --conditions mediumprob_word_0shot,mediumprob_word_5shot,mediumprob_word_10shot,lowprob_word_0shot,lowprob_word_5shot,lowprob_word_10shot,mediumprob_word_overlap_0shot,mediumprob_word_overlap_5shot,mediumprob_word_overlap_10shot,lowprob_word_overlap_0shot,lowprob_word_overlap_5shot,lowprob_word_overlap_10shot --max_tokens 200  --model claude-3




python run_openai.py --tasks revenc,revdec --conditions highprob_0shot,mediumprob_0shot,lowprob_0shot,highprob_5shot,mediumprob_5shot,lowprob_5shot,highprob_10shot,mediumprob_10shot,lowprob_10shot --max_tokens 200 --model gpt-4-0613
python run_openai.py --tasks revenc,revdec --conditions highprob_0shot,mediumprob_0shot,lowprob_0shot,highprob_5shot,mediumprob_5shot,lowprob_5shot,highprob_10shot,mediumprob_10shot,lowprob_10shot --max_tokens 200 --model gpt-3.5-turbo-0613

python run_claude3.py --tasks revenc,revdec --conditions highprob_0shot,mediumprob_0shot,lowprob_0shot,highprob_5shot,mediumprob_5shot,lowprob_5shot,highprob_10shot,mediumprob_10shot,lowprob_10shot --max_tokens 200 --model claude-3




python run_openai.py --tasks sorting --conditions fwd_0shot,fwd_5shot,fwd_10shot,rev_0shot,rev_5shot,rev_10shot --max_tokens 200 --model gpt-4-0613
python run_openai.py --tasks sorting --conditions fwd_0shot,fwd_5shot,fwd_10shot,rev_0shot,rev_5shot,rev_10shot --max_tokens 200 --model gpt-3.5-turbo-0613
python run_claude3.py --tasks sorting --conditions fwd_0shot,fwd_5shot,fwd_10shot,rev_0shot,rev_5shot,rev_10shot --max_tokens 200 --model claude-3


# Fine-tuning
python openai_upload.py stimuli/counting_words_common_10shot_finetune.jsonl
python openai_finetune.py file-w2jjb6krUVevId2x45Rbbs2h count_10shot
python run_openai.py --tasks counting_words --conditions common --max_tokens 25 --model ft:gpt-3.5-turbo-0613:personal:count-10shot:9NYCyc4X

python openai_upload.py stimuli/counting_words_common_100shot_finetune.jsonl
python openai_finetune.py file-wY9wMoAYV5jE5HU9jUQg3HxI count_100shot
python run_openai.py --tasks counting_words --conditions common --max_tokens 25 --model ft:gpt-3.5-turbo-0613:personal:count-100shot:9NYN8hZQ





python openai_upload.py stimuli/rot12dec_highprob_100shot_finetune.jsonl
python openai_finetune.py file-eZx9zLdFZMKmPvqPpshe8aZ6 r12dh_100shot
python run_openai.py --tasks rot12dec --conditions highprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r12dh-100shot:9NgJvlfG

python openai_upload.py stimuli/rot12dec_highprob_10shot_finetune.jsonl
python openai_finetune.py file-mU8SxkmnOmMjCYBL8OUxQt2w r12dh_10shot
python run_openai.py --tasks rot12dec --conditions highprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r12dh-10shot:9NgHTiOF

python openai_upload.py stimuli/rot12enc_highprob_100shot_finetune.jsonl
python openai_finetune.py file-jJg4pgnlrhETgHbW85lM45nx r12eh_100shot
python run_openai.py --tasks rot12enc --conditions highprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r12eh-100shot:9NgL3Vjx

python openai_upload.py stimuli/rot12enc_highprob_10shot_finetune.jsonl
python openai_finetune.py file-9x7zPZsqKmm0ydBDVAtXkg24 r12eh_10shot
python run_openai.py --tasks rot12enc --conditions highprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r12eh-10shot:9NgPyaPc

python openai_upload.py stimuli/rot13dec_highprob_100shot_finetune.jsonl
python openai_finetune.py file-PwXqcTHDMloa6AXEVdcAPYWG r13dh_100shot
python run_openai.py --tasks rot13dec --conditions highprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13dh-100shot:9NgePY2P

python openai_upload.py stimuli/rot13dec_highprob_10shot_finetune.jsonl
python openai_finetune.py file-rNQeVHcjPdVxPyJrCBctl4jR r13dh_10shot
python run_openai.py --tasks rot13dec --conditions highprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13dh-10shot:9NgXMOZK

python openai_upload.py stimuli/rot13dec_lowprob_100shot_finetune.jsonl
python openai_finetune.py file-idgp1snOM5O5yBTPtHaz3m01 r13dl_100shot
python run_openai.py --tasks rot13dec --conditions lowprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13dl-100shot:9NgcPo3H

python openai_upload.py stimuli/rot13dec_lowprob_10shot_finetune.jsonl
python openai_finetune.py file-zSkivYHjRRGuY8rlh9ChLeBG r13dl_10shot
python run_openai.py --tasks rot13dec --conditions lowprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13dl-10shot:9NggubuL

python openai_upload.py stimuli/rot13dec_mediumprob_100shot_finetune.jsonl
python openai_finetune.py file-UcezAD8Ph81ahY87ZAHr2l9E r13dm_100shot
python run_openai.py --tasks rot13dec --conditions mediumprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13dm-100shot:9Ngwmxff

python openai_upload.py stimuli/rot13dec_mediumprob_10shot_finetune.jsonl
python openai_finetune.py file-djdrXriHdrpDavP5MQeCe7tu r13dm_10shot
python run_openai.py --tasks rot13dec --conditions mediumprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13dm-10shot:9Ngsb1im

python openai_upload.py stimuli/rot13enc_highprob_100shot_finetune.jsonl
python openai_finetune.py file-TF5f2NSxyU9B921OfeQYmAsy r13eh_100shot
python run_openai.py --tasks rot13enc --conditions highprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13eh-100shot:9Nh0obrD

python openai_upload.py stimuli/rot13enc_highprob_10shot_finetune.jsonl
python openai_finetune.py file-coLDGIeNK2HnwI2RuB4edNVN r13eh_10shot
python run_openai.py --tasks rot13enc --conditions highprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13eh-10shot:9Nh9hmyo

python openai_upload.py stimuli/rot13enc_mediumprob_100shot_finetune.jsonl
python openai_finetune.py file-gEkwjxQZ5dOAscMknIvUh63x r13em_100shot
python run_openai.py --tasks rot13enc --conditions mediumprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13em-100shot:9NhCSTcf

python openai_upload.py stimuli/rot13enc_mediumprob_10shot_finetune.jsonl
python openai_finetune.py file-8RPivgLC5sa3GSKJFs8xjxIa r13em_10shot
python run_openai.py --tasks rot13enc --conditions mediumprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13em-10shot:9Nh7Yqg6

python openai_upload.py stimuli/rot13enc_lowprob_10shot_finetune.jsonl
python openai_finetune.py file-yrA4yA6sFTBLXoi27uSy2T1o r13el_10shot
python run_openai.py --tasks rot13enc --conditions lowprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13el-10shot:9NhJlYd7

python openai_upload.py stimuli/rot13enc_lowprob_100shot_finetune.jsonl
python openai_finetune.py file-qDH42OJ9SZw4d7virzJP493F r13el_100shot
python run_openai.py --tasks rot13enc --conditions lowprob_0shot --max_tokens 200  --model ft:gpt-3.5-turbo-0613:personal:r13el-100shot:9NhO5zIm



python openai_upload.py stimuli/revdec_highprob_10shot_finetune.jsonl
python openai_finetune.py file-huaXcPLgDEXiqcCOMiyT0E8N rdh_10shot
python run_openai.py --tasks revdec --conditions highprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rdh-10shot:9S9QOf6v 

python openai_upload.py stimuli/revdec_highprob_100shot_finetune.jsonl
python openai_finetune.py file-OeTBNslxnTfj0BD7fY6bvEwa rdh_100shot
python run_openai.py --tasks revdec --conditions highprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rdh-100shot:9S9VZFB5

python openai_upload.py stimuli/revdec_mediumprob_10shot_finetune.jsonl 
python openai_finetune.py file-9KsKLgvIO3oMGgP09mEzzreb rdm_10shot
python run_openai.py --tasks revdec --conditions mediumprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rdm-10shot:9S9QgVm4


python openai_upload.py stimuli/revdec_mediumprob_100shot_finetune.jsonl
python openai_finetune.py file-tAGSd1OOrCYg5mqOn2stQvhd rdm_100shot
python run_openai.py --tasks revdec --conditions mediumprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rdm-100shot:9S9gUIsK

python openai_upload.py stimuli/revdec_lowprob_10shot_finetune.jsonl
python openai_finetune.py file-RNps1P0zekBEgQfFTKlfzFlq rdl_10shot
python run_openai.py --tasks revdec --conditions lowprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rdl-10shot:9S9dK7en

python openai_upload.py stimuli/revdec_lowprob_100shot_finetune.jsonl
python openai_finetune.py file-45fvrEEVMuGO1L95t9r5yeAQ rdl_100shot
python run_openai.py --tasks revdec --conditions lowprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rdl-100shot:9S9gPeoH




python openai_upload.py stimuli/revenc_highprob_10shot_finetune.jsonl
python openai_finetune.py file-S1Lj7WyT4qNe2qREKAZHBXqW reh_10shot
python run_openai.py --tasks revenc --conditions highprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:reh-10shot:9SALatx6 

python openai_upload.py stimuli/revenc_highprob_100shot_finetune.jsonl
python openai_finetune.py file-4DMuv8BzQal8u8dHlIhW22wf reh_100shot
python run_openai.py --tasks revenc --conditions highprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:reh-100shot:9SABR6eq

python openai_upload.py stimuli/revenc_mediumprob_10shot_finetune.jsonl
python openai_finetune.py file-uytB2PIG7U7gcVjP2yGvUkd1 rem_10shot
python run_openai.py --tasks revenc --conditions mediumprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rem-10shot:9SALjJuT


python openai_upload.py stimuli/revenc_mediumprob_100shot_finetune.jsonl
python openai_finetune.py file-dZIfC2uWty1cQlur61L1aLm7 rem_100shot
python run_openai.py --tasks revenc --conditions mediumprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rem-100shot:9SAEh76I

python openai_upload.py stimuli/revenc_lowprob_10shot_finetune.jsonl
python openai_finetune.py file-XbcKCRCdQrVK052TDA8vZ7Nn rel_10shot
python run_openai.py --tasks revenc --conditions lowprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rel-10shot:9SAMip7T

python openai_upload.py stimuli/revenc_lowprob_100shot_finetune.jsonl
python openai_finetune.py file-xZw6tpNu04CNdzeL0WGd87C2 rel_100shot
python run_openai.py --tasks revenc --conditions lowprob_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rel-100shot:9SACHgpi










python openai_upload.py stimuli/sorting_fwd_10shot_finetune.jsonl
python openai_finetune.py file-3rou5taox63cYdnLr2VWVadh fwd_10shot
python run_openai.py --tasks sorting --conditions fwd_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:fwd-10shot:9S9lmcHt

python openai_upload.py stimuli/sorting_fwd_100shot_finetune.jsonl
python openai_finetune.py file-5slb4bzbSL51MrMsxIDeSU0h fwd_100shot
python run_openai.py --tasks sorting --conditions fwd_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:fwd-100shot:9S9sz3um

python openai_upload.py stimuli/sorting_rev_10shot_finetune.jsonl
python openai_finetune.py file-3d0l6eFEJRIh1Gc4hIMcEdDZ rev_10shot
python run_openai.py --tasks sorting --conditions rev_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rev-10shot:9S9uQlp7

python openai_upload.py stimuli/sorting_rev_100shot_finetune.jsonl
python openai_finetune.py file-mfdJBlIPZ1wljHgT7U71nEMP rev_100shot
python run_openai.py --tasks sorting --conditions rev_0shot --max_tokens 200 --model ft:gpt-3.5-turbo-0613:personal:rev-100shot:9S9vpZRp



# Evaluation
python eval_counting_fewshot.py
python eval_rot13_fewshot.py
python tsv_rot13_fewshot.py
python tsv_rot13_fewshot_word.py
python tsv_rot13and12_fewshot.py
python tsv_rot13and12_fewshot_word.py
python eval_sorting_fewshot.py
python tsv_reverse_fewshot.py








