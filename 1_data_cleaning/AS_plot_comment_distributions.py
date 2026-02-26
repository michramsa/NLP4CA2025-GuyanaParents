### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

STYLE = {
    "bar_color":   "#4C72B0",
    "accent":      "#DD8452",
    "bg":          "#F8F9FA",
    "grid_color":  "#DDDDDD",
    "font_family": "DejaVu Sans",
    "title_size":  14,
    "label_size":  11,
    "tick_size":   10,
}

MONTH_LABELS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

def load_data(filename):
    df = pd.read_csv(filename)
    df["year"]  = df["year"].astype(int)
    df["month"] = df["month"].astype(int)
    return df


def apply_base_style(ax, bg, grid_color):
    """Apply consistent background and grid styling to an Axes."""
    ax.set_facecolor(bg)
    ax.xaxis.grid(True, color=grid_color, linestyle="--", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(grid_color)


def add_value_labels(ax, bars, fmt="{:,.0f}"):
    """Annotate each bar with its numeric value."""
    x_max = max(bar.get_width() for bar in bars)
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + x_max * 0.01,
            bar.get_y() + bar.get_height() / 2,
            fmt.format(width),
            va="center", ha="left",
            fontsize=STYLE["tick_size"] - 1,
            color="#444444",
        )

def plot_yearly(df, output_dir):
    counts = (
        df.groupby("year")
        .size()
        .reset_index(name="count")
        .sort_values("year")          # chronological order, oldest at bottom
    )

    fig, ax = plt.subplots(figsize=(9, max(4, len(counts) * 0.55)))
    fig.patch.set_facecolor(STYLE["bg"])
    apply_base_style(ax, STYLE["bg"], STYLE["grid_color"])

    bars = ax.barh(
        counts["year"].astype(str),
        counts["count"],
        color=STYLE["bar_color"],
        edgecolor="white",
        linewidth=0.6,
        height=0.65,
        zorder=3,
    )

    add_value_labels(ax, bars)

    ax.set_xlabel("Number of Comments", fontsize=STYLE["label_size"],
                  fontfamily=STYLE["font_family"], labelpad=8)
    ax.set_ylabel("Year", fontsize=STYLE["label_size"],
                  fontfamily=STYLE["font_family"], labelpad=8)
    ax.set_title("Distribution of Comments per Year",
                 fontsize=STYLE["title_size"], fontweight="bold",
                 fontfamily=STYLE["font_family"], pad=14)
    ax.tick_params(axis="both", labelsize=STYLE["tick_size"])
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    # Extend x-axis slightly to fit value labels
    ax.set_xlim(0, counts["count"].max() * 1.15)

    fig.tight_layout()
    path = os.path.join(output_dir, "100WC_comments_per_year.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")

def plot_monthly(df, output_dir):
    years = sorted(df["year"].unique())

    for year in years:
        yearly_df = df[df["year"] == year]

        # Build a complete 12-month series (fills 0 for missing months)
        month_counts = (
            yearly_df.groupby("month")
            .size()
            .reindex(range(1, 13), fill_value=0)
            .reset_index()
        )
        month_counts.columns = ["month", "count"]
        month_counts["label"] = month_counts["month"].apply(
            lambda m: MONTH_LABELS[m - 1]
        )

        fig, ax = plt.subplots(figsize=(9, 5))
        fig.patch.set_facecolor(STYLE["bg"])
        apply_base_style(ax, STYLE["bg"], STYLE["grid_color"])

        bars = ax.barh(
            month_counts["label"],
            month_counts["count"],
            color=STYLE["accent"],
            edgecolor="white",
            linewidth=0.6,
            height=0.65,
            zorder=3,
        )

        add_value_labels(ax, bars)

        ax.set_xlabel("Number of Comments", fontsize=STYLE["label_size"],
                      fontfamily=STYLE["font_family"], labelpad=8)
        ax.set_ylabel("Month", fontsize=STYLE["label_size"],
                      fontfamily=STYLE["font_family"], labelpad=8)
        ax.set_title(f"Distribution of Comments per Month — {year}",
                     fontsize=STYLE["title_size"], fontweight="bold",
                     fontfamily=STYLE["font_family"], pad=14)
        ax.tick_params(axis="both", labelsize=STYLE["tick_size"])
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

        max_count = month_counts["count"].max()
        ax.set_xlim(0, max_count * 1.15 if max_count > 0 else 10)

        fig.tight_layout()
        path = os.path.join(output_dir, f"100WC_comments_{year}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved: {path}")

def main(input_path, output_dir="figures"):
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading data from: {input_path}")
    df = load_data(input_path)
    print(f"  {len(df):,} rows | years: {sorted(df['year'].unique())}")

    plot_yearly(df, output_dir)
    plot_monthly(df, output_dir)

    print("\nDone! All figures saved to:", output_dir)


if __name__ == "__main__":
    main(
        input_path= cleaned_2026_Guyana_comments_WCDA_100,
        output_dir="figures/WCDA_100_distributions",
    )