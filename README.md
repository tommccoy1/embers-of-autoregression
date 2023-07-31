

# Rot-13 and rot-2 tasks

## Example generation
- High-probability sentences: Created by `example_generation_scripts/sentences_high_probability.py`. Then used the top 100 after manually filtering to remove ones that:
    - Mentioned violence, death, or sex
    - Included proper names  (except for very common ones, such as names of countries)
    - Had grammatical errors
    - Were not complete sentences
- Medium-probability sentences: Created by `example_generation_scripts/sentences_medium_probability.py`. This generates 20 candidates; we manually selected the first (i.e., highest-perplexity) candidate that was grammatically correct (even if semantically odd). For a few sentences, we had to re-run the script to generate additional candidates because none of the 20 that were generated were grammatical; in some cases, we combined parts of two candidates in order to produce a grammatical sentence.
- Random sentences: Created by `example_generation_scripts/sentences_random.py`.
- Adversarial sentences: Copied the high-probability sentences into a new file, and then manually edited each line to replace a single word with another word that was grammatical but unlikely in that context. The new word was selected to be one that had a Levenshtein edit distance of either 1 or 2 from the word being replaced (where each edit could be a single-letter insertion, deletion, or substitution).

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_rot_encode.py` and `stimulus_example_generation/stimulus_generator_rot_decode.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks rot13enc,rot2enc,rot13dec,rot2dec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200  --model gpt-4
python run_openai.py --tasks rot13enc,rot2enc,rot13dec,rot2dec --conditions highprob,mediumprob,lowprob,adversarial --max_tokens 200  --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_rot13.py
python eval_rot13_adversarial.py 
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
```

- Then, inside `evaluation/`:
```
python eval_pig_boar.py
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
```



# Keyboard cipher task

## Example generation
- This task uses the same examples as the rot-13 task.

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_keyboard.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks keyboard --conditions highprob,lowprob,adversarial,random --model gpt-4
python run_openai.py --tasks keyboard --conditions highprob,lowprob,adversarial,random --model gpt-3.5-turbo
```

- Then, inside `evaluation/':
```
python eval_keyboard.py
```

# Acronym task

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

# Repetition task

## Example generation
- This task uses the same examples as the rot-13 task.

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_repeat.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks repeat --conditions highprob,lowprob,adversarial,random --model gpt-4
python run_openai.py --tasks repeat --conditions highprob,lowprob,adversarial,random --model gpt-3.5-turbo
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


# Multiplication task

## Example generation
- Done with `example_generation_scripts/multiplication.py` and `example_generation_scripts/multiplication3.py`

## Stimulus generation
- Done with `stimulus_example_generation/stimulus_generator_multiplication.py` and `stimulus_example_generation/stimulus_generator_multiplication3.py`

## Model testing
- Run these commands:
```
python run_openai.py --tasks multiplication,multiplication3 --conditions number,word,allcaps,alternatingcaps --max_tokens 100 --model gpt-4
python run_openai.py --tasks multiplication,multiplication3 --conditions number,word,allcaps,alternatingcaps --max_tokens 100 --model gpt-3.5-turbo
```

- Then, inside `evaluation/`:
```
python eval_multiplication.py
```


# Counting task

## Example generation

```
# Create a file listing the frequency and token count for words that appear at least 20 times in Wikitext
python counting_tokens.py

# Then create lists of candidate common and rare words: 400 for each token count (2, 3, or 4)
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



