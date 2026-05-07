"""

PHASE 1 — Data Collection & Ingestion

"""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

from loader import (
    load_all_datasets,
    merge_datasets,
    validate,
    show_summary,
)


def main():
    print("\n")
    print("=" * 50)
    print("  LABIA — Phase 1: Data Collection")
    print("=" * 50)

  
    students, courses, submissions, writing, performance, behavior = load_all_datasets()

    master = merge_datasets(students, courses, submissions, writing, performance, behavior)

    validate(master, students)

    show_summary(master, students)

    out_dir = Path(__file__).parent / "data" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "master_raw.csv"
    master.to_csv(out_path, index=False)

    print(f"\n  Output saved to: data/output/master_raw.csv")
    print(f"  Shape: {master.shape[0]:,} rows x {master.shape[1]} columns")
    print("=" * 50)


if __name__ == "__main__":
    main()
