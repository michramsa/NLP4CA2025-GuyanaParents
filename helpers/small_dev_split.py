
### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

if __name__ == "__main__":
    SEED = 42
    np.random.seed(SEED)

    df = pd.read_csv(final_cleaned_no_quotes_no_url)

    development_sample_size = 50
    development_indices = np.random.choice(df.index, size=development_sample_size, replace=False)

    df_development = df.loc[development_indices].copy()
    df_main = df.drop(development_indices).copy()

    ### change these filenames as needed!!!!!
    cb_dev_output_file = Path(final_cleaned_no_quotes_no_url).parent / 'codebook_development_sample.csv'
    train_output_file = Path(final_cleaned_no_quotes_no_url).parent / 'ashift_dataset_v2.csv'
    df_development.to_csv(cb_dev_output_file, index=False)
    df_main.to_csv(train_output_file, index=False)

    print(f"Development sample: {len(df_development)} comments")
    print(f"Main dataset: {len(df_main)} comments")
    print(f"Random seed used: {SEED}")