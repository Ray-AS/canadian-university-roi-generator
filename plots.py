from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd

from configs import DEFAULT_PATH


def plot_tuition_vs_earnings(df: pd.DataFrame, path: Path = DEFAULT_PATH):
    fig, ax = plt.subplots(figsize=(12, 8))

    def thousands(x, pos):
        return f"${x * 1e-3:,.0f}k"

    formatter = FuncFormatter(thousands)

    x_min, x_max = df["total_tuition"].min(), df["total_tuition"].max()
    y_min, y_max = (
        df["earnings_2024_adjusted"].min(),
        df["earnings_2024_adjusted"].max(),
    )

    x_buffer = (x_max - x_min) * 0.15
    y_buffer = (y_max - y_min) * 0.15

    ax.set_xlim(x_min - x_buffer, x_max + x_buffer)
    ax.set_ylim(y_min - y_buffer, y_max + y_buffer)

    ax.scatter(
        df["total_tuition"],
        df["earnings_2024_adjusted"],
        s=200,
        alpha=0.6,
        edgecolors="black",
        linewidth=1,
    )

    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Add field labels
    for _, row in df.iterrows():
        ax.text(
            row["total_tuition"],
            row["earnings_2024_adjusted"] + 750,
            row["field"].replace("_", " ").title(),
            fontsize=12,
            ha="center",
        )

    ax.set_xlabel("Total Tuition (4 years, CAD)")
    ax.set_ylabel("Median Earnings 2 Years After Graduation (2024 adjusted, CAD)")
    ax.set_title("Tuition vs Earnings by Field of Study")
    ax.grid(True, alpha=0.3, linestyle="--")

    plt.tight_layout()
    plt.savefig(path / "tuition_vs_earnings.png", dpi=300, bbox_inches="tight")
    plt.close()
