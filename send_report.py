import os, sys, smtplib
from email.message import EmailMessage
from pathlib import Path

def env(name, default=None, required=True):
    val = os.environ.get(name, default)
    if required and not val:
        sys.exit(f"ERROR: {name} is empty or unset")
    return val

report = Path(env("REPORT_PATH"))
if not report.is_file():
    sys.exit(f"ERROR: report not found: {report}")

msg = EmailMessage()
msg["Subject"] = env("SUBJECT")
msg["From"]    = env("SENDER")
msg["To"]      = env("RECIPIENTS")
msg.set_content("Attached is the latest container security scan report.")
msg.add_attachment(report.read_bytes(), maintype="text",
                   subtype="plain", filename=report.name)

with smtplib.SMTP(env("SMTP_SERVER"), int(env("SMTP_PORT", default="587"))) as s:
    s.starttls()
    s.login(env("SMTP_USERNAME"), env("SMTP_PASSWORD"))
    s.send_message(msg)

print(f"Email sent with {report.name} attached")
