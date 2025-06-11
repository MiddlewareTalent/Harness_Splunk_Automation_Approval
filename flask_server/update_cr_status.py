import requests
import json

SNOW_INSTANCE = "https://dev228482.service-now.com"
USERNAME = "admin"
PASSWORD = "Gb2NQv*V7pw!"

def update_cr_state(state, notes=""):
    with open("cr_info.json") as f:
        cr = json.load(f)

    sys_id = cr["sys_id"]
    url = f"{SNOW_INSTANCE}/api/now/table/change_request/{sys_id}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "state": "3" if state == "approved" else "4",  # 3 = Approved, 4 = Rejected
        "work_notes": notes
    }

    response = requests.patch(url, auth=(USERNAME, PASSWORD), headers=headers, json=payload)

    if response.status_code == 200:
        print(f"[✅] CR {cr['number']} updated to {state.upper()}")
    else:
        print(f"[❌] Failed to update CR: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    # Example: update_cr_state("approved", "Deployment approved via SMTP")
    update_cr_state("approved", "Approved via email link")