import streamlit as st
import pandas as pd
from pathlib import Path
from anomaly_detector import calculate_metrics,detect_anomalies
from business_insights import generate_business_insights

st.set_page_config(page_title="InsightGuard",page_icon="🛡️",layout="wide")
BASE_DIR=Path(__file__).resolve().parent.parent
DATA_FILE=BASE_DIR/"data"/"business_data.xlsx"
HISTORY=BASE_DIR/"output"/"alert_history.csv"
METRICS=["Revenue","Orders","Traffic","Conversion","Cost","Refunds"]

st.title("🛡️ InsightGuard")
st.caption("Automated Business Analytics & Anomaly Monitoring")

df=pd.read_excel(DATA_FILE)
df["Date"]=pd.to_datetime(df["Date"],errors="coerce")
df=df.dropna(subset=["Date"]).drop_duplicates().sort_values("Date").reset_index(drop=True)

threshold=st.sidebar.slider("Anomaly Threshold (%)",5,50,20,5)
min_d,max_d=df["Date"].min().date(),df["Date"].max().date()
date_range=st.sidebar.date_input("Date Range",(min_d,max_d),min_value=min_d,max_value=max_d)
start,end=(date_range if isinstance(date_range,tuple) and len(date_range)==2 else (date_range,date_range))
filtered=df[(df["Date"].dt.date>=start)&(df["Date"].dt.date<=end)]

analysis=calculate_metrics(df.copy(),METRICS)
latest=analysis.iloc[-1]
anomalies=detect_anomalies(analysis,METRICS,threshold)
insights=generate_business_insights(latest,threshold)

st.subheader("📊 Latest Business Performance")
cols=st.columns(6)
vals=[("Revenue",f"₹{latest.Revenue:,.0f}"),("Orders",f"{latest.Orders:,.0f}"),("Traffic",f"{latest.Traffic:,.0f}"),
      ("Conversion",f"{latest.Conversion:.2f}%"),("Cost",f"₹{latest.Cost:,.0f}"),("Refunds",f"{latest.Refunds:,.0f}")]
for c,(n,v) in zip(cols,vals): c.metric(n,v)

st.divider(); st.subheader("🚨 Anomaly Monitoring")
if anomalies:
    adf=pd.DataFrame(anomalies); st.error(f"{len(anomalies)} anomaly/anomalies detected.")
    st.dataframe(adf,width="stretch",hide_index=True)
    st.download_button("⬇️ Download Anomaly Report",adf.to_csv(index=False),"insightguard_anomaly_report.csv","text/csv")
else: st.success("No significant anomalies detected.")

st.divider(); st.subheader("📈 Business Trends")
metric=st.selectbox("Choose a metric",METRICS)
st.line_chart(filtered[["Date",metric]].set_index("Date"))

st.subheader("💰 Revenue Trend")
st.area_chart(filtered[["Date","Revenue"]].set_index("Date"))

st.subheader("🛒 Orders & Traffic")
st.line_chart(filtered[["Date","Orders","Traffic"]].set_index("Date"))

st.divider(); st.subheader("🧠 Business Intelligence")
for x in insights: st.warning(x)
if not insights: st.success("No major business issues detected.")

st.divider(); st.subheader("📜 Alert History")
if HISTORY.exists():
    h=pd.read_csv(HISTORY)
    st.dataframe(h.sort_values("Date",ascending=False),width="stretch",hide_index=True)
else: st.info("No alert history available yet.")

with st.expander("🔍 View Business Data"):
    st.dataframe(filtered,width="stretch",hide_index=True)

st.caption("InsightGuard | Automated Business Analytics & Anomaly Monitoring System")
