#!/usr/bin/env python3
"""
Download Turkish wordlist data from ASJP database or Lexibank.
For this project, we'll use publicly available Turkish data sources.
"""

import requests
import csv
from pathlib import Path

def download_asjp_turkish():
    """
    Download Turkish data from ASJP database.
    ASJP uses a simplified phonetic transcription that we'll need to convert.
    """
    print("Downloading ASJP Turkish data...")
    
    # ASJP dataset URL (this is a common public source)
    # Note: You may need to check the current URL or download manually
    url = "https://asjp.clld.org/static/ListsWithASJPcode.txt"
    
    output_path = Path("../data/raw/asjp_turkish.txt")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse and extract Turkish entries
        turkish_words = []
        for line in response.text.split('\n'):
            if line.strip() and 'Turkish' in line:
                turkish_words.append(line)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(turkish_words))
        
        print(f"✓ Downloaded {len(turkish_words)} Turkish entries to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"✗ Error downloading ASJP data: {e}")
        print("  You may need to download manually from https://asjp.clld.org/")
        return None

def create_sample_turkish_data():
    """
    Create a sample Turkish dataset for testing the pipeline.
    These are real Turkish words in IPA transcription.
    """
    print("Creating sample Turkish dataset...")
    
    # Sample Turkish words with IPA transcription
    # These demonstrate key phonotactic patterns:
    # - Vowel harmony (back/front, round)
    # - Consonant clusters
    # - Word structure
    sample_words = [
        "ev\tev\thouse",
        "kız\tkɯz\tgirl",
        "göz\tɟøz\teye",
        "güzel\tɡyzæl\tbeautiful",
        "kitap\tkitap\tbook",
        "okul\tokul\tschool",
        "adam\tadam\tman",
        "kadın\tkadɯn\twoman",
        "çocuk\tt͡ʃod͡ʒuk\tchild",
        "masa\tmasa\ttable",
        "sandalye\tsandaʎe\tchair",
        "pencere\tpend͡ʒeɾe\twindow",
        "kapı\tkapɯ\tdoor",
        "köprü\tkøpɾy\tbridge",
        "dünya\tdynja\tworld",
        "hayat\thaját\tlife",
        "insan\tinsan\thuman",
        "şehir\tʃehiɾ\tcity",
        "yol\tjol\troad",
        "su\tsu\twater",
        "ağaç\taːt͡ʃ\ttree",
        "dağ\tdaː\tmountain",
        "deniz\tdeniz\tsea",
        "gökyüzü\tɟøcyzy\tsky",
        "yıldız\tjɯldɯz\tstar",
        "ay\taj\tmoon",
        "güneş\tɡyneʃ\tsun",
        "sabah\tsabah\tmorning",
        "akşam\takʃam\tevening",
        "gece\tɟed͡ʒe\tnight",
        "gün\tɡyn\tday",
        "yıl\tjɯl\tyear",
        "zaman\tzaman\ttime",
        "sonra\tsonɾa\tafter",
        "önce\tønʤe\tbefore",
        "büyük\tbyjyk\tbig",
        "küçük\tkyt͡ʃyk\tsmall",
        "uzun\tuzun\tlong",
        "kısa\tkɯsa\tshort",
        "yeni\tjeni\tnew",
        "eski\teski\told",
        "iyi\tiji\tgood",
        "kötü\tkøty\tbad",
        "sıcak\tsɯd͡ʒak\thot",
        "soğuk\tsouk\tcold",
        "beyaz\tbejaz\twhite",
        "siyah\tsijah\tblack",
        "kırmızı\tkɯɾmɯzɯ\tred",
        "mavi\tmavi\tblue",
        "yeşil\tjeʃil\tgreen",
        "sarı\tsaɾɯ\tyellow",
    ]
    
    output_path = Path("../data/raw/turkish_sample.tsv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("orthography\tipa\tgloss\n")
        f.write('\n'.join(sample_words))
    
    print(f"✓ Created sample dataset with {len(sample_words)} words at {output_path}")
    return output_path

def download_lexibank_info():
    """
    Provide information about accessing Lexibank Turkish data.
    """
    print("\n" + "="*60)
    print("LEXIBANK DATA ACCESS")
    print("="*60)
    print("""
For more comprehensive data, you can access Turkish wordlists from:

1. Lexibank: https://github.com/lexibank
   - Look for datasets with Turkish coverage
   - CLDF format makes it easy to extract phonemic forms

2. Turkish National Corpus: https://www.tnc.org.tr/
   - More extensive coverage
   - May need additional preprocessing

3. Manual download steps:
   - Clone lexibank repo: git clone https://github.com/lexibank/[dataset]
   - Extract Turkish entries from CLDF files
   - Convert to IPA using provided transcription systems
    """)

if __name__ == "__main__":
    print("Turkish Phonotactics Project - Data Collection")
    print("=" * 60)
    
    # Create sample data for immediate use
    sample_path = create_sample_turkish_data()
    
    # Attempt to download ASJP (may require manual download)
    # asjp_path = download_asjp_turkish()
    
    # Show Lexibank information
    download_lexibank_info()
    
    print("\n✓ Data collection setup complete!")
    print(f"  Sample data ready at: {sample_path}")