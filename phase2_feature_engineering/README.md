# LABIA — Phase 2: Feature Engineering

**Longitudinal Academic Behaviour & Integrity Analysis**
School of Computer Science, UPES Dehradun

---

## What this phase does

Phase 2 takes the clean merged dataset from Phase 1 and engineers all the analytical features that power the integrity detection system. It runs 4 feature computation steps and produces a per-student risk summary.

| Step | What it computes | New columns |
|------|-----------------|-------------|
| 1 | Z-score standardise writing features | `sl_z`, `rs_z`, `vr_z` |
| 2 | Writing style drift (cosine similarity) | `style_drift` |
| 3 | Grade trend features | `grade_delta`, `grade_rolling_std` |
| 4 | Composite integrity risk score | `risk_ai`, `risk_similarity`, `risk_drift`, `risk_delay`, `composite_risk` |

---

## Folder structure

```
phase2_feature_engineering/
├── data/
│   ├── input/                     ← place master_raw.csv here (from Phase 1)
│   └── output/                    ← output files appear here after running
│       ├── master_features.csv    (30,000 rows with all engineered features)
│       └── student_summary.csv    (500 rows, one per student with risk tier)
├── writing_features.py            ← standardisation + style drift
├── performance_features.py        ← grade delta + rolling std
├── risk_score.py                  ← composite risk score
├── student_summary.py             ← per-student aggregation + risk tiering
├── run_feature_engineering.py     ← run this file
├── requirements.txt
└── README.md
```

---

## Input required

Copy `master_raw.csv` (output from Phase 1) into `data/input/`.

---

## How to run

### Step 1 — Set up virtual environment

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Place the input file

Copy `master_raw.csv` from Phase 1 into `data/input/`.

### Step 3 — Run the pipeline

```
python run_feature_engineering.py
```

### Expected output

```
==================================================
  LABIA — Phase 2: Feature Engineering
==================================================

Step 1/5  Loading Phase 1 output...
  Loaded master_raw.csv | 30,000 rows x 14 columns

Step 2/5  Writing style features...
  Standardising writing features (Z-score)...
    avg_sentence_length → sl_z
    readability_score   → rs_z
    vocab_richness      → vr_z

Step 3/5  Writing style drift...
  (~30 seconds for 30,000 rows)
    Done | avg drift = 0.580 | max drift = 1.999

Step 4/5  Performance trend features...
    grade_delta       | avg change = +0.001
    grade_rolling_std | avg = 5.423

Step 5/5  Composite risk scores...
    composite_risk | avg = 0.260 | max = 0.770

Building student summary...
    500 students summarised
    Risk tier distribution:
      Low       : 100 students (20.0%)
      Medium    : 382 students (76.4%)
      High      :  18 students (3.6%)
      Critical  :   0 students (0.0%)

Phase 2 complete!
==================================================
```

---

## Feature explanations

### Writing style drift

Measures how much a student's writing changed between consecutive submissions using **cosine similarity** on standardised NLP vectors:

```
drift = 1 − cosine_similarity(previous_submission_vector, current_submission_vector)
```

| Drift value | Meaning |
|------------|---------|
| 0.0 – 0.3 | Normal variation |
| 0.3 – 0.8 | Noticeable change |
| 0.8 – 1.5 | Significant shift |
| 1.5 – 2.0 | Near-complete style reversal — strong integrity flag |

### Composite risk score

Weighted combination of 4 normalised signals:

| Signal | Weight | Why |
|--------|--------|-----|
| AI probability | 35% | Most direct integrity signal |
| Similarity score | 25% | Plagiarism / shared content |
| Style drift | 25% | Writing fingerprint change |
| Submission delay | 15% | Behavioural pattern shift |

### Risk tiers

| Tier | Risk score range | Action |
|------|-----------------|--------|
| Low | < 0.20 | No action |
| Medium | 0.20 – 0.40 | Monitor |
| High | 0.40 – 0.60 | Manual review recommended |
| Critical | > 0.60 | Immediate escalation |

---

## Tech stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | Core language |
| pandas | 2.2.2 | DataFrame operations |
| NumPy | 1.26.4 | Vector math |
| scikit-learn | 1.4.2 | StandardScaler, cosine_similarity |

---

## Project phases

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 — Data Collection | ✅ Complete | Load, merge, validate 6 datasets |
| **Phase 2 — Feature Engineering** | ✅ Complete | NLP features, style drift, risk scores |
| Phase 3 — Analytics | 🔄 Next | Anomaly detection, risk tiering |
| Phase 4 — Dashboard | ⏳ Upcoming | Streamlit interactive dashboard |
