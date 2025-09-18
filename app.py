import streamlit as st
import time
import pandas as pd
from datetime import datetime
from network_utils import ping_test, bandwidth_test

st.set_page_config(page_title="Network Performance Dashboard", layout="wide")
st.title("🌐 Network Performance Dashboard")
st.caption("Monitor latency, bandwidth, and packet loss in real-time.")

# Data storage
data = pd.DataFrame(columns=["time", "latency", "packet_loss", "download", "upload"])
placeholder = st.empty()

while True:
    metrics_ping = ping_test()
    metrics_bw = bandwidth_test()

    # Append new row
    new_row = pd.DataFrame([{
        "time": datetime.now().strftime("%H:%M:%S"),
        "latency": metrics_ping["latency_ms"],
        "packet_loss": metrics_ping["packet_loss_%"],
        "download": metrics_bw["download_mbps"],
        "upload": metrics_bw["upload_mbps"],
    }])
    data = pd.concat([data, new_row], ignore_index=True)

    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Latency (ms)", f"{metrics_ping['latency_ms']:.2f}")
        col2.metric("Packet Loss (%)", f"{metrics_ping['packet_loss_%']:.2f}")
        col3.metric("Download (Mbps)", f"{metrics_bw['download_mbps']:.2f}")
        col4.metric("Upload (Mbps)", f"{metrics_bw['upload_mbps']:.2f}")

        st.line_chart(data.set_index("time")[["latency"]])
        st.line_chart(data.set_index("time")[["packet_loss"]])
        st.line_chart(data.set_index("time")[["download", "upload"]])

    time.sleep(60)  # refresh every minute
