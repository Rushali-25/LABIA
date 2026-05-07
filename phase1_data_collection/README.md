
# LABIA — Phase 1: Data Collection & Ingestion

**Longitudinal Academic Behaviour & Integrity Analysis**
School of Computer Science, UPES Dehradun

---

## What this phase does

Phase 1 is the data foundation of the LABIA project. It:

- Loads **6 structured CSV datasets** covering 500 students, 20 courses, and 30,000 academic submissions across 4 semesters
- Merges all 6 files into a single clean master table using submission ID, course ID, and semester as join keys
- Validates the merged data (null check, duplicate check, student count, semester range)
- Prints a full statistical summary of the dataset
- Saves the output to `data/output/master_raw.csv` ready for Phase 2

---

## Folder structure

```
phase1_data_collection/
├── data/
│   ├── raw/                  ← place your 6 CSV files here
│   └── output/               ← master_raw.csv appears here after running
├── loader.py                 ← all loading, merging, validation logic
├── run_data_collection.py    ← run this file
├── requirements.txt
└── README.md
```

---

## Datasets used

| File | Rows | Description |
|------|------|-------------|
| `students.csv` | 500 | Student profiles: GPA, English proficiency, integrity risk baseline |
| `courses.csv` | 20 | Course metadata: semester, difficulty level |
| `submissions.csv` | 30,000 | Core records: AI probability, similarity score, submission time |
| `writing_features.csv` | 30,000 | NLP features: sentence length, readability, vocabulary richness |
| `performance_metrics.csv` | 30,000 | Grade per submission |
| `behavior_metrics.csv` | 30,000 | Submission delay (hours), revision count |

---

## How to run

### Step 1 — Set up virtual environment

Open the VS Code terminal (`Ctrl + backtick`) and run:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Place your CSV files

Copy all 6 CSV files into the `data/raw/` folder.

### Step 3 — Run the pipeline

```
python run_data_collection.py
```

### Expected output

```
==================================================
  LABIA — Phase 1: Data Collection
==================================================

  Step 1: Loading CSV files
  students.csv            :    500 rows
  courses.csv             :     20 rows
  submissions.csv         : 30,000 rows
  writing_features.csv    : 30,000 rows
  performance_metrics.csv : 30,000 rows
  behavior_metrics.csv    : 30,000 rows

  Step 2: Merging datasets
  Merged table shape : 30,000 rows x 14 columns

  Step 3: Validating merged data
  [PASS] No null values found
  [PASS] Student count correct (500 students)
  [PASS] No duplicate submission IDs
  [PASS] Semesters correct: [1, 2, 3, 4]
  [PASS] Each student has exactly 60 submissions

  All checks passed!

  Output saved to: data/output/master_raw.csv
  Phase 1 complete!
==================================================
```

---

## Output

`data/output/master_raw.csv` — 30,000 rows × 14 columns

This file is the input for **Phase 2: Feature Engineering**.

---

## Tech stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | Core language |
| pandas | 2.2.2 | Data loading and merging |
| NumPy | 1.26.4 | Numerical support |

---

## Project phases

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1 — Data Collection** | ✅ Complete | Load, merge, validate 6 datasets |
| Phase 2 — Feature Engineering | 🔄 Next | NLP features, style drift, risk scores |
| Phase 3 — Analytics | ⏳ Upcoming | Anomaly detection, risk tiering |
| Phase 4 — Dashboard | ⏳ Upcoming | Streamlit interactive dashboard |
>>>>>>> 3a56d2b (Phase 1: data collection and ingestion complete)
