import pandas as pd

def _minmax_normalise(series):
    mn = series.min()
    mx = series.max()
    if (mx - mn) < 1e-9:
        return pd.Series(0.0, index=series.index)
    return (series - mn) / (mx - mn)


def compute_composite_risk(df):
    print("  Computing composite risk scores...")

    df = df.copy()

    
    df["risk_ai"]         = _minmax_normalise(df["ai_probability"])
    df["risk_similarity"] = _minmax_normalise(df["similarity_score"])
    df["risk_drift"]      = _minmax_normalise(df["style_drift"].fillna(0))
    df["risk_delay"]      = _minmax_normalise(df["submission_delay_hours"].clip(lower=0))

    
    df["composite_risk"] = (
        0.35 * df["risk_ai"] +
        0.25 * df["risk_similarity"] +
        0.25 * df["risk_drift"] +
        0.15 * df["risk_delay"]
    )

    avg = df["composite_risk"].mean()
    mx  = df["composite_risk"].max()
    print(f"    composite_risk | avg = {avg:.3f} | max = {mx:.3f}")
    print(f"    Signal breakdown (avg normalised values):")
    print(f"      risk_ai         = {df['risk_ai'].mean():.3f}  (35% weight)")
    print(f"      risk_similarity = {df['risk_similarity'].mean():.3f}  (25% weight)")
    print(f"      risk_drift      = {df['risk_drift'].mean():.3f}  (25% weight)")
    print(f"      risk_delay      = {df['risk_delay'].mean():.3f}  (15% weight)")

    return df
