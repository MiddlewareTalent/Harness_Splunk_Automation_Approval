import requests
import json
import datetime
import subprocess

# ServiceNow configuration
SNOW_INSTANCE = "https://dev228482.service-now.com"
USERNAME = "admin"
PASSWORD = "Gb2NQv*V7pw!"

def get_approver_info():
    try:
        approver_name = subprocess.getoutput("git log -1 --pretty=format:'%an'").strip("'")
    except:
        approver_name = "Unknown Approver"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return approver_name, timestamp

def update_cr_state(state, notes=""):
    try:
        with open("cr_info.json") as f:
            cr = json.load(f)
    except Exception as e:
        print(f"[❌] Failed to load cr_info.json: {e}")
        return

    cr_number = cr.get("number")
    sys_id = cr.get("sys_id")

    if not cr_number or not sys_id:
        print("[❌] Invalid CR data in cr_info.json.")
        return

    # Determine state code
    state_code = "3" if state == "approved" else "4"  # 3: Authorized, 4: Scheduled or rejected depending on your config

    # Construct detailed work note
    approver, timestamp = get_approver_info()
    detailed_note = (
        f"✅ Change Request approved via SMTP email link.\n"
        f"🔸 Approved By: {approver}\n"
        f"📅 Approved At: {timestamp}\n"
        f"📝 Notes: {notes}"
    )

    url = f"{SNOW_INSTANCE}/api/now/table/change_request/{sys_id}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "state": state_code,
        "work_notes": detailed_note
    }

    response = requests.patch(url, auth=(USERNAME, PASSWORD), headers=headers, json=payload)

    if response.status_code == 200:
        print(f"[✅] CR {cr_number} updated to {state.upper()} with detailed work notes.")
    else:
        print(f"[❌] Failed to update CR: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    # You can change this to "rejected" if needed
    update_cr_state("approved", "Deployment approved successfully.")