
### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

# data has text which are empty or otherwise unneeded, fix whitespace
def remove_deleted_fix_whitespace(csv):
    df = pd.read_csv(csv)

    # remove NaNs + "[deleted]" + "[removed]"
    df_cleaned = df[(df['body'].notna()) & (df['body'] != '[deleted]') & (df['body'] != '[removed]') ]
    # check for completely empty rows
    df_cleaned = df_cleaned[df_cleaned['body'].str.strip() != '']

    df_cleaned['body'] = df_cleaned['body'].str.replace(r'\s+', ' ', regex=True).str.strip()
    print(df_cleaned.head())

    ### if you want to see an intermediate file
    # df_cleaned.to_csv('data/cleaned.csv', index=False)

    return df_cleaned

def remove_emoji_from_dataframe(df):
    # Make a copy to avoid modifying the original dataframe
    df_copy = df.copy()
    
    # Define emoji pattern
    emoji_pattern = re.compile(
        "[" 
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  # Enclosed characters
        u"\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        u"\U00002500-\U00002BEF"  # Chinese/Japanese/Korean characters
        u"\U00002600-\U000026FF"  # Miscellaneous Symbols
        u"\U0001f926-\U0001f937"  # Face symbols
        u"\U00010000-\U0010ffff"  # Extra Unicode characters
        u"\u2640-\u2642"          # Gender symbols
        u"\u2600-\u2B55"          # Miscellaneous symbols
        u"\u200d"                 # Zero width joiner
        u"\u23cf"                 # Control character
        u"\u23e9"                 # Play button
        u"\u231a"                 # Watch
        u"\ufe0f"                 # Variation selector
        u"\u3030"                 # Wavy dash
        "]+", 
        flags=re.UNICODE
    )
    
    if 'body' in df_copy.columns:
        # Handle NaN values and non-string data
        df_copy['body'] = df_copy['body'].astype(str)
        df_copy['body'] = df_copy['body'].apply(lambda x: emoji_pattern.sub(r'', x) if pd.notna(x) else x)
    else:
        raise KeyError("The dataframe does not contain a 'body' column")
    
    ## if you want to see an intermediate file
    df_copy.to_csv('data/cleaned.csv', index=False)
    
    return df_copy

# duplicate comments
def remove_duplicates(df):
    df_cleaned = df.drop_duplicates(subset=['body'], keep='first')

    return df_cleaned

def clean_reddit_body(text):
    if pd.isna(text):
        return text
    
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    
    text = unescape(text)
    
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Keep paragraph breaks
    text = re.sub(r' +', ' ', text)  # Multiple spaces to single
    
    text = text.strip()
    
    return text

def contains_quote(text):
    if pd.isna(text):
        return False
    return bool(re.search(r'^>', text, flags=re.MULTILINE))

def jsonl_to_csv(jsonl_file, csv_file):
    df = pd.read_json(jsonl_file, lines=True)
    print(df.shape)
    # df.to_csv(csv_file, index=False)

def jsonl_to_csv_demo(jsonl_file, csv_file, n=10):
    df = pd.read_json(jsonl_file, lines=True)
    df.head(n).to_csv(csv_file, index=False)  # Only first n rows

if __name__ == "__main__":
    ### smaller version of the file
    # jsonl_to_csv_demo(artic_shift_comments, 'data/articshift_comments_DEMO.csv', 10)
    ### largest verison of the file
    # jsonl_to_csv(artic_shift_comments, 'data/articshift_comments_RAW_tester.csv')

    # df_test = remove_deleted_fix_whitespace(filtered_artic_shift_comments_2)
    # df_test = remove_emoji_from_dataframe(df_test)

    df = pd.read_csv("/home/m210/NLP4CA/data/cleaned.csv")
    has_quotes_mask = df['body'].apply(contains_quote)

    df_with_quotes = df[has_quotes_mask].copy()
    df_no_quotes = df[~has_quotes_mask].copy()

    df_no_quotes['body'] = df_no_quotes['body'].apply(clean_reddit_body)

    output_no_quotes = filtered_artic_shift_comments_2.parent / "articshift_filtered_comments_v2_no_quotes.csv"
    output_with_quotes = filtered_artic_shift_comments_2.parent / "articshift_filtered_comments_v2_with_quotes.csv"

    df_no_quotes.to_csv(output_no_quotes, index=False)
    df_with_quotes.to_csv(output_with_quotes, index=False)

    print(f"Processing complete!")
    print(f"Total comments: {len(df)}")
    print(f"Comments without quotes (cleaned): {len(df_no_quotes)}")
    print(f"Comments with quotes (for review): {len(df_with_quotes)}")
    print(f"\nFiles saved:")
    print(f"  - {output_no_quotes}")
    print(f"  - {output_with_quotes}")