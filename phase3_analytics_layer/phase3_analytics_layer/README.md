# LABIA — Phase 3: Analytics Layer

**Longitudinal Academic Behaviour & Integrity Analysis**
School of Computer Science, UPES Dehradun

---

## What this phase does

Phase 3 takes the feature-engineered dataset from Phase 2 and applies machine learning to detect anomalous submissions and produce a final risk profile for every student.

| Step | What it does | Output |
|------|-------------|--------|
| 1 | Isolation Forest anomaly detection | `anomaly_flag`, `anomaly_score` per submission |
| 2 | Student-level aggregation | One summary row per student |
| 3 | Risk tier assignment | Low / Medium / High / Critical |
| 4 | Semester trend summary | 4-row trend table |
| 5 | Chart generation | 4 PNG analysis charts |

---

## Folder structure

```
phase3_analytics_layer/
├── data/
│   ├── input/                      ← place master_features.csv here (from Phase 2)
│   └── output/                     ← output files appear here after running
│       ├── master_analytics.csv    (30,000 rows with anomaly flags)
│       ├── student_summary.csv     (500 rows, one per student)
│       ├── semester_trends.csv     (4 rows, one per semester)
│       └── charts/
│           ├── semester_trends.png
│           ├── risk_tier_distribution.png
│           ├── ai_probability_histogram.png
│           └── drift_distribution.png
├── anomaly_detection.py            ← Isolation Forest model
├── student_aggregation.py          ← per-student summary + risk tiering
├── visualisations.py               ← 4 analysis charts
├── run_analytics.py                ← run this file
├── requirements.txt
└── README.md
```

---

## Input required

Copy `master_features.csv` (output from Phase 2) into `data/input/`.

---

## How to run

### Step 1 — Set up virtual environment
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Place the input file
Copy `master_features.csv` from Phase 2 into `data/input/`.

### Step 3 — Run the pipeline
```
python run_analytics.py
```

### Expected output

```
===========================================================
  LABIA — Phase 3: Analytics Layer
===========================================================

Step 1/4  Loading Phase 2 output...
  Loaded master_features.csv | 30,000 rows x 25 columns

Step 2/4  Anomaly detection (Isolation Forest)...
  Running Isolation Forest...
    Features   : 8 features
    Estimators : 200 trees
    Contamination : 5%
    Results:
    Total submissions   : 30,000
    Flagged as anomaly  : 1,500 (5.0%)
    Avg score (normal)  : 0.380
    Avg score (anomaly) : 0.520

Step 3/4  Student aggregation & risk tiering...
    500 students aggregated
    Risk tier distribution:
      Low        : 100 students (20.0%)  ██████████
      Medium     : 382 students (76.4%)  ██████████████████████████████████████
      High       :  18 students ( 3.6%)  █
      Critical   :   0 students ( 0.0%)

Step 4/4  Generating charts...
  All 4 charts saved to data/output/charts/

===========================================================
  Phase 3 complete!
===========================================================
```

---

## How Isolation Forest works

```
Normal submission  → similar to many others → needs many splits to isolate → long path length → low anomaly score
Anomalous submission → rare and different → isolated in few splits → short path length → HIGH anomaly score
```

The model uses **8 features** simultaneously — no single signal triggers a flag. A submission must be unusual across multiple dimensions to be flagged.

---

## Results from your dataset

| Metric | Value |
|--------|-------|
| Total submissions | 30,000 |
| Anomalies flagged | 1,500 (5.0%) |
| Semester 1 anomaly rate | 3.44% |
| Semester 4 anomaly rate | 7.31% |
| High-risk students | 18 (3.6%) |
| Top risk student | S0251 (AI prob 34.7%, max drift 1.956) |

---

## Tech stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | Core language |
| pandas | 2.2.2 | Data manipulation |
| NumPy | 1.26.4 | Numerical operations |
| scikit-learn | 1.4.2 | Isolation Forest, StandardScaler |
| matplotlib | 3.9.0 | Chart generation |
| seaborn | 0.13.2 | Chart styling |

---

## Project phases

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 — Data Collection | ✅ Complete | Load, merge, validate 6 datasets |
| Phase 2 — Feature Engineering | ✅ Complete | Style drift, risk scores |
| **Phase 3 — Analytics** | ✅ Complete | Anomaly detection, risk tiering, charts |
| Phase 4 — Dashboard | 🔄 Next | Streamlit interactive dashboard |
