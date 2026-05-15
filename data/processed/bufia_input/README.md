# Turkish Phonotactics Data

## Files

- `train.txt` / `dev.txt`: Training and development sets (IPA strings, one per line)
- `train_segmented.txt` / `dev_segmented.txt`: Space-segmented phonemes
- `all_words.txt`: Complete dataset without train/dev split

## Data Statistics

Run this script to see current statistics.

## For BUFIA

1. Simple word list format (train.txt)
2. Segmented format (train_segmented.txt)
3. Feature matrix format (turkish_features.txt)

## Experiment Set Up

1. Install BUFIA (Haskell implementation)
2. Run BUFIA with different parameter settings:
   - Vary tier sizes (k=1, 2, 3...)
   - Vary feature sets
   - Vary n-gram lengths
3. Analyze learned constraints
4. Compare with Turkish phonological descriptions

## Key Patterns to Look For

### Vowel Harmony
- Back/front harmony: [+back] vowels together, [-back] vowels together
- Rounding harmony: [+round] vowels pattern together in certain contexts

### Consonant Restrictions
- Word-initial clusters: limited options
- Syllable-final restrictions
- Voicing patterns

### Example Constraints to Expect
- *[+back][-back]: Back and front vowels don't mix in same word
- Word-initial cluster restrictions
- No *tk, *pn, etc. sequences
