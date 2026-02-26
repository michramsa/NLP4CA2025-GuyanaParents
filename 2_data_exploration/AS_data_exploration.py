### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

def word_char_count_figs(filename, output_dir=None):
    df = pd.read_csv(filename)
    
    if output_dir is None:
        output_dir = Path(filename).parent
    else:
        output_dir = Path(output_dir)
    
    # fig 1: word count
    plt.figure(figsize=(10, 6))
    plt.hist(df['word_count'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Word Count', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Word Count', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(output_dir / 'word_count_distribution_iter3_non_matched.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Word count distribution saved to {output_dir / 'word_count_distribution_all.png'}")
    
    # fig 2: char count
    plt.figure(figsize=(10, 6))
    plt.hist(df['char_count'], bins=50, color='coral', edgecolor='black', alpha=0.7)
    plt.xlabel('Character Count', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Character Count', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(output_dir / 'char_count_distribution_iter3_non_matched.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Character count distribution saved to {output_dir / 'char_count_distribution_iter3_non_matched.png'}")

if __name__ == "__main__":
    # create figs for word count and char count
    # must be a CSV with the following columns: word_count, char_count

    filename = "/home/epi2melabs/NLP4CA2025-GuyanaParents/bootstrap_output/iter3_non_matched.csv"
    output = "/home/epi2melabs/NLP4CA2025-GuyanaParents/2_data_exploration/figures"
    word_char_count_figs(filename, output)