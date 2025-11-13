import convokit
import pandas as pd
import os
import re
import json
import csv
from pathlib import Path
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer


# Get the project root directory (where your script is)
PROJECT_ROOT = Path(__file__).parent

# Build paths relative to project root
raw_data_file = PROJECT_ROOT / "data" / "guyana_utterances.csv"
clean_data_file = PROJECT_ROOT / "data" / "guyana_utterances_cleaned.csv"
raw_curated_file = PROJECT_ROOT / "data" / "curated_raw_data.csv"
clean_curated_file = PROJECT_ROOT / "data" / "curated_raw_data_cleaned.csv"
artic_shift_comments = PROJECT_ROOT / "data"/ "r_Guyana_comments.jsonl"
artic_shift_posts = PROJECT_ROOT / "data"/ "r_Guyana_posts.jsonl"
filtered_artic_shift_comments_1 = PROJECT_ROOT / "data" / "articshift_filtered_comments.csv"
filtered_artic_shift_comments_2 = PROJECT_ROOT / "data" / "articshift_filtered_comments_v2.csv"