
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

# needs a filename in the following format: 'data/cleaned.csv'
def remove_emoji_from_dataframe(df, filename):
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
    df_copy.to_csv(filename, index=False)
    
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

# must include ".csv" in the argument for the filename
# example: "articshift_filtered_comments_v2_no_quotes.csv"
def remove_quotes(csv_filename, no_quotes_filename, with_quotes_filename):
    df = pd.read_csv(csv_filename)
    has_quotes_mask = df['body'].apply(contains_quote)

    df_with_quotes = df[has_quotes_mask].copy()
    df_no_quotes = df[~has_quotes_mask].copy()

    df_no_quotes['body'] = df_no_quotes['body'].apply(clean_reddit_body)

    output_no_quotes = filtered_artic_shift_comments_2.parent / no_quotes_filename
    output_with_quotes = filtered_artic_shift_comments_2.parent / with_quotes_filename

    df_no_quotes.to_csv(output_no_quotes, index=False)
    df_with_quotes.to_csv(output_with_quotes, index=False)

    print(f"Processing complete!")
    print(f"Total comments: {len(df)}")
    print(f"Comments without quotes (cleaned): {len(df_no_quotes)}")
    print(f"Comments with quotes (for review): {len(df_with_quotes)}")
    print(f"\nFiles saved:")
    print(f"  - {output_no_quotes}")
    print(f"  - {output_with_quotes}")

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
    # df.to_csv(csv_file, index=False)

def jsonl_to_csv_demo(jsonl_file, csv_file, n=10):
    df = pd.read_json(jsonl_file, lines=True)
    df.head(n).to_csv(csv_file, index=False)  # Only first n rows

if __name__ == "__main__":

    ### some random tester files i made
    # ## smaller version of the file
    # jsonl_to_csv_demo(artic_shift_comments, 'data/articshift_comments_DEMO.csv', 10)
    # ## largest verison of the file
    # jsonl_to_csv(artic_shift_comments, 'data/articshift_comments_RAW_tester.csv')
    ###

    #### Run this section by section. Start with 1. When 1 is done, comment it, then uncomment and run 2, and so on...

    ### START 1 ###

    ## 1. cleaning whitespace and emojis
    df_test = remove_deleted_fix_whitespace(filtered_artic_shift_comments_2)

    ### when i originally made this, i used "cleaned.csv" so that's what you'll see... that will be replaced by whatever you change the filename variable to
    filename = 'put something here'
    df_test = remove_emoji_from_dataframe(df_test, filename)

    ### END 1 ###

    ### START 2 ###
    
    # ## 2. cleaning comments that quote other people/ may be in reply to others
    # # the location of this cleaned.csv file/rather the path name is variable and needs to be updated
    # cleaned_filename = "/home/epi2melabs/NLP4CA2025-GuyanaParents/data/cleaned.csv"
    # no_quote_filename = "articshift_filtered_comments_v2_no_quotes.csv"
    # with_quote_filename = "articshift_filtered_comments_v2_with_quotes.csv"
    # remove_quotes(cleaned_filename, no_quote_filename, with_quote_filename)

    ### END 2 ###

    ### START 3 ###

    # ## 3. removing extra comments - we'll still keep the original in case we need it but for reading purposes, this will make things easier
    # drop_columns = ['author_flair_css_class','author_flair_text','can_gild','controversiality','created_utc','distinguished','edited',
    #                 'gilded','is_submitter','link_id','parent_id','permalink','retrieved_on','score','stickied','subreddit','subreddit_id',
    #                 'subreddit_type','name','ups','no_follow','send_replies','author_flair_template_id','approved_by','banned_by','body_html',
    #                 'likes','mod_reports','num_reports','removal_reason','replies','report_reasons','saved','user_reports','archived','can_mod_post',
    #                 'score_hidden','author_flair_background_color','author_flair_richtext','author_flair_text_color','author_flair_type','rte_mode',''
    #                 'author_cakeday','author_created_utc','author_fullname','collapsed','collapsed_reason','subreddit_name_prefixed','gildings',
    #                 'author_patreon_flair','quarantined','all_awardings','locked','total_awards_received','steward_reports','awarders','associated_award',
    #                 'collapsed_because_crowd_control','author_premium','treatment_tags','top_awarded_type','comment_type','collapsed_reason_code',''
    #                 'retrieved_utc','author_is_blocked','unrepliable_reason','editable','_meta','approved_at_utc','banned_at_utc','created',
    #                 'downs','mod_note','mod_reason_by','mod_reason_title','media_metadata','body_sha1','nest_level','matching_patterns']
    
    # # change the filename as needed
    # filename = "/home/epi2melabs/NLP4CA2025-GuyanaParents/data/articshift_filtered_comments_v2_no_quotes.csv"
    # reduce_csv_columns(filename, "simple_ashift_filtered_v2_no_quotes.csv", drop_columns)

    ### END 3 ###

    ### START 4 ###

    # ## 4. removing URLs - let's replace instead of remove

    # ## change the filename
    # filename = "/home/epi2melabs/NLP4CA2025-GuyanaParents/data/simple_ashift_filtered_v2_no_quotes.csv"
    # replace_urls_and_save(filename,"simple_ashift_filtered_v2_no_quotes_URL.csv")