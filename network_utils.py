import subprocess
import re
import platform
import speedtest

def ping_test(host="8.8.8.8", count=5):
    # Detect OS → Windows uses -n, Linux/Mac uses -c
    param = "-n" if platform.system().lower() == "windows" else "-c"
    result = subprocess.run(["ping", param, str(count), host], capture_output=True, text=True)
    output = result.stdout

    # Extract latency values (handles Windows & Linux/Mac)
    times = re.findall(r'time[=<](\d+\.?\d*)', output)
    times = [float(t) for t in times]

    packet_loss = 100 - (len(times) / count * 100)
    avg_latency = sum(times) / len(times) if times else None

    return {"latency_ms": avg_latency, "packet_loss_%": packet_loss}

def bandwidth_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000  # Mbps
    upload = st.upload() / 1_000_000      # Mbps
    return {"download_mbps": download, "upload_mbps": upload}
