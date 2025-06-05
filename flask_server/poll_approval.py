import time
import requests

NGROK_STATUS_URL = " https://aa47-136-232-205-158.ngrok-free.app"

print("⏳ Waiting for approval...")

for i in range(30):  # Max wait = 30 * 10 = 300 seconds = 5 min
    try:
        res = requests.get(NGROK_STATUS_URL, timeout=5)
        data = res.json()

        if data["approved"] is True:
            print("✅ Approved. Proceeding...")
            exit(0)
        elif data["approved"] is False:
            print(f"❌ Rejected. Reason: {data['reason']}")
            exit(1)
        else:
            print("⌛ No response yet. Retrying...")
    except Exception as e:
        print("❌ Error:", e)

    time.sleep(10)

print("❌ Timeout. No approval received.")
exit(1)