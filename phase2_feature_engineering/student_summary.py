
import pandas as pd


RISK_BINS   = [0.0, 0.20, 0.40, 0.60, 1.01]
RISK_LABELS = ["Low", "Medium", "High", "Critical"]


def build_student_summary(master):
    
    print("  Building student-level summary...")

    summary = master.groupby("student_id").agg(
        avg_grade          = ("grade",            "mean"),
        grade_std          = ("grade",            "std"),
        avg_ai_prob        = ("ai_probability",   "mean"),
        max_ai_prob        = ("ai_probability",   "max"),
        avg_similarity     = ("similarity_score", "mean"),
        avg_drift          = ("style_drift",      "mean"),
        max_drift          = ("style_drift",      "max"),
        avg_delay          = ("submission_delay_hours", "mean"),
        avg_composite_risk = ("composite_risk",   "mean"),
        max_composite_risk = ("composite_risk",   "max"),
        submission_count   = ("submission_id",    "count"),
    ).reset_index()

    # Add risk tier
    summary["risk_tier"] = pd.cut(
        summary["avg_composite_risk"],
        bins   = RISK_BINS,
        labels = RISK_LABELS,
    )

    # Print tier distribution
    tier_counts = summary["risk_tier"].value_counts().sort_index()
    print(f"    {len(summary)} students summarised")
    print(f"    Risk tier distribution:")
    for tier, count in tier_counts.items():
        pct = count / len(summary) * 100
        print(f"      {tier:<10}: {count:>3} students ({pct:.1f}%)")

    return summary
