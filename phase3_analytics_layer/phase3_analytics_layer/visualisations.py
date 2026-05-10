import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")   
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path



BLUE   = "#1A56A0"
TEAL   = "#0F6E56"
AMBER  = "#854F0B"
PURPLE = "#534AB7"
RED    = "#D85A30"


def _ensure_charts_dir(out_dir):
    charts_dir = Path(out_dir) / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    return charts_dir


def plot_semester_trends(trends, out_dir):
    
    charts_dir = _ensure_charts_dir(out_dir)

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")

    ax.plot(trends["semester"], trends["avg_ai_prob"] * 100,
            "o-", color=BLUE, lw=2.2, markersize=7, label="Avg AI probability (%)")
    ax.plot(trends["semester"], trends["anomaly_pct"],
            "s-", color=AMBER, lw=2.2, markersize=7, label="Anomaly rate (%)")
    ax.plot(trends["semester"], trends["avg_risk"] * 100,
            "^-", color=PURPLE, lw=2.2, markersize=7, label="Avg risk score (×100)")

    
    for _, row in trends.iterrows():
        ax.annotate(f"{row['avg_ai_prob']*100:.1f}%",
                    (row["semester"], row["avg_ai_prob"] * 100),
                    textcoords="offset points", xytext=(0, 9),
                    ha="center", fontsize=9, color=BLUE, fontweight="bold")

    ax.set_xlabel("Semester", fontsize=11)
    ax.set_ylabel("Value", fontsize=11)
    ax.set_title("Key Integrity Signals Across Semesters", fontsize=13,
                 fontweight="bold", pad=10)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["Semester 1", "Semester 2", "Semester 3", "Semester 4"])
    ax.legend(fontsize=9.5, framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = charts_dir / "semester_trends.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#FAFAFA")
    plt.close()
    print(f"    Saved: {path}")


def plot_risk_tier_distribution(summary, out_dir):
    
    charts_dir = _ensure_charts_dir(out_dir)

    tier_counts = (summary["risk_tier"]
                   .value_counts()
                   .reindex(["Low", "Medium", "High", "Critical"])
                   .fillna(0))

    colors = [TEAL, AMBER, RED, "#7B1D1D"]
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor("#FAFAFA")

    wedges, texts, autotexts = ax.pie(
        tier_counts,
        labels    = tier_counts.index,
        colors    = colors,
        autopct   = "%1.1f%%",
        startangle= 90,
        pctdistance=0.82,
        wedgeprops = {"width": 0.5},  
    )
    for t in autotexts:
        t.set_fontsize(11)
        t.set_fontweight("bold")

    ax.set_title("Student Risk Tier Distribution\n(500 students)",
                 fontsize=13, fontweight="bold", pad=10)

   
    legend_labels = [f"{tier}: {int(count)} students"
                     for tier, count in tier_counts.items()]
    ax.legend(legend_labels, loc="lower center",
              bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=10)

    path = charts_dir / "risk_tier_distribution.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#FAFAFA")
    plt.close()
    print(f"    Saved: {path}")


def plot_ai_probability_histogram(df, out_dir):
    
    charts_dir = _ensure_charts_dir(out_dir)

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")

    ax.hist(df["ai_probability"], bins=30, color=BLUE,
            edgecolor="white", linewidth=0.5, alpha=0.85)

    ax.axvline(df["ai_probability"].mean(), color=RED, lw=2,
               linestyle="--", label=f"Mean = {df['ai_probability'].mean():.3f}")
    ax.axvline(0.5, color=AMBER, lw=1.5,
               linestyle=":", label="0.5 threshold")

    ax.set_xlabel("AI Probability", fontsize=11)
    ax.set_ylabel("Number of submissions", fontsize=11)
    ax.set_title("Distribution of AI Probability\n(30,000 submissions)",
                 fontsize=13, fontweight="bold", pad=10)
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = charts_dir / "ai_probability_histogram.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#FAFAFA")
    plt.close()
    print(f"    Saved: {path}")


def plot_drift_distribution(df, out_dir):
    
    charts_dir = _ensure_charts_dir(out_dir)

    drift_vals = df["style_drift"].dropna()

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")

    ax.hist(drift_vals, bins=40, color=TEAL,
            edgecolor="white", linewidth=0.5, alpha=0.85)

    ax.axvline(drift_vals.mean(), color=RED, lw=2,
               linestyle="--", label=f"Mean drift = {drift_vals.mean():.3f}")
    ax.axvline(1.0, color=AMBER, lw=1.5,
               linestyle=":", label="Drift = 1.0 (notable threshold)")
    ax.axvline(1.5, color=RED, lw=1.5,
               linestyle="-.", label="Drift = 1.5 (high risk threshold)")

    ax.set_xlabel("Style Drift (cosine distance)", fontsize=11)
    ax.set_ylabel("Number of submissions", fontsize=11)
    ax.set_title("Distribution of Writing Style Drift\n(29,500 valid submissions)",
                 fontsize=13, fontweight="bold", pad=10)
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = charts_dir / "drift_distribution.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#FAFAFA")
    plt.close()
    print(f"    Saved: {path}")


def generate_all_charts(df, summary, trends, out_dir):
   
    print("  Generating charts...")
    plot_semester_trends(trends, out_dir)
    plot_risk_tier_distribution(summary, out_dir)
    plot_ai_probability_histogram(df, out_dir)
    plot_drift_distribution(df, out_dir)
    