
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


def standardise_writing_features(df):
   
    print("  Standardising writing features (Z-score)...")

    scaler = StandardScaler()
    df = df.copy()

    df[["sl_z", "rs_z", "vr_z"]] = scaler.fit_transform(
        df[["avg_sentence_length", "readability_score", "vocab_richness"]]
    )

    print(f"    avg_sentence_length → sl_z  | mean={df['sl_z'].mean():.3f}, std={df['sl_z'].std():.3f}")
    print(f"    readability_score   → rs_z  | mean={df['rs_z'].mean():.3f}, std={df['rs_z'].std():.3f}")
    print(f"    vocab_richness      → vr_z  | mean={df['vr_z'].mean():.3f}, std={df['vr_z'].std():.3f}")

    return df


def compute_style_drift(df):
    
    print("  Computing writing style drift per student...")
    print("  (loops through 500 students × 60 submissions each)")

    df = df.copy()
    drift_values = pd.Series(index=df.index, dtype=float)

    for student_id, group in df.groupby("student_id"):
        vectors = group[["sl_z", "rs_z", "vr_z"]].values
        drifts  = [np.nan]   # first submission: no previous to compare

        for i in range(1, len(vectors)):
            prev = vectors[i - 1].reshape(1, -1)
            curr = vectors[i].reshape(1, -1)
            sim  = cosine_similarity(prev, curr)[0][0]
            drifts.append(1.0 - sim)

        drift_values[group.index] = drifts

    df["style_drift"] = drift_values

    valid_drifts = df["style_drift"].dropna()
    print(f"    Done | avg drift = {valid_drifts.mean():.3f} | max drift = {valid_drifts.max():.3f}")
    print(f"    Interpretation: avg drift of {valid_drifts.mean():.3f} = normal baseline for this cohort")

    return df
