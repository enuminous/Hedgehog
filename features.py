import numpy as np
import pandas as pd

def raw_features(df, feature_columns):
    return df[feature_columns].astype(float).ffill().fillna(0.0)

def candidate_features(df, feature_columns, horizons=(3,7,23)):
    x=raw_features(df,feature_columns)
    out=pd.DataFrame(index=df.index)

    dx=x.diff().fillna(0.0)
    out["state_disagreement"]=x.std(axis=1).fillna(0.0)
    out["signed_change"]=dx.mean(axis=1)
    out["change_disagreement"]=dx.std(axis=1).fillna(0.0)
    out["state_velocity"]=out["state_disagreement"].diff().fillna(0.0)

    # Relational precursor: divergence between channels rather than magnitude alone.
    centered=x.sub(x.mean(axis=1),axis=0)
    out["relational_energy"]=(centered**2).mean(axis=1)

    for h in horizons:
        out[f"disagreement_mean_{h}"]=out["state_disagreement"].rolling(h,min_periods=1).mean()
        out[f"relational_mean_{h}"]=out["relational_energy"].rolling(h,min_periods=1).mean()
        out[f"signed_mean_{h}"]=out["signed_change"].rolling(h,min_periods=1).mean()

    # Small recursive persistence state.
    base=(
        out["state_disagreement"].rank(pct=True)
        +out["change_disagreement"].rank(pct=True)
        +out["relational_energy"].rank(pct=True)
    )/3.0
    rec=np.zeros(len(out))
    for i,v in enumerate(base.to_numpy()):
        prev=rec[i-1] if i else 0.0
        rec[i]=0.65*prev+0.35*np.tanh(float(v)+prev)
    out["recursive_persistence"]=rec

    return out.replace([np.inf,-np.inf],np.nan).fillna(0.0)

def structured_complexity(env):
    dims=[
        "temporal_depth",
        "partial_observability",
        "feedback",
        "contradiction",
        "distributed_state",
    ]
    return float(np.mean([float(env[d]) for d in dims]))
