#!/usr/bin/env python3
"""
Generate BUFIA-compatible feature table for Turkish phonemes.
BUFIA expects format: symbol feature1 feature2 feature3 ...
Where features are specified without +/- prefix (just feature name means +, -feature means -)
"""

from pathlib import Path

# Turkish phoneme inventory with features
# Using binary features suitable for TSL learning
TURKISH_PHONEMES = {
    # Vowels - features: syl, cons, son, cont, voi, hi, lo, back, round
    'i': ['syl', '-cons', 'son', 'cont', 'voi', 'hi', '-lo', '-back', '-round'],
    'y': ['syl', '-cons', 'son', 'cont', 'voi', 'hi', '-lo', '-back', 'round'],
    'ɯ': ['syl', '-cons', 'son', 'cont', 'voi', 'hi', '-lo', 'back', '-round'],
    'u': ['syl', '-cons', 'son', 'cont', 'voi', 'hi', '-lo', 'back', 'round'],
    'e': ['syl', '-cons', 'son', 'cont', 'voi', '-hi', '-lo', '-back', '-round'],
    'ø': ['syl', '-cons', 'son', 'cont', 'voi', '-hi', '-lo', '-back', 'round'],
    'o': ['syl', '-cons', 'son', 'cont', 'voi', '-hi', '-lo', 'back', 'round'],
    'a': ['syl', '-cons', 'son', 'cont', 'voi', '-hi', 'lo', 'back', '-round'],
    'æ': ['syl', '-cons', 'son', 'cont', 'voi', '-hi', 'lo', '-back', '-round'],
    
    # Stops - features: syl, cons, son, cont, delrel, voi, ant, cor, lab
    'p': ['-syl', 'cons', '-son', '-cont', '-delrel', '-voi', 'ant', '-cor', 'lab'],
    'b': ['-syl', 'cons', '-son', '-cont', '-delrel', 'voi', 'ant', '-cor', 'lab'],
    't': ['-syl', 'cons', '-son', '-cont', '-delrel', '-voi', 'ant', 'cor', '-lab'],
    'd': ['-syl', 'cons', '-son', '-cont', '-delrel', 'voi', 'ant', 'cor', '-lab'],
    'k': ['-syl', 'cons', '-son', '-cont', '-delrel', '-voi', '-ant', '-cor', '-lab', 'hi', 'back'],
    'g': ['-syl', 'cons', '-son', '-cont', '-delrel', 'voi', '-ant', '-cor', '-lab', 'hi', 'back'],
    'ɡ': ['-syl', 'cons', '-son', '-cont', '-delrel', 'voi', '-ant', '-cor', '-lab', 'hi', 'back'],
    'c': ['-syl', 'cons', '-son', '-cont', '-delrel', '-voi', '-ant', '-cor', '-lab', 'hi', '-back'],
    'ɟ': ['-syl', 'cons', '-son', '-cont', '-delrel', 'voi', '-ant', '-cor', '-lab', 'hi', '-back'],
    
    # Affricates - features: syl, cons, son, cont, delrel, voi, ant, cor, strid
    't͡ʃ': ['-syl', 'cons', '-son', '-cont', 'delrel', '-voi', '-ant', 'cor', 'strid'],
    'd͡ʒ': ['-syl', 'cons', '-son', '-cont', 'delrel', 'voi', '-ant', 'cor', 'strid'],
    'ʤ': ['-syl', 'cons', '-son', '-cont', 'delrel', 'voi', '-ant', 'cor', 'strid'],
    
    # Fricatives - features: syl, cons, son, cont, voi, ant, cor, lab, strid
    'f': ['-syl', 'cons', '-son', 'cont', '-voi', 'ant', '-cor', 'lab', 'strid'],
    'v': ['-syl', 'cons', '-son', 'cont', 'voi', 'ant', '-cor', 'lab', 'strid'],
    's': ['-syl', 'cons', '-son', 'cont', '-voi', 'ant', 'cor', 'strid'],
    'z': ['-syl', 'cons', '-son', 'cont', 'voi', 'ant', 'cor', 'strid'],
    'ʃ': ['-syl', 'cons', '-son', 'cont', '-voi', '-ant', 'cor', 'strid'],
    'ʒ': ['-syl', 'cons', '-son', 'cont', 'voi', '-ant', 'cor', 'strid'],
    'h': ['-syl', '-cons', '-son', 'cont', '-voi', 'sg'],
    
    # Nasals - features: syl, cons, son, nas, voi, ant, cor, lab
    'm': ['-syl', 'cons', 'son', 'nas', 'voi', 'ant', '-cor', 'lab'],
    'n': ['-syl', 'cons', 'son', 'nas', 'voi', 'ant', 'cor', '-lab'],
    
    # Liquids - features: syl, cons, son, cont, lat, voi, ant, cor
    'l': ['-syl', 'cons', 'son', 'cont', 'lat', 'voi', 'ant', 'cor'],
    'r': ['-syl', 'cons', 'son', 'cont', '-lat', 'voi', 'ant', 'cor'],
    'ɾ': ['-syl', 'cons', 'son', '-cont', '-lat', 'voi', 'ant', 'cor'],
    
    # Glides - features: syl, cons, son, cont, voi, hi, back
    'j': ['-syl', '-cons', 'son', 'cont', 'voi', 'hi', '-back'],
    'ʎ': ['-syl', 'cons', 'son', 'cont', 'lat', 'voi', '-ant', 'cor', 'hi', '-back'],
    
    # Word boundary
    '#': ['#'],
}

def create_feature_table(output_file):
    """
    Create BUFIA-compatible feature table file.
    """
    print("Creating BUFIA feature table for Turkish...")
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Header comment
        f.write("# BUFIA Feature Table for Turkish\n")
        f.write("# Format: symbol feature1 feature2 ...\n")
        f.write("# Features without prefix = +, features with - prefix = -\n\n")
        
        # Write each phoneme
        for symbol, features in sorted(TURKISH_PHONEMES.items()):
            # Skip word boundary for now (BUFIA adds it automatically)
            if symbol == '#':
                continue
            
            line = f"{symbol}\t{' '.join(features)}"
            f.write(line + '\n')
    
    print(f"✓ Created feature table: {output_path}")
    print(f"  Total symbols: {len(TURKISH_PHONEMES) - 1}")  # -1 for #
    
    # Print statistics
    vowels = [s for s, f in TURKISH_PHONEMES.items() if 'syl' in f and s != '#']
    consonants = [s for s, f in TURKISH_PHONEMES.items() if '-syl' in f]
    
    print(f"  Vowels: {len(vowels)}")
    print(f"  Consonants: {len(consonants)}")
    
    return output_path

def create_simplified_feature_table(output_file):
    """
    Create a simplified feature table focusing only on vowel harmony features.
    This is useful for experiments specifically targeting vowel harmony.
    """
    print("\nCreating simplified feature table (vowel harmony focus)...")
    
    # Simplified features: just the ones relevant for vowel harmony
    SIMPLIFIED = {
        # Vowels - just: syl, back, round, hi
        'i': ['syl', '-back', '-round', 'hi'],
        'y': ['syl', '-back', 'round', 'hi'],
        'ɯ': ['syl', 'back', '-round', 'hi'],
        'u': ['syl', 'back', 'round', 'hi'],
        'e': ['syl', '-back', '-round', '-hi'],
        'ø': ['syl', '-back', 'round', '-hi'],
        'o': ['syl', 'back', 'round', '-hi'],
        'a': ['syl', 'back', '-round', '-hi'],
        'æ': ['syl', '-back', '-round', '-hi'],
        
        # Consonants - just: -syl, voi
        'p': ['-syl', '-voi'],
        'b': ['-syl', 'voi'],
        't': ['-syl', '-voi'],
        'd': ['-syl', 'voi'],
        'k': ['-syl', '-voi'],
        'g': ['-syl', 'voi'],
        'ɡ': ['-syl', 'voi'],
        'c': ['-syl', '-voi'],
        'ɟ': ['-syl', 'voi'],
        't͡ʃ': ['-syl', '-voi'],
        'd͡ʒ': ['-syl', 'voi'],
        'ʤ': ['-syl', 'voi'],
        'f': ['-syl', '-voi'],
        'v': ['-syl', 'voi'],
        's': ['-syl', '-voi'],
        'z': ['-syl', 'voi'],
        'ʃ': ['-syl', '-voi'],
        'ʒ': ['-syl', 'voi'],
        'h': ['-syl', '-voi'],
        'm': ['-syl', 'voi'],
        'n': ['-syl', 'voi'],
        'l': ['-syl', 'voi'],
        'r': ['-syl', 'voi'],
        'ɾ': ['-syl', 'voi'],
        'j': ['-syl', 'voi'],
        'ʎ': ['-syl', 'voi'],
    }
    
    output_path = Path(output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Simplified Turkish Feature Table (Vowel Harmony Focus)\n")
        f.write("# Vowels: syl, back, round, hi\n")
        f.write("# Consonants: -syl, voi\n\n")
        
        for symbol, features in sorted(SIMPLIFIED.items()):
            line = f"{symbol}\t{' '.join(features)}"
            f.write(line + '\n')
    
    print(f"✓ Created simplified feature table: {output_path}")
    
    return output_path

def print_usage_examples():
    """
    Print example BUFIA commands.
    """
    print("\n" + "="*70)
    print("USAGE EXAMPLES")
    print("="*70)
    
    examples = [
        {
            'name': 'Experiment 1: Full features, local bigrams',
            'cmd': './bufia -w train.txt -f turkish_features.txt -n 2 -k 2 -l local -a 1'
        },
        {
            'name': 'Experiment 2: Simplified features (vowel harmony)',
            'cmd': './bufia -w train.txt -f turkish_features_simple.txt -n 2 -k 2 -l local -a 1'
        },
        {
            'name': 'Experiment 3: Piecewise (long-distance)',
            'cmd': './bufia -w train.txt -f turkish_features.txt -n 2 -k 2 -l piecewise -a 1'
        },
        {
            'name': 'Experiment 4: No word boundaries',
            'cmd': './bufia -w train.txt -f turkish_features.txt -n 2 -k 2 -l local -a 1 -b False'
        },
    ]
    
    for i, ex in enumerate(examples, 1):
        print(f"\n{ex['name']}:")
        print(f"  {ex['cmd']}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    print("Turkish Phonotactics - BUFIA Feature Table Generator")
    print("="*70)
    
    # Create output directory
    output_dir = Path("../data/processed/bufia_input")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create full feature table
    full_table = create_feature_table(output_dir / "turkish_features.txt")
    
    # Create simplified feature table
    simple_table = create_simplified_feature_table(output_dir / "turkish_features_simple.txt")
    
    # Print usage examples
    print_usage_examples()
    
    print("\n✓ Feature tables created successfully!")
    print("\nNext step: Install and run BUFIA")
    print("  See: ../docs/BUFIA_INSTALLATION.md")