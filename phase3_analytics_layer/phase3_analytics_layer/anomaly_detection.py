import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


ANOMALY_FEATURES = [
    "avg_sentence_length",
    "readability_score",
    "vocab_richness",
    "grade",
    "submission_delay_hours",
    "revision_count",
    "ai_probability",
    "similarity_score",
]


def detect_anomalies(df, contamination=0.05):
    
    print("  Running Isolation Forest...")
    print(f"    Features   : {ANOMALY_FEATURES}")
    print(f"    Estimators : 200 trees")
    print(f"    Contamination : {contamination*100:.0f}%")
    print(f"    Random seed   : 42 (results reproducible)")

    df = df.copy()

    
    X = df[ANOMALY_FEATURES].fillna(df[ANOMALY_FEATURES].median())

    
    X_scaled = StandardScaler().fit_transform(X)

    
    model = IsolationForest(
        n_estimators=200,       
        contamination=contamination,
        random_state=42,        
        n_jobs=-1,              
    )

    df["anomaly_flag"]  = model.fit_predict(X_scaled)   
    df["anomaly_score"] = -model.score_samples(X_scaled) 

    total   = len(df)
    flagged = (df["anomaly_flag"] == -1).sum()
    avg_score_normal  = df.loc[df["anomaly_flag"] ==  1, "anomaly_score"].mean()
    avg_score_anomaly = df.loc[df["anomaly_flag"] == -1, "anomaly_score"].mean()

    print(f"\n    Results:")
    print(f"    Total submissions   : {total:,}")
    print(f"    Flagged as anomaly  : {flagged:,} ({flagged/total*100:.1f}%)")
    print(f"    Normal submissions  : {total-flagged:,}")
    print(f"    Avg score (normal)  : {avg_score_normal:.3f}")
    print(f"    Avg score (anomaly) : {avg_score_anomaly:.3f}")

    return df
