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
    # Possessive/Personal Relationship Indicators
    r"\b(my|our|his|her)\s+(mom|mother|dad|father|parents|family)\b",
    r"\b(my|our)\s+(mama|papa|mummy|daddy|mommy|mum|pa)\b",
    
    # Cultural and Informal Family Terms
    r"\b(mama|papa|pops|mummy|daddy|mommy|old\s+man|old\s+lady)\b",
    r"\b(ma|pa|mumma|dada|momma|poppa|granny|granddad)\b",
    
    # Extended/Non-Traditional Family
    r"\b(step(mom|mother|dad|father|parents)|step-parent)\b",
    r"\b(grand(ma|mother|pa|father|parents)|auntie|uncle|guardian|caregiver)\b",
    r"\b(foster\s+(mom|dad|parents)|adoptive\s+parents|single\s+(mom|dad|parent))\b",
    
    # Temporal/Experiential Context - Strong Indicators
    r"\b(when\s+i\s+was\s+(a\s+)?(kid|child|teenager|young)|as\s+a\s+(kid|child|teenager))\b",
    r"\b(growing\s+up|during\s+childhood|in\s+my\s+teens|back\s+then)\b",
    r"\b(i\s+remember\s+when|used\s+to\s+(tell|say)|would\s+always\s+(say|tell))\b",
    
    # Emotional/Relational Language
    r"\b(made\s+me\s+feel|i\s+felt\s+like|always\s+made\s+me)\b",
    r"\b(argued\s+with|fought\s+with|disagreed\s+with)\b",
    r"\b(proud\s+of\s+me|disappointed\s+in|supported\s+me)\b",
    r"\b(compared\s+me\s+to|expected\s+me\s+to|wanted\s+me\s+to)\b",
    
    # Positive Parenting Experiences
    r"\b(helped\s+me|taught\s+me|showed\s+me|guided\s+me)\b",
    r"\b(believed\s+in\s+me|was\s+there\s+for\s+me|understood\s+me)\b",
    r"\b(gave\s+me\s+advice|offered\s+guidance)\b",
    
    # Modern Parenting Contexts
    r"\b(phone\s+rules|screen\s+time|social\s+media\s+rules|internet\s+rules)\b",
    r"\b(allowance|driving\s+privileges|dating\s+rules|curfew)\b",
    r"\b(college\s+choice|career\s+decisions|life\s+goals)\b",
    
    # Cultural-Specific Terms
    r"\b((guyanese|caribbean|immigrant|traditional)\s+parents)\b",
    r"\b(back\s+home|our\s+culture|cultural\s+(expectations|practices))\b",
    
    # Relationship Quality Indicators
    r"\b((strict|lenient|overprotective|supportive|toxic|difficult)\s+(mom|dad|mother|father|parents))\b",
    r"\b(relationship\s+with\s+my|bond\s+with\s+my|connection\s+to\s+my)\b",
    
    # Life Stage References
    r"\b(still\s+live\s+with\s+(my\s+)?(parents|mom|dad)|moved\s+back\s+home)\b",
    r"\b(visit\s+home|going\s+home\s+to\s+(see\s+)?(my\s+)?(parents|mom|dad))\b",
    
    # Original Strong Patterns (Refined)
    r"\b(raise(d|s|ing)\s+(me|us)|how\s+i\s+was\s+raised)\b",
    r"\b(strict|discipline|punish(ment)?|rules?|curfew|grounded)\b",
    r"\b(ask(ing)?\s+(my\s+)?(parents|mom|dad)\s+for\s+permission)\b",
    r"\b(helicopter\s+(mom|dad|mother|father|parents)|narcissistic\s+(mom|dad|parents))\b",
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
                       default="articshift_filtered_comments_v2.csv",
                       help="Output CSV file for filtered comments")
    
    args = parser.parse_args()
    
    filter_parenting_comments(args.input_csv, args.output_csv)

if __name__ == "__main__":
    main()
