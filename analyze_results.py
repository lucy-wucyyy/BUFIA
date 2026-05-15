#!/usr/bin/env python3
"""
Analyze BUFIA output and compare with known Turkish phonotactics.
"""

import re
from pathlib import Path
from collections import defaultdict

# Known Turkish phonotactic constraints from the literature
TURKISH_CONSTRAINTS = {
    'vowel_harmony': {
        'backness': "Vowels in a word should agree in [back] feature",
        'rounding': "High vowels agree in rounding with preceding vowel",
        'examples': ['*ev.ler (e-front, i-front ✓)', '*kız.lar (ɯ-back, a-back ✓)']
    },
    'consonant_clusters': {
        'initial': "Limited initial clusters: stops + liquids/glides mainly",
        'final': "Final consonants restricted; certain clusters disallowed",
        'examples': ['*tk, *pb, *gd forbidden initially']
    },
    'word_structure': {
        'syllable': "(C)V(C) syllable structure",
        'stress': "Usually final syllable stress",
    }
}

def parse_bufia_constraint(constraint_line):
    """
    Parse a BUFIA constraint line.
    Format varies by implementation, but typically:
    *[feature1=value1][feature2=value2]...
    """
    # This is a template - adjust based on actual BUFIA output format
    if constraint_line.startswith('*'):
        return {
            'raw': constraint_line,
            'type': 'forbidden',
            'parsed': constraint_line[1:]  # Remove *
        }
    return None

def categorize_constraint(constraint):
    """
    Categorize constraint as vowel-related, consonant-related, etc.
    """
    raw = constraint['raw'].lower()
    
    if any(f in raw for f in ['syl', 'back', 'round', 'hi', 'lo']):
        if 'syl' in raw or any(v in raw for v in ['back', 'round', 'hi']):
            return 'vowel'
    
    if any(f in raw for f in ['cons', 'voice', 'cont', 'strid']):
        return 'consonant'
    
    return 'mixed'

def analyze_bufia_output(bufia_output_file):
    """
    Read and analyze BUFIA output file.
    """
    print(f"Analyzing BUFIA output: {bufia_output_file}")
    print("="*60)
    
    if not Path(bufia_output_file).exists():
        print(f"✗ File not found: {bufia_output_file}")
        print("\nTo generate BUFIA output, run:")
        print("  bufia --input train.txt --output results.txt --tier-size 2 --ngram 2")
        return
    
    constraints = []
    
    with open(bufia_output_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('*'):
                constraint = parse_bufia_constraint(line)
                if constraint:
                    constraints.append(constraint)
    
    print(f"Total constraints learned: {len(constraints)}\n")
    
    # Categorize
    categories = defaultdict(list)
    for c in constraints:
        cat = categorize_constraint(c)
        categories[cat].append(c)
    
    for cat, items in categories.items():
        print(f"{cat.upper()} constraints: {len(items)}")
        for item in items[:5]:  # Show first 5
            print(f"  {item['raw']}")
        if len(items) > 5:
            print(f"  ... and {len(items)-5} more")
        print()

def compare_with_reference():
    """
    Show what to look for in BUFIA output based on Turkish phonology.
    """
    print("\n" + "="*60)
    print("EXPECTED PATTERNS IN TURKISH")
    print("="*60)
    
    print("\n1. VOWEL HARMONY")
    print("-"*60)
    print("Back/Front Harmony:")
    print("  Should see: *[+syl,+back][+syl,-back] or similar")
    print("  Meaning: Back vowels and front vowels don't mix in a word")
    print("  Examples: 'kitap' (all front), 'okul' (all back)")
    
    print("\nRounding Harmony:")
    print("  Should see: Constraints on [round] feature sequences")
    print("  Examples: 'güzel' (front + round), 'dünya' (front + round)")
    
    print("\n2. CONSONANT RESTRICTIONS")
    print("-"*60)
    print("Initial Clusters:")
    print("  Should see: *#[stop][stop] or similar")
    print("  Meaning: No double stops word-initially")
    
    print("Final Restrictions:")
    print("  Should see: Constraints on [-syl] at word end")
    
    print("\n3. EVALUATION QUESTIONS")
    print("-"*60)
    print("✓ Does BUFIA capture back/front harmony?")
    print("✓ Does BUFIA capture rounding harmony?")
    print("✓ Are initial cluster restrictions learned?")
    print("✓ Are there false positives (constraints not in Turkish)?")
    print("✓ What known patterns are missed?")

def create_analysis_template():
    """
    Create a template for recording experimental results.
    """
    template = """# BUFIA Experiment Results

## Experiment Parameters
- Tier size (k): ___
- N-gram size (n): ___
- Feature set: ___
- Training data: ___ words
- Dev data: ___ words

## Constraints Learned
Total: ___

### Vowel Harmony Constraints
- [ ] Back/front harmony: ___ constraints
  - Example: 
  - Interpretation:

- [ ] Rounding harmony: ___ constraints
  - Example:
  - Interpretation:

### Consonant Constraints
- [ ] Initial clusters: ___ constraints
  - Example:
  - Interpretation:

- [ ] Final position: ___ constraints
  - Example:
  - Interpretation:

### Other Constraints
- List any unexpected or interesting constraints:

## Evaluation

### Coverage (what was captured correctly)
- ✓ Back/front vowel harmony: YES / PARTIAL / NO
- ✓ Rounding harmony: YES / PARTIAL / NO
- ✓ Initial clusters: YES / PARTIAL / NO
- Comments:

### Precision (false positives)
- Overgenerated constraints (not real Turkish patterns):
  1.
  2.

### Comparison with Reference Grammar
- Match with Kornfilt (1997): ___
- Match with Clements & Sezer (1982): ___

## Discussion Notes
- What worked well:
- What didn't work:
- Surprising findings:
- Parameter sensitivity:

## Next Experiments
- Try different k value?
- Try different n value?
- Need more data?
- Feature set modification?
"""
    
    output_path = Path("../results/experiment_template.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"\n✓ Created analysis template: {output_path}")

if __name__ == "__main__":
    print("BUFIA Output Analysis Tool")
    print("="*60)
    
    # Show expected patterns
    compare_with_reference()
    
    # Try to analyze output if it exists
    output_files = [
        "../results/bufia_output.txt",
        "../results/experiment_k2_n2.txt",
        "../results/results_k1_n2.txt",
    ]
    
    found = False
    for output_file in output_files:
        if Path(output_file).exists():
            print(f"\n{'='*60}")
            analyze_bufia_output(output_file)
            found = True
            break
    
    if not found:
        print("\n" + "="*60)
        print("NO BUFIA OUTPUT FILES FOUND YET")
        print("="*60)
        print("\nRun BUFIA first, then use this script to analyze results.")
        print("\nExample BUFIA command:")
        print("  cd ../bufia")
        print("  bufia --input ../data/processed/bufia_input/train.txt \\")
        print("        --output ../results/experiment_k2_n2.txt \\")
        print("        --tier-size 2 --ngram 2")
    
    # Create analysis template
    create_analysis_template()
    
    print("\n" + "="*60)
    print("Analysis complete!")