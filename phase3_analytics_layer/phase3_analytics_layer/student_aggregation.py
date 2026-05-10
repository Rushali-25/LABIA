import pandas as pd


RISK_BINS   = [0.0, 0.20, 0.40, 0.60, 1.01]
RISK_LABELS = ["Low", "Medium", "High", "Critical"]


def build_student_summary(df):
    
    print("  Building student-level summary...")

    summary = df.groupby("student_id").agg(
        avg_grade          = ("grade",                "mean"),
        grade_std          = ("grade",                "std"),
        avg_ai_prob        = ("ai_probability",       "mean"),
        max_ai_prob        = ("ai_probability",       "max"),
        avg_similarity     = ("similarity_score",     "mean"),
        avg_drift          = ("style_drift",          "mean"),
        max_drift          = ("style_drift",          "max"),
        avg_delay          = ("submission_delay_hours","mean"),
        anomaly_count      = ("anomaly_flag",         lambda x: (x == -1).sum()),
        avg_anomaly_score  = ("anomaly_score",        "mean"),
        avg_composite_risk = ("composite_risk",       "mean"),
        max_composite_risk = ("composite_risk",       "max"),
        submission_count   = ("submission_id",        "count"),
    ).reset_index()

    
    summary["risk_tier"] = pd.cut(
        summary["avg_composite_risk"],
        bins   = RISK_BINS,
        labels = RISK_LABELS,
    )

    
    tier_counts = summary["risk_tier"].value_counts().sort_index()
    print(f"    {len(summary)} students aggregated")
    print(f"    Risk tier distribution:")
    for tier, count in tier_counts.items():
        pct = count / len(summary) * 100
        bar = "█" * int(pct / 2)
        print(f"      {tier:<10} : {count:>3} students ({pct:5.1f}%)  {bar}")

   
    top5 = summary.nlargest(5, "avg_composite_risk")[
        ["student_id", "avg_grade", "avg_ai_prob",
         "max_drift", "anomaly_count", "avg_composite_risk", "risk_tier"]
    ].round(3)
    print(f"\n    Top 5 highest-risk students:")
    print(top5.to_string(index=False))

    return summary


def build_semester_trends(df):
    
    print("\n  Building semester trend summary...")

    trends = df.groupby("semester").agg(
        avg_grade       = ("grade",           "mean"),
        avg_ai_prob     = ("ai_probability",  "mean"),
        avg_drift       = ("style_drift",     "mean"),
        avg_risk        = ("composite_risk",  "mean"),
        anomaly_pct     = ("anomaly_flag",    lambda x: (x == -1).mean() * 100),
        total_anomalies = ("anomaly_flag",    lambda x: (x == -1).sum()),
        submission_count= ("submission_id",   "count"),
    ).reset_index().round(3)

    print(f"    Semester trends computed:")
    print(trends[["semester", "avg_grade", "avg_ai_prob",
                  "avg_drift", "anomaly_pct"]].to_string(index=False))

    return trends
