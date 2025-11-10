### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################
import pandas as pd
import re
import argparse
from datetime import datetime

# Simplified patterns for parenting-related content
PARENTING_PATTERNS = [
    r"\b(parent|parents|mom|mother|dad|father)\b",
    r"\b(family|childhood|growing\s+up)\b", 
    r"\b(raised|discipline|strict)\b",
    r"\b(my\s+(mom|mother|dad|father|parents))\b",
    r"\b(our\s+(family|parents))\b",
    r"\b(when\s+i\s+was\s+(young|a\s+kid|little))\b",
]

def compile_patterns(patterns):
    """Compile regex patterns with case-insensitive flag"""
    return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]

def contains_parenting_content(text):
    """Check if text contains parenting-related content"""
    if not text or pd.isna(text):
        return False
    
    compiled_patterns = compile_patterns(PARENTING_PATTERNS)
    return any(pattern.search(str(text)) for pattern in compiled_patterns)

def filter_parenting_comments(input_csv, output_csv):
    """Filter CSV for parenting-related comments"""
    
    # Read the CSV file
    print(f"Reading CSV file: {input_csv}")
    try:
        df = pd.read_csv(input_csv)
        print(f"Total comments loaded: {len(df)}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Filter for parenting-related content
    print("Filtering for parenting-related content...")
    parenting_mask = df['body'].apply(contains_parenting_content)
    filtered_df = df[parenting_mask].copy()
    
    print(f"Comments matching parenting patterns: {len(filtered_df)}")
    
    # Add a column indicating which patterns matched (for debugging)
    def get_matching_patterns(text):
        if not text or pd.isna(text):
            return ""
        
        compiled_patterns = compile_patterns(PARENTING_PATTERNS)
        matches = []
        for i, pattern in enumerate(compiled_patterns):
            if pattern.search(str(text)):
                matches.append(f"Pattern_{i+1}")
        return "|".join(matches)
    
    if len(filtered_df) > 0:
        filtered_df['matching_patterns'] = filtered_df['body'].apply(get_matching_patterns)
    
    # Save filtered results
    filtered_df.to_csv(output_csv, index=False)
    print(f"Filtered comments saved to: {output_csv}")
    
    # Print some sample matches for verification
    if len(filtered_df) > 0:
        print("\nSample matching comments:")
        print("-" * 50)
        for idx, (_, row) in enumerate(filtered_df.head(5).iterrows()):
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

def main():
    parser = argparse.ArgumentParser(description="Filter CSV for parenting-related Reddit comments")
    parser.add_argument("--input_csv", 
                       default="/home/m210/NLP4CA/data/articshift_comments_RAW.csv",
                       help="Input CSV file with Reddit comments")
    parser.add_argument("--output_csv", 
                       default="articshift_filtered_comments.csv",
                       help="Output CSV file for filtered comments")
    
    args = parser.parse_args()
    
    filter_parenting_comments(args.input_csv, args.output_csv)

if __name__ == "__main__":
    main()
