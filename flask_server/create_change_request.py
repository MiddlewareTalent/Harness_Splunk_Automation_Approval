import requests
from requests.auth import HTTPBasicAuth
import json

# Replace with your ServiceNow instance and credentials
INSTANCE = "https://dev228482.service-now.com"
USERNAME = "admin"
PASSWORD = "Gb2NQv*V7pw!"

# Change request endpoint
url = f"{INSTANCE}/api/now/table/change_request"

# Payload for the change request
payload = {
    "short_description": "Deploy logs to Splunk via Harness pipeline",
    "description": "Automated CI/CD log deployment. Awaiting approval.",
    "category": "Software",
    "priority": "2",
    "state": "New"
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Make the request
response = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers, data=json.dumps(payload))

# Parse response
if response.status_code == 201:
    result = response.json()["result"]
    print("✅ Change Request created:")
    print("Number:", result["number"])
    print("Sys ID:", result["sys_id"])
else:
    print("❌ Failed to create change request:")
    print(response.status_code, response.text)