# Topic Modelling for the People - https://maria-antoniak.github.io/2022/07/27/topic-modeling-for-the-people.html
# Some important notes about this - we may not necessarily be able to follow some of these rules completely because we're dealing
# with data that may contain all English, all Creolese, or a mix of English and Creolese. 

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
    print(df.head())

    # remove NaNs + "[deleted]" + "[removed]"
    df_cleaned = df[(df['text'].notna()) & (df['text'] != '[deleted]') & (df['text'] != '[removed]') ]
    # check for completely empty rows
    df_cleaned = df_cleaned[df_cleaned['text'].str.strip() != '']
    print(df_cleaned.head())

    df_cleaned['text'] = df_cleaned['text'].str.replace(r'\s+', ' ', regex=True).str.strip()

    return df_cleaned

# emojis look like empty cells in Excel - need to be removed
def remove_emoji_only_responses(df):
    """
    Remove responses that are likely just emojis or very short
    """
    # Remove based on character length (emojis are typically 1-4 characters)
    df_cleaned = df[df['text'].str.len() > 4]
    
    return df_cleaned

# duplicate comments
def remove_duplicates(df):
    df_cleaned = df.drop_duplicates(subset=['text'], keep='first')

    return df_cleaned

# filters length AND save
def filter_length_and_save(df, min_words, save_name):
    df['word_count'] = df['text'].str.split().str.len()
    
    min_words = 5  
    df_cleaned = df[df['word_count'] >= min_words]
    df_cleaned.to_csv('data/'+save_name, index=False)

# encompasses all helper functions
# outputs - cleaned data file into the data folder
# see "imports.py" for variable definitions
def all_cleaning(file_name, min_words, save_name):
    df_cleaned = remove_deleted_fix_whitespace(file_name)
    df_cleaned = remove_emoji_only_responses(df_cleaned)
    df_cleaned = remove_duplicates(df_cleaned)

    # remove text of certain length
    filter_length_and_save(df_cleaned, min_words, save_name)

if __name__=="__main__":
    ## Change this save file name everytime you change the file!!
    save_file_name = "curated_raw_data_cleaned.csv"
    all_cleaning(raw_curated_file, 10, save_file_name)