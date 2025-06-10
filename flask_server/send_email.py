import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your ngrok URL
NGROK_URL = "https://38a3-136-232-205-158.ngrok-free.app"

# GitHub repo link (for deployment context)
GITHUB_REPO_URL = "https://github.com/MiddlewareTalent/Harness_Splunk_Automation_Approval.git"

# SMTP Config (Use real SMTP)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "yaswanthkumarch2001@gmail.com"
PASSWORD = "uqjc bszf djfw bsor"
TO_EMAIL = "Raviteja@middlewaretalents.com"

# Construct the email
msg = MIMEMultipart("alternative")
msg["Subject"] = "🛡️ Harness Deployment Approval Needed"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL

approve_link = f"{NGROK_URL}/approve"
reject_link = f"{NGROK_URL}/reject?reason=manual"

html = f"""
<html>
  <body style="font-family: Arial, sans-serif; text-align: center;">
    <h2>🚀 Deployment Approval Required</h2>
    <p>A new deployment is pending approval. Please review and take action:</p>

    <a href="{approve_link}" style="padding: 10px 20px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 10px;">✅ Approve</a>
    <a href="{reject_link}" style="padding: 10px 20px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 5px; margin: 10px;">❌ Reject</a>

    <p>If you do nothing, the deployment will timeout after 5 minutes.</p>

    <hr style="margin-top:30px; margin-bottom:20px;">
    <p style="font-size: 14px;">🔗 <strong>GitHub Repository:</strong><br>
    <a href="{GITHUB_REPO_URL}" style="color: #0366d6;">{GITHUB_REPO_URL}</a></p>
  </body>
</html>
"""

msg.attach(MIMEText(html, "html"))

# Send the email
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

print("📧 Email sent.")