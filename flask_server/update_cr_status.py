import requests
import json
import datetime
import subprocess
import pytz

# ----------------------------
# ServiceNow Configuration
# ----------------------------
SNOW_INSTANCE = "https://dev228482.service-now.com"
USERNAME = "admin"
PASSWORD = "Gb2NQv*V7pw!"

# ----------------------------
# Get Approver Info from Git
# ----------------------------
def get_approver_info():
    try:
        approver_name = subprocess.getoutput("git log -1 --pretty=format:'%an'").strip("'")
    except:
        approver_name = "Unknown Approver"

    ist = pytz.timezone("Asia/Kolkata")
    timestamp = datetime.datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
    return approver_name, timestamp

# ----------------------------
# Update CR State
# ----------------------------
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

    # Determine ServiceNow state code
    state_code = "3" if state == "approved" else "8"  # 3 = Authorize, 8 = Canceled (for rejected)

    # Prepare work note
    approver, timestamp = get_approver_info()
    detailed_note = (
        f"{'✅' if state == 'approved' else '❌'} Change Request {state.upper()} via SMTP email link.\n"
        f"🔸 By: {approver}\n"
        f"📅 At: {timestamp}\n"
        f"📝 Notes: {notes}"
    )

    # Make API call
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

# ----------------------------
# Main Entry Point
# ----------------------------
if __name__ == "__main__":
    # Change to "rejected" if you're rejecting
    update_cr_state("approved", "Deployment approved successfully.")
