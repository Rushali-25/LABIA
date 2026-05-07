"""

Loads all 6 raw CSV files and merges them into
one clean master DataFrame.

"""

import pandas as pd
from pathlib import Path


def load_all_datasets(data_dir=None):
    
    if data_dir is None:
       
        data_dir = Path(__file__).parent / "data" / "raw"
    else:
        data_dir = Path(data_dir)

    print("=" * 50)
    print("  Step 1: Loading CSV files")
    print("=" * 50)

    students    = pd.read_csv(data_dir / "students.csv")
    courses     = pd.read_csv(data_dir / "courses.csv")
    submissions = pd.read_csv(data_dir / "submissions.csv",
                               parse_dates=["submission_time"])
    writing     = pd.read_csv(data_dir / "writing_features.csv")
    performance = pd.read_csv(data_dir / "performance_metrics.csv")
    behavior    = pd.read_csv(data_dir / "behavior_metrics.csv")

    print(f"  students.csv            : {len(students):>6,} rows")
    print(f"  courses.csv             : {len(courses):>6,} rows")
    print(f"  submissions.csv         : {len(submissions):>6,} rows")
    print(f"  writing_features.csv    : {len(writing):>6,} rows")
    print(f"  performance_metrics.csv : {len(performance):>6,} rows")
    print(f"  behavior_metrics.csv    : {len(behavior):>6,} rows")

    return students, courses, submissions, writing, performance, behavior


def merge_datasets(students, courses, submissions, writing, performance, behavior):
    
    print("\n" + "=" * 50)
    print("  Step 2: Merging datasets")
    print("=" * 50)

    master = (
        submissions
        .merge(writing,     on="submission_id",         how="left")
        .merge(performance,  on="submission_id",         how="left")
        .merge(behavior,     on="submission_id",         how="left")
        .merge(courses,      on=["course_id", "semester"], how="left")
        .sort_values(["student_id", "submission_time"])
        .reset_index(drop=True)
    )

    print(f"  Merged table shape : {master.shape[0]:,} rows x {master.shape[1]} columns")
    print(f"  Columns            : {list(master.columns)}")

    return master


def validate(master, students):

    print("\n" + "=" * 50)
    print("  Step 3: Validating merged data")
    print("=" * 50)

    all_passed = True

    
    null_count = master.isnull().sum().sum()
    if null_count == 0:
        print("  [PASS] No null values found")
    else:
        print(f"  [FAIL] {null_count} null values found — check merge keys")
        all_passed = False

    
    expected = len(students)
    actual   = master["student_id"].nunique()
    if actual == expected:
        print(f"  [PASS] Student count correct ({actual} students)")
    else:
        print(f"  [FAIL] Student count mismatch: expected {expected}, got {actual}")
        all_passed = False

    
    dupes = master["submission_id"].duplicated().sum()
    if dupes == 0:
        print("  [PASS] No duplicate submission IDs")
    else:
        print(f"  [FAIL] {dupes} duplicate submission IDs found")
        all_passed = False

    
    semesters = sorted(master["semester"].unique().tolist())
    if semesters == [1, 2, 3, 4]:
        print(f"  [PASS] Semesters correct: {semesters}")
    else:
        print(f"  [WARN] Unexpected semesters: {semesters}")

    
    counts = master.groupby("student_id").size()
    if counts.min() == counts.max():
        print(f"  [PASS] Each student has exactly {counts.min()} submissions")
    else:
        print(f"  [WARN] Unequal submission counts: min={counts.min()}, max={counts.max()}")

    if not all_passed:
        raise ValueError("\nValidation failed. Fix the issues above before continuing.")

    print("\n  All checks passed!")
    

def show_summary(master, students):
    
    print("\n" + "=" * 50)
    print("  Dataset Summary")
    print("=" * 50)
    print(f"  Total submissions  : {len(master):,}")
    print(f"  Total students     : {master['student_id'].nunique()}")
    print(f"  Total courses      : {master['course_id'].nunique()}")
    print(f"  Semesters          : {sorted(master['semester'].unique().tolist())}")
    print(f"\n  Grade range        : {master['grade'].min():.1f} – {master['grade'].max():.1f}")
    print(f"  Avg grade          : {master['grade'].mean():.2f}")
    print(f"\n  AI probability range: {master['ai_probability'].min():.3f} – {master['ai_probability'].max():.3f}")
    print(f"  Avg AI probability  : {master['ai_probability'].mean():.3f}")
    print(f"\n  Similarity score range: {master['similarity_score'].min():.3f} – {master['similarity_score'].max():.3f}")
    print(f"\n  Submission delay range: {master['submission_delay_hours'].min()} – {master['submission_delay_hours'].max()} hours")
    print(f"\n  Student GPA range  : {students['prior_gpa'].min():.2f} – {students['prior_gpa'].max():.2f}")
    print("=" * 50)
