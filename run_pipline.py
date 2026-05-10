#!/usr/bin/env python3
"""
Master script to run the complete data preparation pipeline.
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_path, description):
    """
    Run a Python script and handle errors.
    """
    print("\n" + "="*70)
    print(f"Running: {description}")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=script_path.parent,
            check=True,
            capture_output=False
        )
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running {description}")
        print(f"  Error: {e}")
        return False

def main():
    """
    Run the complete pipeline.
    """
    print("="*70)
    print("TURKISH PHONOTACTICS PROJECT - FULL PIPELINE")
    print("="*70)
    
    scripts_dir = Path(__file__).parent
    
    # Define pipeline steps
    steps = [
        (scripts_dir / "download_data.py", "Step 1: Data Collection"),
        (scripts_dir / "ipa_to_features.py", "Step 2: IPA to Features Conversion"),
        (scripts_dir / "prepare_bufia_input.py", "Step 3: BUFIA Input Preparation"),
    ]
    
    # Run each step
    success_count = 0
    for script, description in steps:
        if run_script(script, description):
            success_count += 1
        else:
            print(f"\n⚠ Pipeline stopped at: {description}")
            break
    
    # Final summary
    print("\n" + "="*70)
    print("PIPELINE SUMMARY")
    print("="*70)
    print(f"Completed: {success_count}/{len(steps)} steps")
    
    if success_count == len(steps):
        print("\n✓ All steps completed successfully!")
        print("\nYour data is ready for BUFIA:")
        print("  → ../data/processed/bufia_input/train.txt")
        print("  → ../data/processed/bufia_input/dev.txt")
        print("\nNext: Install BUFIA and run experiments")
    else:
        print("\n⚠ Pipeline incomplete - please check errors above")

if __name__ == "__main__":
    main()