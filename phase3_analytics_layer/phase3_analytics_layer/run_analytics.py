import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd

from anomaly_detection    import detect_anomalies
from student_aggregation  import build_student_summary, build_semester_trends
from visualisations       import generate_all_charts


def load_input():
   
    input_path = Path(__file__).parent / "data" / "input" / "master_features.csv"

    if not input_path.exists():
        print("\n  ERROR: master_features.csv not found.")
        print(f"  Expected at: {input_path}")
        print("  Please run Phase 2 first and copy master_features.csv into data/input/")
        sys.exit(1)

    df = pd.read_csv(input_path, parse_dates=["submission_time"])
    print(f"  Loaded master_features.csv | {len(df):,} rows x {df.shape[1]} columns")
    return df


def main():
    print("\n")
    print("=" * 58)
    print("  LABIA — Phase 3: Analytics Layer")
    print("=" * 58)

   
    print("\nStep 1/4  Loading Phase 2 output...")
    df = load_input()

    
    print("\nStep 2/4  Anomaly detection (Isolation Forest)...")
    df = detect_anomalies(df, contamination=0.05)

    
    print("\nStep 3/4  Student aggregation & risk tiering...")
    summary = build_student_summary(df)
    trends  = build_semester_trends(df)

    
    print("\nStep 4/4  Generating charts...")
    out_dir = Path(__file__).parent / "data" / "output"
    generate_all_charts(df, summary, trends, str(out_dir))

   
    out_dir.mkdir(parents=True, exist_ok=True)

    analytics_path = out_dir / "master_analytics.csv"
    summary_path   = out_dir / "student_summary.csv"
    trends_path    = out_dir / "semester_trends.csv"

    df.to_csv(analytics_path, index=False)
    summary.to_csv(summary_path, index=False)
    trends.to_csv(trends_path, index=False)

  
    print("\n" + "=" * 58)
    print("  Phase 3 complete! Output files:")
    print(f"  master_analytics.csv → {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"  student_summary.csv  → {len(summary)} students with risk tiers")
    print(f"  semester_trends.csv  → {len(trends)} semester rows")
    print(f"  charts/              → 4 PNG chart files")

    print("\n  New columns added in this phase:")
    for col in ["anomaly_flag", "anomaly_score"]:
        non_null = df[col].notna().sum()
        print(f"    {col:<20} | {non_null:>6,} values")

    flagged = (df["anomaly_flag"] == -1).sum()
    print(f"\n  Anomaly summary:")
    print(f"    Total flagged    : {flagged:,} submissions ({flagged/len(df)*100:.1f}%)")
    print(f"    Normal           : {len(df)-flagged:,} submissions")

    
    print(f"\n  Anomaly rate by semester:")
    for _, row in trends.iterrows():
        print(f"    Semester {int(row['semester'])} : {row['anomaly_pct']:.2f}%  "
              f"({int(row['total_anomalies'])} flagged out of {int(row['submission_count'])})")

   


if __name__ == "__main__":
    main()
