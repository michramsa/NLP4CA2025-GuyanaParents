### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################
import argparse
from datetime import datetime
import json


PATTERNS = [
    r"\b(government|parliament|minister|prime|president|PPP|PPP/C|ministries|politics|APNU|PNC|election)\b",
    r"\b(economy|infrastructure|corruption|corrupt|budget|healthcare|education|economic|voting)\b",
    r"\b(policy|irfaan|ali|law|bill|gov't)\b"
]

def compile_patterns(patterns):
    """Compile regex patterns with case-insensitive flag"""
    return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]

def contains_content(text, compiled_patterns):
    if not text or pd.isna(text):
        return False
    
    return any(pattern.search(str(text)) for pattern in compiled_patterns)

def get_matching_patterns(text, compiled_patterns):
    """Get which patterns matched for this text"""
    if not text or pd.isna(text):
        return ""
    
    matches = []
    for i, pattern in enumerate(compiled_patterns):
        if pattern.search(str(text)):
            matches.append(f"Pattern_{i+1}")
    return "|".join(matches)

def bootstrap_filter(input_csv, output_dir, iteration=1, patterns=None):
    """
    Filter CSV for pattern-related comments.
    Saves both matched and non-matched comments for review.
    """
    
    # Use provided patterns or defaults
    if patterns is None:
        patterns = PATTERNS
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read the CSV file
    print(f"\n{'='*60}")
    print(f"ITERATION {iteration}")
    print(f"{'='*60}")
    print(f"Reading CSV file: {input_csv}")
    try:
        df = pd.read_csv(input_csv)
        print(f"Total comments loaded: {len(df)}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Compile patterns
    compiled_patterns = compile_patterns(patterns)
    
    # Filter for content
    print("Filtering for content...")
    mask = df['body'].apply(lambda x: contains_content(x, compiled_patterns))
    
    # Split into matched and non-matched
    matched_df = df[mask].copy()
    non_matched_df = df[~mask].copy()
    
    print(f"\nResults:")
    print(f"  Matched: {len(matched_df)} ({len(matched_df)/len(df)*100:.1f}%)")
    print(f"  Non-matched: {len(non_matched_df)} ({len(non_matched_df)/len(df)*100:.1f}%)")
    
    # Add matching pattern info to matched comments
    if len(matched_df) > 0:
        matched_df['matching_patterns'] = matched_df['body'].apply(
            lambda x: get_matching_patterns(x, compiled_patterns)
        )
    
    # Save matched results
    matched_file = output_dir / f"iter{iteration}_matched.csv"
    matched_df.to_csv(matched_file, index=False)
    print(f"\nMatched comments saved to: {matched_file}")
    
    # Save non-matched results
    non_matched_file = output_dir / f"iter{iteration}_non_matched.csv"
    non_matched_df.to_csv(non_matched_file, index=False)
    print(f"Non-matched comments saved to: {non_matched_file}")
    
    # Save patterns used for this iteration
    patterns_file = output_dir / f"iter{iteration}_patterns.json"
    pattern_data = {
        'iteration': iteration,
        'timestamp': datetime.now().isoformat(),
        'patterns': patterns,
        'num_matched': len(matched_df),
        'num_non_matched': len(non_matched_df),
        'match_rate': len(matched_df) / len(df)
    }
    with open(patterns_file, 'w') as f:
        json.dump(pattern_data, f, indent=2)
    print(f"Patterns saved to: {patterns_file}")
    
    # Print some sample matches for verification
    if len(matched_df) > 0:
        print("\nSample matching comments:")
        print("-" * 50)
        for idx, (_, row) in enumerate(matched_df.head(5).iterrows()):
            print(f"Sample {idx+1}:")
            print(f"Author: {row.get('author', 'N/A')}")
            print(f"Text: {str(row['body'])[:200]}...")
            print(f"Patterns: {row.get('matching_patterns', 'N/A')}")
            print("-" * 50)
    else:
        print("\nNo matching comments found. Consider:")
        print("1. Broadening the search patterns")
        print("2. Checking if the data contains the expected content")
        print("3. Manually reviewing a few comments to understand the language used")
    
    # Print next steps
    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    print(f"{'='*60}")
    print("1. Review matched comments in:", matched_file)
    print("   - Look for FALSE POSITIVES (shouldn't have matched)")
    print("2. Review non-matched comments in:", non_matched_file)
    print("   - Look for FALSE NEGATIVES (should have matched)")
    print("3. Update PATTERNS in this script based on your findings")
    print("4. Run next iteration:")
    print(f"   python {Path(__file__).name} --iteration {iteration+1}")
    print()


if __name__ == "__main__":

    # change as needed
    iteration_num = 1
    bootstrap_filter(cleaned_2026_Guyana_comments, "./bootstrap_output", iteration_num, None)