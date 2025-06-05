import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your ngrok URL
NGROK_URL = "https://aa47-136-232-205-158.ngrok-free.app"

# SMTP Config (Use real SMTP)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "yaswanthkumarch2001@gmail.com"
PASSWORD = "uqjc bszf djfw bsor"
TO_EMAIL = "Raviteja@middlewaretalents.com"

msg = MIMEMultipart("alternative")
msg["Subject"] = "🛡️ Harness Deployment Approval Needed"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL

approve_link = f"{NGROK_URL}/approve"
reject_link = f"{NGROK_URL}/reject?reason=manual"

html = f"""
<html>
  <body>
    <p>Click below to approve or reject the deployment:</p>
    <a href="{approve_link}">✅ Approve</a><br>
    <a href="{reject_link}">❌ Reject</a>
  </body>
</html>
"""

msg.attach(MIMEText(html, "html"))

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

print("📧 Email sent.")
