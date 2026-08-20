import pandas as pd
from hedgehog import HEDGEHOGExperiment
from features import structured_complexity

def make_exp():
    return HEDGEHOGExperiment(
        environment_column="environment_id",
        target_column="future_event",
        feature_columns=["signal_a","signal_b","signal_c"],
        development_environments=["DEV-A","DEV-B","DEV-C"],
        heldout_environments=["HOLD-LOW","HOLD-MID","HOLD-HABITAT","HOLD-NOISE"],
    )

def test_environment_complexity():
    envs=pd.read_csv("example_environments.csv")
    row=envs.iloc[0].to_dict()
    v=structured_complexity(row)
    assert 0 <= v <= 1

def test_all_heldout_environments_reported():
    df=pd.read_csv("example_data.csv")
    envs=pd.read_csv("example_environments.csv")
    out=make_exp().run(df,envs)
    assert set(out["heldout"])=={"HOLD-LOW","HOLD-MID","HOLD-HABITAT","HOLD-NOISE"}
    assert "median_heldout_delta_brier" in out["summary"]

def test_verdict_valid():
    df=pd.read_csv("example_data.csv")
    envs=pd.read_csv("example_environments.csv")
    out=make_exp().run(df,envs)
    assert out["summary"]["verdict"] in {
        "GENERALIZES","HABITAT-CONDITIONAL",
        "WEAK / INCONCLUSIVE","DOES NOT GENERALIZE"
    }
