### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################
import json

def build_id_lookup(jsonl_path):
    id_to_toplevel = {}

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                # turn JSON into dictionary
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            comment_id = record.get("id", "")
            parent_id = record.get("parent_id", "")

            # t3_ prefix  =  direct reply to a post  =  top-level comment
            # t1_ prefix  =  reply to another comment =  not top-level
            id_to_toplevel[comment_id] = parent_id.startswith("t3_")

    return id_to_toplevel


def lookup_toplevel(comment_id, id_to_toplevel):
    return id_to_toplevel.get(comment_id, None)


def add_toplevel_column(jsonl_path, csv_path, output_path):
    id_to_toplevel = build_id_lookup(jsonl_path)

    df = pd.read_csv(csv_path, dtype=str)
    df["TL_comment"] = df["id"].apply(lookup_toplevel, id_to_toplevel=id_to_toplevel)

    unmatched = df["TL_comment"].isna().sum()
    if unmatched:
        print(f"Warning: {unmatched} row(s) had no matching ID in the JSONL "
              f"and will have NaN in TL_comment.")

    columns = [
        "author", "body", "id", "created_utc", "date",
        "year", "month", "year_month", "word_count", "char_count",
        "matching_patterns", "TL_comment"
    ]
    df[columns].to_csv(output_path, index=False)
    print(f"Done. Output written to: {output_path}")

def split_by_toplevel(input_path, toplevel_output_path, replies_output_path):
    df = pd.read_csv(input_path)

    toplevel_df = df[df["TL_comment"] == True]
    replies_df = df[df["TL_comment"] == False]

    toplevel_df.to_csv(toplevel_output_path, index=False)
    replies_df.to_csv(replies_output_path, index=False)

    print(f"Top-level comments written to: {toplevel_output_path} ({len(toplevel_df)} rows)")
    print(f"Replies written to: {replies_output_path} ({len(replies_df)} rows)")

if __name__ == "__main__":

    # add_toplevel_column(jsonl_path=raw_data_file,csv_path= quartile_comments,output_path= "X")

    split_by_toplevel(input_path=TL_quartile_comments,
                      toplevel_output_path="TL_iter4_quartile_comments.csv",
                      replies_output_path="Reply_iter4_quartile_comments.csv")