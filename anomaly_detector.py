import pandas as pd

def calculate_metrics(df, metrics, window=7):
    for m in metrics:
        df[f"{m}_Change"]=df[m].pct_change()*100
        df[f"{m}_Baseline"]=df[m].rolling(window).mean().shift(1)
        b=df[f"{m}_Baseline"]
        df[f"{m}_Deviation"]=((df[m]-b)/b)*100
        df[f"{m}_Anomaly"]=df[f"{m}_Deviation"].abs()>20
    return df

def detect_anomalies(df, metrics, threshold=20):
    latest=df.iloc[-1]; out=[]
    for m in metrics:
        d=latest[f"{m}_Deviation"]
        if pd.isna(d) or abs(d)<=threshold: continue
        severity="Critical" if abs(d)>=50 else ("High" if abs(d)>=30 else "Medium")
        out.append({"Metric":m,"Current Value":latest[m],"Baseline":latest[f"{m}_Baseline"],
                    "Deviation (%)":round(d,2),"Direction":"Increase" if d>0 else "Decrease",
                    "Severity":severity})
    return out
