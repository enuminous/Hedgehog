import json
import pandas as pd
from hedgehog import HEDGEHOGExperiment

df=pd.read_csv("example_data.csv")
envs=pd.read_csv("example_environments.csv")

exp=HEDGEHOGExperiment(
    environment_column="environment_id",
    target_column="future_event",
    feature_columns=["signal_a","signal_b","signal_c"],
    development_environments=["DEV-A","DEV-B","DEV-C"],
    heldout_environments=["HOLD-LOW","HOLD-MID","HOLD-HABITAT","HOLD-NOISE"],
    horizons=(3,7,23),
    random_state=23,
    material_gain=0.002,
)

print(json.dumps(exp.run(df,envs),indent=2))
