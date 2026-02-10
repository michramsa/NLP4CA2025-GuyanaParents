### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################


# File Purpose: Takes a raw Articshift file of comments (in JSONL format), cleans it for whitespace, emojis, deleted users, etc.

# data has text which are empty or otherwise unneeded, fix whitespace
def remove_deleted_fix_whitespace_df(df):
    """
    Modified version that works with DataFrame directly.
    """
    # Remove rows where author is "[deleted]" OR body is "[deleted]" or "[removed]" or NaN
    df_cleaned = df[
        (df['author'] != '[deleted]') &
        (df['body'].notna()) & 
        (df['body'] != '[deleted]') & 
        (df['body'] != '[removed]')
    ].copy()
    
    # Check for completely empty rows
    df_cleaned = df_cleaned[df_cleaned['body'].str.strip() != '']
    
    # Fix whitespace
    df_cleaned['body'] = df_cleaned['body'].str.replace(r'\s+', ' ', regex=True).str.strip()
    
    print(f"Removed {len(df) - len(df_cleaned)} deleted/removed comments")
    
    return df_cleaned

# NEW: Filter out bot comments
def remove_bots(df):
    """
    Remove comments from known bots and accounts with 'bot' in their username.
    """
    # Common bot keywords - add more as needed
    bot_keywords = ['bot', 'automoderator']
    
    # Create a pattern to match any of the bot keywords (case-insensitive)
    bot_pattern = '|'.join(bot_keywords)
    
    # Filter out bots
    df_cleaned = df[~df['author'].str.lower().str.contains(bot_pattern, na=False)]
    
    print(f"Removed {len(df) - len(df_cleaned)} bot comments")
    
    return df_cleaned

def clean_reddit_markdown(text):
    """
    Remove Reddit-specific markdown, formatting, and references.
    """
    if pd.isna(text):
        return text
    
    # Remove bold markdown
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    
    # Remove italic markdown
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    
    # Remove strikethrough
    text = re.sub(r'~~(.+?)~~', r'\1', text)
    
    # Remove spoiler tags
    text = re.sub(r'>!(.+?)!<', r'\1', text)
    
    # Replace subreddit links with placeholder
    # Must have word boundary or whitespace before 'r/' to avoid matching "December/January"
    text = re.sub(r'(?:^|\s)(r/\w+)', r' [SUBREDDIT]', text)
    
    # Replace user mentions with placeholder
    # Must have word boundary or whitespace before 'u/' 
    text = re.sub(r'(?:^|\s)(u/\w+)', r' [USER]', text)
    
    # Remove extra whitespace that may have been created
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def remove_emoji_from_text(text):
    """
    Remove both Unicode emojis and text-based emoticons from text.
    Can be used with df['body'].apply()
    """
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # First, remove Unicode emojis
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
    text = emoji_pattern.sub(r'', text)
    
    # Second, remove text-based emoticons
    # Common emoticons patterns
    emoticon_patterns = [
        r':\)',      # :)
        r':\(',      # :(
        r':D',       # :D
        r':P',       # :P
        r':p',       # :p
        r':\|',      # :|
        r':/',       # :/
        r':\\',      # :\
        r':o',       # :o
        r':O',       # :O
        r';-?\)',    # ;) or ;-)
        r';-?\(',    # ;( or ;-(
        r':-?\)',    # :-) or :)
        r':-?\(',    # :-( or :(
        r':-?D',     # :-D or :D
        r':-?P',     # :-P or :P
        r':-?p',     # :-p or :p
        r':-?\|',    # :-| or :|
        r':-?/',     # :-/ or :/
        r':-?\\',    # :-\ or :\
        r':-?o',     # :-o or :o
        r':-?O',     # :-O or :O
        r'<3',       # <3 (heart)
        r'</3',      # </3 (broken heart)
        r'=\)',      # =)
        r'=\(',      # =(
        r'=D',       # =D
        r'=-?\)',    # =-)
        r'=-?\(',    # =-(
        r'XD',       # XD
        r'xD',       # xD
        r'T_T',      # T_T
        r'T-T',      # T-T
        r'>:\(',     # >:(
        r'>:-\(',    # >:-(
        r':3',       # :3
        r':\*',      # :*
        r':-?\*',    # :-*
        r'\^_\^',    # ^_^
        r'\^-\^',    # ^-^
        r'-_-',      # -_-
        r'o.o',      # o.o
        r'o_o',      # o_o
        r'O_O',      # O_O
        r'0_0',      # 0_0
        r'>_<',      # >_
        r'<_<',      # <_
        r'>_>',      # >_>
        r'\^\^',     # ^^
        r'~_~',      # ~_~
        r'-\.-',     # -.-
        r'¯\\_\(ツ\)_/¯',  # shrug
        r'\(╯°□°\)╯︵ ┻━┻',  # table flip
    ]
    
    # Remove each emoticon pattern
    for pattern in emoticon_patterns:
        # Use word boundaries or spaces to avoid removing parts of words
        text = re.sub(r'\s' + pattern + r'(?:\s|$)', ' ', text)
        text = re.sub(r'^' + pattern + r'(?:\s|$)', '', text)
    
    # Clean up any extra whitespace created
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

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

def reduce_csv_columns(input_file, output_filename, columns_to_drop):
    df = pd.read_csv(input_file)
    
    df_reduced = df.drop(columns=columns_to_drop, errors='ignore')
    
    output_file = Path(input_file).parent / output_filename
    
    df_reduced.to_csv(output_file, index=False)
    
    # Print summary
    print(f"Original columns: {len(df.columns)}")
    print(f"Remaining columns: {len(df_reduced.columns)}")
    print(f"Columns dropped: {len(columns_to_drop)}")
    print(f"\nFile saved: {output_file}")

def replace_urls(text):
    if pd.isna(text):
        return text
    
    url_pattern = r'http[s]?://\S+|www\.\S+'
    text = re.sub(url_pattern, '[URL]', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def replace_urls_and_save(input_filename, output_filename):
    df = pd.read_csv(input_filename)

    df['body_cleaned'] = df['body'].apply(replace_urls)

    df_output = df[['author', 'body_cleaned', 'id']]

    output_file = Path(input_filename).parent / output_filename
    df_output.to_csv(output_file, index=False)

    print(f"Successfully processed {len(df_output)} rows")
    print(f"Saved to: {output_file}")

def jsonl_to_csv(jsonl_file, csv_file):
    df = pd.read_json(jsonl_file, lines=True)
    print(df.shape)
    df.to_csv(csv_file, index=False)

def jsonl_to_csv_demo(jsonl_file, csv_file, n=10):
    df = pd.read_json(jsonl_file, lines=True)
    df.head(n).to_csv(csv_file, index=False)  # Only first n rows

# NEW: Function to analyze comment length distribution
def analyze_comment_lengths(df, column='body'):
    """
    Analyze and print statistics about comment lengths.
    """
    df['word_count'] = df[column].str.split().str.len()
    df['char_count'] = df[column].str.len()
    
    print("\n=== Comment Length Distribution ===")
    print(f"Total comments: {len(df)}")
    print(f"\nWord Count Statistics:")
    print(df['word_count'].describe())
    print(f"\nCharacter Count Statistics:")
    print(df['char_count'].describe())
    
    # Print some percentiles
    print(f"\nWord Count Percentiles:")
    for p in [10, 25, 50, 75, 90, 95, 99]:
        print(f"  {p}th percentile: {df['word_count'].quantile(p/100):.0f} words")
    
    return df

def clean_reddit_data_pipeline(input_jsonl_path, output_csv_path):
    """
    Pipeline to clean Reddit data from JSONL to final cleaned CSV.
    
    Args:
        input_jsonl_path: Path to input JSONL file
        output_csv_path: Path for final cleaned CSV output
    """
    
    # Step 1: Convert JSONL to CSV (initial conversion)
    print("Step 1: Converting JSONL to CSV...")
    temp_csv = '0_data/temp_initial.csv'
    jsonl_to_csv(input_jsonl_path, temp_csv)
    
    # Step 2: Load as DataFrame and clean
    print("Step 2: Loading and cleaning data...")
    df = pd.read_csv(temp_csv)
    
    # Step 3: Remove deleted content and fix whitespace
    print("Step 3: Removing deleted content and fixing whitespace...")
    df = remove_deleted_fix_whitespace_df(df)

    # Step 4: Remove bots
    print("Step 4: Removing bot comments...")
    df = remove_bots(df)
    
    # Step 5: Clean Reddit markdown
    print("Step 5: Cleaning Reddit markdown formatting...")
    df['body'] = df['body'].apply(clean_reddit_markdown)
    
    # Step 6: Remove emojis
    print("Step 6: Removing emojis...")
    df['body'] = df['body'].apply(remove_emoji_from_text)
    
    # Step 7: Remove duplicates
    print("Step 7: Removing duplicate comments...")
    df = remove_duplicates(df)
    
    # Step 8: Clean Reddit body text
    print("Step 8: Cleaning Reddit body text...")
    df['body'] = df['body'].apply(clean_reddit_body)
    
    # Step 9: Replace URLs
    print("Step 9: Replacing URLs with [URL] placeholder...")
    df['body'] = df['body'].apply(replace_urls)
    
    # Step 10: Filter out quotes (optional - based on your needs)
    print("Step 10: Filtering quotes...")
    df = df[~df['body'].apply(contains_quote)]  # Keep only non-quotes
    
    # Step 11: Reduce columns (keep only needed columns)
    print("Step 11: Selecting final columns...")
    final_columns = ['author', 'body', 'id']  # Adjust as needed
    df = df[final_columns]
    
    # Step 12: Analyze and save
    print("Step 12: Analyzing comment lengths...")
    df = analyze_comment_lengths(df, column='body')
    
    # Step 13: Save final cleaned data
    print(f"Step 13: Saving cleaned data to {output_csv_path}...")
    df.to_csv(output_csv_path, index=False)
    
    print(f"\n✓ Cleaning complete!")
    print(f"  Total comments: {len(df)}")
    print(f"  Output saved to: {output_csv_path}")
    
    return df

if __name__ == "__main__":
    # Define paths
    input_jsonl = raw_data_file
    output_cleaned = '0_data/2026_Guyana_comments_CLEANED_FINAL.csv'
    
    # Run the complete pipeline
    cleaned_df = clean_reddit_data_pipeline(input_jsonl, output_cleaned)
