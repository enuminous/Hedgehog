from dataclasses import dataclass
import numpy as np
import pandas as pd

from features import raw_features, candidate_features, structured_complexity
from models import LogisticModel
from metrics import binary_metrics, safe_corr

@dataclass
class HEDGEHOGExperiment:
    environment_column: str
    target_column: str
    feature_columns: list
    development_environments: list
    heldout_environments: list
    horizons: tuple=(3,7,23)
    random_state: int=23
    material_gain: float=0.002

    def run(self,df,environments):
        df=df.copy().reset_index(drop=True)
        env_meta=environments.set_index("environment_id").to_dict("index")

        missing=set(self.development_environments+self.heldout_environments)-set(env_meta)
        if missing:
            raise ValueError(f"missing environment metadata: {sorted(missing)}")

        raw=raw_features(df,self.feature_columns)
        cand=candidate_features(df,self.feature_columns,self.horizons)
        augmented=pd.concat([raw,cand],axis=1)

        dev_mask=df[self.environment_column].isin(self.development_environments).to_numpy()
        y=df[self.target_column].astype(int).to_numpy()

        baseline=LogisticModel(self.random_state).fit(raw.loc[dev_mask],y[dev_mask])
        candidate=LogisticModel(self.random_state).fit(augmented.loc[dev_mask],y[dev_mask])

        p_base_all=baseline.predict_proba(raw)
        p_cand_all=candidate.predict_proba(augmented)

        development={
            "baseline":binary_metrics(y[dev_mask],p_base_all[dev_mask]),
            "candidate":binary_metrics(y[dev_mask],p_cand_all[dev_mask]),
        }
        development["delta_brier"]=development["baseline"]["brier"]-development["candidate"]["brier"]

        heldout={}
        gains=[]
        complexities=[]
        noises=[]

        for env_id in self.heldout_environments:
            mask=(df[self.environment_column]==env_id).to_numpy()
            if not mask.any():
                continue
            bm=binary_metrics(y[mask],p_base_all[mask])
            cm=binary_metrics(y[mask],p_cand_all[mask])
            gain=bm["brier"]-cm["brier"]
            meta=env_meta[env_id]
            complexity=structured_complexity(meta)
            noise=float(meta["noise"])

            heldout[env_id]={
                "n":int(mask.sum()),
                "baseline":bm,
                "candidate":cm,
                "delta_brier":float(gain),
                "structured_complexity":complexity,
                "noise":noise,
                "habitat":{
                    k:float(meta[k]) for k in [
                        "temporal_depth","partial_observability","feedback",
                        "contradiction","distributed_state","noise"
                    ]
                }
            }
            gains.append(gain)
            complexities.append(complexity)
            noises.append(noise)

        if not gains:
            raise ValueError("no held-out observations")

        median_gain=float(np.median(gains))
        win_rate=float(np.mean(np.asarray(gains)>0))
        worst_gain=float(np.min(gains))
        complexity_corr=safe_corr(complexities,gains)
        noise_corr=safe_corr(noises,gains)
        transfer_degradation=float(development["delta_brier"]-median_gain)

        # A simple preregisterable habitat signature:
        # gain should rise with structured complexity, while excessive noise should hurt.
        habitat_support=(
            complexity_corr is not None and complexity_corr>0
            and noise_corr is not None and noise_corr<0
        )

        if median_gain >= self.material_gain and win_rate >= 0.60:
            verdict="GENERALIZES"
        elif median_gain > 0 and habitat_support:
            verdict="HABITAT-CONDITIONAL"
        elif median_gain > 0:
            verdict="WEAK / INCONCLUSIVE"
        else:
            verdict="DOES NOT GENERALIZE"

        return {
            "development_environments":self.development_environments,
            "heldout_environments":self.heldout_environments,
            "development":development,
            "heldout":heldout,
            "summary":{
                "median_heldout_delta_brier":median_gain,
                "heldout_win_rate":win_rate,
                "worst_environment_delta_brier":worst_gain,
                "structured_complexity_gain_correlation":complexity_corr,
                "noise_gain_correlation":noise_corr,
                "habitat_signature_supported":habitat_support,
                "transfer_degradation":transfer_degradation,
                "material_gain_threshold":self.material_gain,
                "verdict":verdict,
            },
            "interpretation":"Positive ΔBrier favors the candidate. Habitat relationships are meaningful only if dimensions and signs were frozen before held-out outcomes were inspected."
        }
