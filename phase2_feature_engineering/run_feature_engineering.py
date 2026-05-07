import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd

from writing_features     import standardise_writing_features, compute_style_drift
from performance_features import compute_performance_trends
from risk_score           import compute_composite_risk
from student_summary      import build_student_summary


def load_input():
    input_path = Path(__file__).parent / "data" / "input" / "master_raw.csv"

    if not input_path.exists():
        print("\n  ERROR: master_raw.csv not found.")
        print(f"  Expected at: {input_path}")
        print("  Please run Phase 1 first and copy master_raw.csv into data/input/")
        sys.exit(1)

    df = pd.read_csv(input_path, parse_dates=["submission_time"])
    print(f"  Loaded master_raw.csv | {len(df):,} rows x {df.shape[1]} columns")
    return df


def main():
    print("\n")
    print("=" * 55)
    print("  LABIA — Phase 2: Feature Engineering")
    print("=" * 55)

    
    print("\nStep 1/5  Loading Phase 1 output...")
    df = load_input()

   
    print("\nStep 2/5  Writing style features...")
    df = standardise_writing_features(df)

   
    print("\nStep 3/5  Writing style drift...")
    print("          (~30 seconds for 30,000 rows)")
    df = compute_style_drift(df)

    
    print("\nStep 4/5  Performance trend features...")
    df = compute_performance_trends(df)

    
    print("\nStep 5/5  Composite risk scores...")
    df = compute_composite_risk(df)

    
    print("\nBuilding student summary...")
    summary = build_student_summary(df)

   
    out_dir = Path(__file__).parent / "data" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    features_path = out_dir / "master_features.csv"
    summary_path  = out_dir / "student_summary.csv"

    df.to_csv(features_path, index=False)
    summary.to_csv(summary_path, index=False)

   
    print("\n" + "=" * 55)
    print("  Phase 2 complete! Output files:")
    print(f"  master_features.csv  → {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"  student_summary.csv  → {len(summary)} students")
    print("\n  New columns added in this phase:")
    new_cols = ["sl_z","rs_z","vr_z","style_drift",
                "grade_delta","grade_rolling_std",
                "risk_ai","risk_similarity","risk_drift",
                "risk_delay","composite_risk"]
    for col in new_cols:
        if col in df.columns:
            non_null = df[col].notna().sum()
            print(f"    {col:<22} | {non_null:>6,} non-null values")
    print("\n  Top 5 highest-risk students:")
    top5 = summary.nlargest(5, "avg_composite_risk")[
        ["student_id","avg_grade","avg_ai_prob","max_drift","avg_composite_risk","risk_tier"]
    ].round(3)
    print(top5.to_string(index=False))



if __name__ == "__main__":
    main()
