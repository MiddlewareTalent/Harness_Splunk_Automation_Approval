#!/bin/bash

echo "📦 Installing Python dependencies..."
pip install requests --quiet

echo "📁 Checking log files in logs/ directory..."
ls -l logs/ || echo "⚠️ logs/ directory not found!"

echo "🚀 Starting Python script to send logs to Splunk..."

python3 <<EOF
import json
import requests
import glob
import os

# 🔐 Hardcoded Splunk credentials (for testing/demo ONLY)
SPLUNK_HEC_URL = "https://prd-p-xugh6.splunkcloud.com:8088"
SPLUNK_HEC_TOKEN = "a6a4f859-d3ee-4331-92ac-02b9bd9ea9b7"
SPLUNK_INDEX = "harness_demo"
SPLUNK_SOURCETYPE = "app_logs"  # 👈 Change if needed

headers = {
    "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
    "Content-Type": "application/json"
}

log_files = glob.glob("logs/app.log")

if not log_files:
    print("⚠️ No log files found in logs/errors.log — skipping send.")
else:
    print(f"📂 Found log file(s): {log_files}")

for filepath in log_files:
    with open(filepath, "r") as f:
        for line in f:
            if not line.strip():
                continue
            payload = {
                "event": line.strip(),
                "sourcetype": SPLUNK_SOURCETYPE,
                "index": SPLUNK_INDEX
            }
            print(f"📤 Sending: {payload}")  # Debug: print what's being sent
            try:
                response = requests.post(
                    f"{SPLUNK_HEC_URL}/services/collector/event",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=10,
                    verify=False
                )
                if response.status_code == 200:
                    print(f"✅ Sent: {line.strip()}")
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"❌ Exception while sending log: {e}")
EOF