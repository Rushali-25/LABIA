"""
performance_features.py
------------------------
FEATURE ENGINEERING — Step 2: Performance Trend Features

What this file does:
  For each student (in submission time order), computes:
    grade_delta       : how much the grade changed from the previous submission
                        positive = improved, negative = dropped
    grade_rolling_std : rolling standard deviation over the last 3 submissions
                        high value = erratic/inconsistent grades
                        low value  = stable performance

Columns added:
  grade_delta       : grade change from previous submission (NaN for first)
  grade_rolling_std : 3-submission rolling standard deviation (NaN until 2+ submissions)
"""

import pandas as pd


def compute_performance_trends(df):
    """
    Compute grade delta and rolling standard deviation per student.
    """
    print("  Computing performance trend features...")

    df = df.copy()
    delta_series = pd.Series(index=df.index, dtype=float)
    std_series   = pd.Series(index=df.index, dtype=float)

    for student_id, group in df.groupby("student_id"):
        # Grade change between consecutive submissions
        delta_series[group.index] = group["grade"].diff().values

        # Rolling std over last 3 submissions (measures consistency)
        std_series[group.index] = (
            group["grade"].rolling(window=3, min_periods=2).std().values
        )

    df["grade_delta"]       = delta_series
    df["grade_rolling_std"] = std_series

    avg_delta = df["grade_delta"].dropna().mean()
    avg_std   = df["grade_rolling_std"].dropna().mean()

    print(f"    grade_delta       | avg change = {avg_delta:+.3f} (near 0 = stable grades)")
    print(f"    grade_rolling_std | avg = {avg_std:.3f}  (lower = more consistent)")

    return df
