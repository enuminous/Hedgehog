import numpy as np
from sklearn.metrics import brier_score_loss, roc_auc_score, average_precision_score, log_loss

def binary_metrics(y,p):
    y=np.asarray(y,dtype=int)
    p=np.clip(np.asarray(p,dtype=float),1e-9,1-1e-9)
    out={
        "brier":float(brier_score_loss(y,p)),
        "log_loss":float(log_loss(y,np.c_[1-p,p],labels=[0,1])),
    }
    if len(np.unique(y))>1:
        out["roc_auc"]=float(roc_auc_score(y,p))
        out["average_precision"]=float(average_precision_score(y,p))
    else:
        out["roc_auc"]=None
        out["average_precision"]=None
    return out

def safe_corr(a,b):
    a=np.asarray(a,dtype=float)
    b=np.asarray(b,dtype=float)
    if len(a)<2 or np.std(a)<1e-12 or np.std(b)<1e-12:
        return None
    return float(np.corrcoef(a,b)[0,1])
