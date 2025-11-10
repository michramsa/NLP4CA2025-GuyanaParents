### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

import json
import csv
import pandas as pd


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
    jsonl_to_csv(artic_shift_comments, 'data/articshift_comments_RAW_tester.csv')