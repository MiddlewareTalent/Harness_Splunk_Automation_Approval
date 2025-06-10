import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get dynamic Git info
def get_git_info():
    author = subprocess.getoutput("git log -1 --pretty=format:'%an'")
    commit_msg = subprocess.getoutput("git log -1 --pretty=format:'%s'")
    branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
    commit_hash = subprocess.getoutput("git rev-parse --short HEAD")
    return author.strip("'"), commit_msg, branch, commit_hash

author, commit_msg, branch, commit_hash = get_git_info()

# Configs
NGROK_URL = "https://38a3-136-232-205-158.ngrok-free.app"
GITHUB_REPO_URL = "https://github.com/MiddlewareTalent/Harness_Splunk_Automation_Approval.git"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "yaswanthkumarch2001@gmail.com"
PASSWORD = "uqjc bszf djfw bsor"
TO_EMAIL = "Raviteja@middlewaretalents.com"

# Email setup
msg = MIMEMultipart("alternative")
msg["Subject"] = "🛡️ Deployment Approval Request – Harness Splunk Pipeline"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL

approve_link = f"{NGROK_URL}/approve"
reject_link = f"{NGROK_URL}/reject?reason=manual"

html = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; color: #333;">
    <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
      <h2 style="color: #2c3e50;">🚀 Deployment Approval Required</h2>
      <p><strong>Environment:</strong> <span style="color: #2980b9;">Production</span></p>
      <p><strong>Triggered By:</strong> {author}</p>
      <p><strong>Branch:</strong> <code>{branch}</code></p>
      <p><strong>Commit:</strong> {commit_msg} <code>({commit_hash})</code></p>

      <hr style="margin: 20px 0;">

      <p style="font-size: 16px;">Please review and approve/reject this deployment within the next <strong>5 minutes</strong>.</p>

      <div style="margin: 20px 0;">
        <a href="{approve_link}" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">✅ Approve</a>
        <a href="{reject_link}" style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-left: 15px;">❌ Reject</a>
      </div>

      <hr style="margin: 30px 0;">
      <p><strong>🔗 GitHub Repository:</strong><br>
        <a href="{GITHUB_REPO_URL}" style="color: #007bff;">{GITHUB_REPO_URL}</a>
      </p>

      <p style="font-size: 12px; color: gray; margin-top: 40px;">This is an automated approval request from the Harness CI/CD pipeline.</p>
    </div>
  </body>
</html>
"""

msg.attach(MIMEText(html, "html"))

# Send the email
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

print("📧 Approval email sent.")