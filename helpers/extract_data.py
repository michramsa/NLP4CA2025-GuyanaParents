import convokit
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_folder = os.path.join(project_root, "data")
print(f"Data folder path: {data_folder}")
os.makedirs(data_folder, exist_ok=True)
print(f"Data directory exists: {os.path.exists(data_folder)}")

# load corpus
print("Downloading corpus...")
corpus = convokit.Corpus(filename=convokit.download("subreddit-Guyana"))
print("Corpus downloaded and loaded successfully")

# turn corpus to df
print("Converting to DataFrame...")
df = corpus.get_utterances_dataframe()
print(f"DataFrame created with {len(df)} rows")

# Define the full path for the CSV file
csv_path = os.path.join(data_folder, "guyana_utterances.csv")
print(f"CSV will be saved to: {csv_path}")

# Save DataFrame to CSV
print("Saving to CSV...")
df.to_csv(csv_path, index=False)
print(f"CSV file saved successfully. File exists: {os.path.exists(csv_path)}")
print(f"File size: {os.path.getsize(csv_path)} bytes")