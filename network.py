#!/usr/bin/env python3
# DESC: Test network connectivity and report upload/download speed (compact by default)
# TAG: network, internet, speedtest, connectivity, diagnostics
# ARG: [--expand] - Show detailed results instead of summary
# EXAMPLE: jynetcheck --expand

import os
import subprocess
import socket
import speedtest
import sys


def check_connectivity(host="8.8.8.8", port=53, timeout=3):
    """Check if internet connection is available."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def ping_test(target="8.8.8.8", count=4):
    """Ping a host and return average latency (ms)."""
    try:
        output = subprocess.check_output(
            ["ping", "-c", str(count), target],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for line in output.splitlines():
            if "avg" in line or "rtt" in line:
                avg_line = line
                break
        else:
            avg_line = ""
        # Extract numeric average ping
        avg_ping = None
        if "=" in avg_line:
            parts = avg_line.split("=")[1].split("/")
            avg_ping = float(parts[1]) if len(parts) > 1 else None
        return avg_ping, output
    except subprocess.CalledProcessError:
        return None, None


def speed_test():
    """Run download/upload speed test and return Mbps + ping (ms)."""
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Mbps
    upload_speed = st.upload() / 1_000_000
    ping_ms = st.results.ping
    return download_speed, upload_speed, ping_ms


def main():
    expand = "--expand" in sys.argv
    connected = check_connectivity()

    if not connected:
        if expand:
            print("❌ No internet connection detected.")
        else:
            print("❌ Disconnected")
        sys.exit(1)

    avg_ping, ping_output = ping_test()
    download, upload, ping_ms = 0, 0, avg_ping or 0

    try:
        download, upload, ping_ms = speed_test()
    except Exception:
        if expand:
            print("⚠️  Speed test failed, showing ping only.")

    if expand:
        os.system("clear")
        print("=== 🌐 Network Diagnostic (jynetcheck) ===\n")
        print("✅ Internet connection detected.\n")
        if ping_output:
            print("📡 Ping Results:\n")
            print(ping_output)
        print("📊 Speed Test Results:")
        print(f"   ⚡ Download: {download:.2f} Mbps")
        print(f"   📤 Upload:   {upload:.2f} Mbps")
        print(f"   🕒 Ping:     {ping_ms:.2f} ms\n")
    else:
        print(f"✅ Connected | ↓ {download:.2f} Mbps ↑ {upload:.2f} Mbps | Ping {ping_ms:.0f} ms")


if __name__ == "__main__":
    main()

