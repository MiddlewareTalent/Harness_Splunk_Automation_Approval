import requests
import subprocess
import json

# ==== ServiceNow Dev Instance ====
SNOW_INSTANCE = "https://dev228482.service-now.com"
USERNAME = "admin"
PASSWORD = "Gb2NQv*V7pw!"  # Use CyberArk or Harness secrets later for security

# === Fetch Git Commit Metadata ===
def get_git_metadata():
    try:
        author = subprocess.check_output(["git", "log", "-1", "--pretty=format:%an"]).decode().strip()
        email = subprocess.check_output(["git", "log", "-1", "--pretty=format:%ae"]).decode().strip()
        commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"]).decode().strip()
        commit_id = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        return {
            "author": author,
            "email": email,
            "commit_msg": commit_msg,
            "commit_id": commit_id,
            "branch": branch
        }
    except Exception as e:
        print(f"[❌] Failed to fetch Git metadata: {e}")
        return {}

# === Create CR in ServiceNow ===
def create_change_request(metadata):
    url = f"{SNOW_INSTANCE}/api/now/table/change_request"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "short_description": f"Deployment for {metadata['branch']} - {metadata['commit_msg']}",
        "description": f"Deployment triggered by GitHub user: {metadata['author']} ({metadata['email']})\n"
                       f"Commit ID: {metadata['commit_id']}\nBranch: {metadata['branch']}",
        "category": "Software",
        "type": "normal",
        "risk": "low",
        "state": "New"
    }

    response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, json=payload)

    if response.status_code == 201:
        data = response.json()["result"]
        print(f"[✅] CR created: {data['number']} (sys_id: {data['sys_id']})")
        # Save CR sys_id to a file for later update
        with open("cr_info.json", "w") as f:
            json.dump({"sys_id": data["sys_id"], "number": data["number"]}, f)
    else:
        print(f"[❌] Failed to create CR: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    metadata = get_git_metadata()
    if metadata:
        create_change_request(metadata)
