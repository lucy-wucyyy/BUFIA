#!/usr/bin/env python3
"""
Split data into train/dev sets for BUFIA experiments.
"""

import json
import random
from pathlib import Path

def split_train_dev(input_file, train_ratio=0.8, seed=42):
    """
    Split data into training and development sets.
    """
    print(f"Splitting data (train ratio: {train_ratio})...")
    
    # Load data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Shuffle with fixed seed for reproducibility
    random.seed(seed)
    random.shuffle(data)
    
    # Split
    split_idx = int(len(data) * train_ratio)
    train_data = data[:split_idx]
    dev_data = data[split_idx:]
    
    print(f"  Train: {len(train_data)} words")
    print(f"  Dev: {len(dev_data)} words")
    
    return train_data, dev_data

def write_wordlist(words_data, output_file):
    """
    Write wordlist in simple format (one word per line).
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in words_data:
            f.write(f"{word['ipa']}\n")

def write_segmented(words_data, output_file):
    """
    Write segmented format (space-separated phonemes).
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in words_data:
            segments = ' '.join(word['segments'])
            f.write(f"{segments}\n")

def create_bufia_formats(train_data, dev_data, output_dir):
    """
    Create multiple BUFIA input formats for experimentation.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Format 1: Simple IPA strings
    print("\nCreating BUFIA input files...")
    
    train_simple = output_dir / "train.txt"
    dev_simple = output_dir / "dev.txt"
    
    write_wordlist(train_data, train_simple)
    write_wordlist(dev_data, dev_simple)
    print(f"  ✓ Simple format: {train_simple}, {dev_simple}")
    
    # Format 2: Space-segmented
    train_seg = output_dir / "train_segmented.txt"
    dev_seg = output_dir / "dev_segmented.txt"
    
    write_segmented(train_data, train_seg)
    write_segmented(dev_data, dev_seg)
    print(f"  ✓ Segmented format: {train_seg}, {dev_seg}")
    
    # Create full dataset version (no split) for some experiments
    all_data = train_data + dev_data
    all_file = output_dir / "all_words.txt"
    write_wordlist(all_data, all_file)
    print(f"  ✓ Full dataset: {all_file}")

def create_readme(output_dir):
    """
    Create README explaining the data formats.
    """
    readme_content = """# Turkish Phonotactics Data

## Files

- `train.txt` / `dev.txt`: Training and development sets (IPA strings, one per line)
- `train_segmented.txt` / `dev_segmented.txt`: Space-segmented phonemes
- `all_words.txt`: Complete dataset without train/dev split

## Data Statistics

Run this script to see current statistics.

## For BUFIA

Depending on your BUFIA implementation, you may need:
1. Simple word list format (train.txt)
2. Segmented format (train_segmented.txt)
3. Feature matrix format (you may need to run BUFIA's own preprocessing)

## Next Steps

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
"""
    
    readme_path = Path(output_dir) / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"  ✓ Created README: {readme_path}")

def print_statistics(train_data, dev_data):
    """
    Print data statistics.
    """
    print("\n" + "="*60)
    print("DATA STATISTICS")
    print("="*60)
    
    def calc_stats(data, name):
        total_words = len(data)
        total_segments = sum(len(w['segments']) for w in data)
        avg_length = total_segments / total_words if total_words > 0 else 0
        
        print(f"\n{name}:")
        print(f"  Words: {total_words}")
        print(f"  Total segments: {total_segments}")
        print(f"  Avg word length: {avg_length:.2f} segments")
        
        # Segment distribution
        segment_counts = {}
        for word in data:
            for seg in word['segments']:
                segment_counts[seg] = segment_counts.get(seg, 0) + 1
        
        print(f"  Unique segments: {len(segment_counts)}")
        
    calc_stats(train_data, "Training Set")
    calc_stats(dev_data, "Development Set")

if __name__ == "__main__":
    print("Turkish Phonotactics - Data Preparation for BUFIA")
    print("=" * 60)
    
    # Input and output paths
    input_file = Path("../data/processed/turkish_features.json")
    output_dir = Path("../data/processed/bufia_input")
    
    # Load and split data
    train_data, dev_data = split_train_dev(input_file)
    
    # Create BUFIA input files
    create_bufia_formats(train_data, dev_data, output_dir)
    
    # Create README
    create_readme(output_dir)
    
    # Print statistics
    print_statistics(train_data, dev_data)
    
    print("\n" + "="*60)
    print("✓ Data preparation complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Install BUFIA: https://github.com/alenaks/BUFIA")
    print("2. Run BUFIA on train.txt with different parameters")
    print("3. Evaluate on dev.txt")
    print("4. Analyze learned constraints")