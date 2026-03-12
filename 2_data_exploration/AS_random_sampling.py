### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

def combine_csvs(file1, file2, output_filename):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    print(f"File 1: {len(df1)} rows")
    print(f"File 2: {len(df2)} rows")

    combined = pd.concat([df1, df2], ignore_index=True)
    combined = combined.drop_duplicates(subset="body", keep="first")

    print(f"After deduplication: {len(combined)} rows")
    print(f"Duplicates removed: {len(df1) + len(df2) - len(combined)}")

    combined.to_csv(output_filename, index=False)
    print(f"Saved to: {output_filename}")

def random_sampling(input_file, sample_size, num_bins, equal_width_output, quantile_output):
    df = pd.read_csv(input_file)
    print(f"Total comments: {len(df)}")
    print(f"Word count range: {df['word_count'].min()} - {df['word_count'].max()}")
    print(f"Word count mean: {df['word_count'].mean():.1f}")
    print(f"Word count median: {df['word_count'].median():.1f}")
    print()

    # --- Sample 1: Equal-width bins ---
    df["ew_bin"] = pd.cut(df["word_count"], bins=num_bins)
    per_bin = sample_size // num_bins

    ew_samples = []
    for bin_label, group in df.groupby("ew_bin", observed=True):
        n = min(per_bin, len(group))
        ew_samples.append(group.sample(n=n, random_state=42))

    ew_sample = pd.concat(ew_samples, ignore_index=True).drop(columns=["ew_bin"])

    print("=== Equal-Width Bins ===")
    print(f"Target per bin: {per_bin}")
    print(f"Actual sample size: {len(ew_sample)}")
    print(f"(May be < {sample_size} if some bins have fewer than {per_bin} comments)")
    print()
    for bin_label, group in df.groupby("ew_bin", observed=True):
        sampled = min(per_bin, len(group))
        print(f"  {bin_label}: {len(group)} available, {sampled} sampled")
    print()

    ew_sample.to_csv(equal_width_output, index=False)
    print("Saved equal width!")

    # --- Sample 2: Quantile-based bins ---
    df["q_bin"] = pd.qcut(df["word_count"], q=num_bins, duplicates="drop")
    actual_bins = df["q_bin"].nunique()
    per_bin_q = sample_size // actual_bins

    q_samples = []
    for bin_label, group in df.groupby("q_bin", observed=True):
        n = min(per_bin_q, len(group))
        q_samples.append(group.sample(n=n, random_state=42))

    q_sample = pd.concat(q_samples, ignore_index=True).drop(columns=["ew_bin", "q_bin"])

    print("=== Quantile-Based Bins ===")
    print(f"Number of bins: {actual_bins}")
    print(f"Target per bin: {per_bin_q}")
    print(f"Actual sample size: {len(q_sample)}")
    print()
    for bin_label, group in df.groupby("q_bin", observed=True):
        sampled = min(per_bin_q, len(group))
        print(f"  {bin_label}: {len(group)} available, {sampled} sampled")
    print()

    q_sample.to_csv(quantile_output, index=False)
    print("Saved quantile!")


if __name__ == "__main__":
#  outfile = PROJECT_ROOT / "0_data" / "2026_Guyana_comments_CLEANED_WCDA_combined.csv"
#  combine_csvs(cleaned_2026_Guyana_comments_WCDA_50, cleaned_2026_Guyana_comments_WCDA_100, outfile)

    input_file = PROJECT_ROOT / "bootstrap_output" / "iter4_matched.csv"
    sample_size = 2000
    num_bins = 10
    eq_width_out = PROJECT_ROOT / "0_data" / "iter4_equal_width_comments.csv"
    quart_out = PROJECT_ROOT / "0_data" / "iter4_quartile_comments.csv"

    random_sampling(input_file, sample_size, num_bins, eq_width_out, quart_out)

