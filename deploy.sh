#!/bin/bash

echo "Starting Python script to send logs to Splunk..."

python3 <<EOF
import json
import requests
import glob

# 🔐 Hardcoded Splunk credentials (for testing/demo ONLY)
SPLUNK_HEC_URL = "https://prd-p-xugh6.splunkcloud.com:8088"
SPLUNK_HEC_TOKEN = "a6a4f859-d3ee-4331-92ac-02b9bd9ea9b7"
SPLUNK_INDEX = "harness_demo"

headers = {
    "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
    "Content-Type": "application/json"
}

log_files = glob.glob("logs/*.log")

for filepath in log_files:
    with open(filepath, "r") as f:
        for line in f:
            if not line.strip():
                continue
            payload = {
                "event": line.strip(),
                "sourcetype": "_json",
                "index": SPLUNK_INDEX
            }
            try:
                response = requests.post(
                    f"{SPLUNK_HEC_URL}/services/collector/event",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=10
                )
                if response.status_code == 200:
                    print(f"✅ Sent: {line.strip()}")
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"❌ Exception: {e}")
EOF
