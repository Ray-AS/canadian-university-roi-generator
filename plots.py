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

    print(f"Plot Tuition vs. Earnings saved: {path / 'tuition_vs_earnings.png.png'}")


def plot_roi_vs_enrollment(df: pd.DataFrame, path: Path = DEFAULT_PATH):
    pass


def plot_debt_to_income(df: pd.DataFrame, path: Path = DEFAULT_PATH):
    df_sorted = df.sort_values("debt_to_income", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(
        range(len(df_sorted)), df_sorted["debt_to_income"], alpha=0.7, edgecolor="black"
    )

    ax.axvline(x=1.0, color="red", linestyle="--", linewidth=1.5, alpha=0.6)

    ax.set_yticks(range(len(df_sorted)))
    ax.set_yticklabels(
        [field.replace("_", " ").title() for field in df_sorted["field"]]
    )
    ax.set_xlabel("Debt-to-Income Ratio")
    ax.set_title("Student Debt Burden by Field of Study")
    # ax.set_title(
    #     "Student Debt Burden by Field of Study\nEstimated Debt / Median Earnings (After 2 Years)"
    # )

    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        value = row["debt_to_income"]
        ax.text(value + 0.05, i, f"{value:.2f}x", va="center", fontsize=12)

    x_min, x_max = df["debt_to_income"].min(), df["debt_to_income"].max()
    x_buffer = (x_max - x_min) * 0.15
    ax.set_xlim(x_min - x_buffer, x_max + x_buffer)

    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(path / "debt_to_income_ratio.png", dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Plot Debt / Income Ratio saved: {path / 'debt_to_income_ratio.png'}")


def plot_payback_years(df: pd.DataFrame, path: Path = DEFAULT_PATH):
    df_sorted = df.sort_values("payback_years", ascending=True)

    # Cap at 30 years for visualization
    df_sorted["payback_years_capped"] = df_sorted["payback_years"].clip(upper=30)

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(
        range(len(df_sorted)),
        df_sorted["payback_years_capped"],
        alpha=0.7,
        edgecolor="black",
    )

    ax.axvline(x=10, color="green", linestyle="--", linewidth=1.5, alpha=0.4)
    ax.axvline(x=20, color="red", linestyle="--", linewidth=1.5, alpha=0.4)

    ax.set_yticks(range(len(df_sorted)))
    ax.set_yticklabels(
        [field.replace("_", " ").title() for field in df_sorted["field"]]
    )
    ax.set_xlabel("Years to Pay Off Student Debt")
    ax.set_title("How Long Will It Take to Pay Off Student Debt?")
    # ax.set_title(
    #     "How Long Will It Take to Pay Off Student Debt?\nAssuming 10% of Post-Tax Income Goes to Debt Repayment"
    # )

    # Add value labels on bars
    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        value = row["payback_years"]
        display_value = min(value, 30)
        label = f"{value:.1f} years" if value < 30 else "30+ years"
        ax.text(display_value + 0.5, i, label, va="center", fontsize=12)

    ax.grid(axis="x", alpha=0.3)
    ax.set_xlim(0, 32)

    plt.tight_layout()
    plt.savefig(path / "payback_years.png", dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Plot Payback Years saved: {path / 'payback_years.png'}")


def plot_roi_by_field(df: pd.DataFrame, output_path: Path):
    df_sorted = df.sort_values("roi_5yr_w_tuition", ascending=False)

    fig, ax = plt.subplots(figsize=(12, 8))

    x = range(len(df_sorted))
    width = 0.35

    ax.barh(
        [i - width / 2 for i in x],
        df_sorted["roi_5yr_w_tuition"],
        width,
        label="ROI (Tuition)",
        alpha=0.7,
        edgecolor="black",
    )

    ax.barh(
        [i + width / 2 for i in x],
        df_sorted["roi_5yr_w_debt"],
        width,
        label="ROI (Debt)",
        alpha=0.7,
        edgecolor="black",
        color="red",
    )

    # Calculate and add average ROI line
    avg_roi_tuition = df["roi_5yr_w_tuition"].mean()
    avg_roi_debt = df["roi_5yr_w_debt"].mean()
    ax.axvline(
        x=avg_roi_tuition,
        color="blue",
        linestyle="--",
        linewidth=1.5,
        alpha=0.5,
        label=f"Avg ROI (Tuition): {avg_roi_tuition:.2f}",
    )
    ax.axvline(
        x=avg_roi_debt,
        color="red",
        linestyle="--",
        linewidth=1.5,
        alpha=0.5,
        label=f"Avg ROI (Debt): {avg_roi_debt:.2f}",
    )

    ax.set_yticks(x)
    ax.set_yticklabels(
        [field.replace("_", " ").title() for field in df_sorted["field"]]
    )
    ax.set_xlabel("5-Year Return on Investment (ROI)")
    ax.set_title("5-Year ROI by Field of Study")
    # ax.set_title(
    #     "5-Year ROI by Field of Study\nComparing Investment Based on Tuition vs. Debt"
    # )
    ax.legend(loc="upper right")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path / "roi_by_field.png", dpi=300, bbox_inches="tight")
    plt.close()
    print(
        f"Plot return on investment by field saved: {output_path / 'roi_by_field.png'}"
    )


def generate_all_plots(df: pd.DataFrame, output_path: Path = Path("figures")):
    output_path.mkdir(parents=True, exist_ok=True)

    print("Generating plots...")
    print("=" * 60)

    plot_tuition_vs_earnings(df, output_path)
    plot_roi_by_field(df, output_path)
    plot_debt_to_income(df, output_path)
    plot_debt_to_income(df, output_path)

    print("=" * 60)
    print(f"All plots saved to: {output_path.absolute()}\n")
