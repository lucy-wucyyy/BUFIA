#!/usr/bin/env python3
"""
Convert IPA transcriptions to phonological feature matrices.
This uses a simplified feature system based on Hayes and PanPhon.
"""

import csv
import json
from pathlib import Path
from collections import defaultdict

# Phonological feature system (simplified Hayes-style features)
# Features: syl, cons, son, cont, delrel, lat, nas, strid, voi, sg, cg, ant, cor, distr, lab, hi, lo, back, round, tense
IPA_FEATURES = {
    # Vowels
    'i': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '+', 'lo': '-', 'back': '-', 'round': '-', 'tense': '+'},
    'y': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '+', 'lo': '-', 'back': '-', 'round': '+', 'tense': '+'},
    'ɯ': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '+', 'lo': '-', 'back': '+', 'round': '-', 'tense': '+'},
    'u': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '+', 'lo': '-', 'back': '+', 'round': '+', 'tense': '+'},
    'e': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '-', 'lo': '-', 'back': '-', 'round': '-', 'tense': '+'},
    'ø': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '-', 'lo': '-', 'back': '-', 'round': '+', 'tense': '+'},
    'o': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '-', 'lo': '-', 'back': '+', 'round': '+', 'tense': '+'},
    'a': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '-', 'lo': '+', 'back': '+', 'round': '-', 'tense': '+'},
    'æ': {'syl': '+', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '-', 'lo': '+', 'back': '-', 'round': '-', 'tense': '+'},
    
    # Stops
    'p': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '-', 'ant': '+', 'cor': '-', 'lab': '+'},
    'b': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '+', 'ant': '+', 'cor': '-', 'lab': '+'},
    't': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '-', 'ant': '+', 'cor': '+', 'lab': '-'},
    'd': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '+', 'ant': '+', 'cor': '+', 'lab': '-'},
    'k': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '-', 'ant': '-', 'cor': '-', 'lab': '-', 'hi': '+', 'back': '+'},
    'ɡ': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '+', 'ant': '-', 'cor': '-', 'lab': '-', 'hi': '+', 'back': '+'},
    'g': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '+', 'ant': '-', 'cor': '-', 'lab': '-', 'hi': '+', 'back': '+'},
    'c': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '-', 'ant': '-', 'cor': '-', 'lab': '-', 'hi': '+', 'back': '-'},
    'ɟ': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '-', 'voi': '+', 'ant': '-', 'cor': '-', 'lab': '-', 'hi': '+', 'back': '-'},
    
    # Affricates
    't͡ʃ': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '+', 'voi': '-', 'ant': '-', 'cor': '+', 'strid': '+'},
    'd͡ʒ': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '+', 'voi': '+', 'ant': '-', 'cor': '+', 'strid': '+'},
    'ʤ': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '-', 'delrel': '+', 'voi': '+', 'ant': '-', 'cor': '+', 'strid': '+'},
    
    # Fricatives
    'f': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '+', 'delrel': '-', 'voi': '-', 'ant': '+', 'cor': '-', 'lab': '+', 'strid': '+'},
    'v': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '+', 'delrel': '-', 'voi': '+', 'ant': '+', 'cor': '-', 'lab': '+', 'strid': '+'},
    's': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '+', 'delrel': '-', 'voi': '-', 'ant': '+', 'cor': '+', 'strid': '+'},
    'z': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '+', 'delrel': '-', 'voi': '+', 'ant': '+', 'cor': '+', 'strid': '+'},
    'ʃ': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '+', 'delrel': '-', 'voi': '-', 'ant': '-', 'cor': '+', 'strid': '+'},
    'ʒ': {'syl': '-', 'cons': '+', 'son': '-', 'cont': '+', 'delrel': '-', 'voi': '+', 'ant': '-', 'cor': '+', 'strid': '+'},
    'h': {'syl': '-', 'cons': '-', 'son': '-', 'cont': '+', 'delrel': '-', 'voi': '-', 'sg': '+'},
    
    # Nasals
    'm': {'syl': '-', 'cons': '+', 'son': '+', 'cont': '-', 'nas': '+', 'voi': '+', 'ant': '+', 'cor': '-', 'lab': '+'},
    'n': {'syl': '-', 'cons': '+', 'son': '+', 'cont': '-', 'nas': '+', 'voi': '+', 'ant': '+', 'cor': '+', 'lab': '-'},
    
    # Liquids
    'l': {'syl': '-', 'cons': '+', 'son': '+', 'cont': '+', 'lat': '+', 'voi': '+', 'ant': '+', 'cor': '+'},
    'ɾ': {'syl': '-', 'cons': '+', 'son': '+', 'cont': '-', 'lat': '-', 'voi': '+', 'ant': '+', 'cor': '+'},
    'r': {'syl': '-', 'cons': '+', 'son': '+', 'cont': '+', 'lat': '-', 'voi': '+', 'ant': '+', 'cor': '+'},
    
    # Glides
    'j': {'syl': '-', 'cons': '-', 'son': '+', 'cont': '+', 'voi': '+', 'hi': '+', 'back': '-'},
    'ʎ': {'syl': '-', 'cons': '+', 'son': '+', 'cont': '+', 'lat': '+', 'voi': '+', 'ant': '-', 'cor': '+', 'hi': '+', 'back': '-'},
}

def parse_ipa_segment(segment):
    """
    Parse IPA segment and return feature vector.
    Handles multi-character segments like affricates.
    """
    # Try exact match first
    if segment in IPA_FEATURES:
        return IPA_FEATURES[segment]
    
    # Try without diacritics
    base = segment.replace('ː', '').replace('ʰ', '').replace('ʲ', '')
    if base in IPA_FEATURES:
        return IPA_FEATURES[base]
    
    print(f"Warning: Unknown IPA segment '{segment}'")
    return None

def ipa_to_features(ipa_string):
    """
    Convert IPA string to sequence of feature vectors.
    """
    segments = []
    i = 0
    
    while i < len(ipa_string):
        # Try to match affricates (2-3 char sequences)
        if i + 2 < len(ipa_string) and ipa_string[i:i+3] in IPA_FEATURES:
            segments.append(ipa_string[i:i+3])
            i += 3
        elif i + 1 < len(ipa_string) and ipa_string[i:i+2] in IPA_FEATURES:
            segments.append(ipa_string[i:i+2])
            i += 2
        else:
            segments.append(ipa_string[i])
            i += 1
    
    feature_vectors = []
    for seg in segments:
        features = parse_ipa_segment(seg)
        if features:
            feature_vectors.append((seg, features))
    
    return feature_vectors

def convert_data_to_features(input_file, output_file):
    """
    Convert TSV file with IPA to feature matrix format.
    """
    print(f"Converting {input_file} to feature format...")
    
    words_data = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            ipa = row['ipa']
            feature_seq = ipa_to_features(ipa)
            
            words_data.append({
                'orthography': row['orthography'],
                'ipa': ipa,
                'gloss': row.get('gloss', ''),
                'segments': [seg for seg, _ in feature_seq],
                'features': [feat for _, feat in feature_seq]
            })
    
    # Save as JSON for easy processing
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Converted {len(words_data)} words")
    print(f"  Output: {output_file}")
    
    return words_data

def create_bufia_input(words_data, output_file):
    """
    Create BUFIA-compatible input format.
    BUFIA typically expects tab-separated feature vectors.
    """
    print(f"Creating BUFIA input format...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in words_data:
            # Convert each word to feature string
            # Format: each segment as space-separated features
            ipa = word['ipa']
            segments = word['segments']
            
            # Simple format: just the IPA string (BUFIA will use its own features)
            f.write(f"{ipa}\n")
    
    print(f"✓ Created BUFIA input with {len(words_data)} words")
    print(f"  Output: {output_file}")

def analyze_phoneme_inventory(words_data):
    """
    Analyze and display the phoneme inventory found in the data.
    """
    print("\n" + "="*60)
    print("PHONEME INVENTORY ANALYSIS")
    print("="*60)
    
    all_segments = set()
    vowels = set()
    consonants = set()
    
    for word in words_data:
        for seg in word['segments']:
            all_segments.add(seg)
            
            features = parse_ipa_segment(seg)
            if features and features.get('syl') == '+':
                vowels.add(seg)
            elif features:
                consonants.add(seg)
    
    print(f"\nVowels ({len(vowels)}): {' '.join(sorted(vowels))}")
    print(f"Consonants ({len(consonants)}): {' '.join(sorted(consonants))}")
    print(f"Total segments: {len(all_segments)}")
    
    # Check for vowel harmony patterns
    print("\n" + "-"*60)
    print("VOWEL HARMONY FEATURES")
    print("-"*60)
    for v in sorted(vowels):
        features = parse_ipa_segment(v)
        if features:
            back = features.get('back', '?')
            round_val = features.get('round', '?')
            hi = features.get('hi', '?')
            print(f"  {v}: back={back}, round={round_val}, hi={hi}")

if __name__ == "__main__":
    print("Turkish Phonotactics - IPA to Features Conversion")
    print("=" * 60)
    
    # Set up paths
    input_file = Path("../data/raw/turkish_sample.tsv")
    feature_output = Path("../data/processed/turkish_features.json")
    bufia_output = Path("../data/processed/turkish_bufia_input.txt")
    
    # Create output directory
    feature_output.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert data
    words_data = convert_data_to_features(input_file, feature_output)
    
    # Create BUFIA input
    create_bufia_input(words_data, bufia_output)
    
    # Analyze inventory
    analyze_phoneme_inventory(words_data)
    
    print("\n✓ Feature conversion complete!")