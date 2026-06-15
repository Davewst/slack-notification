import os, sys, smtplib
from email.message import EmailMessage
from pathlib import Path

report = Path(os.environ["REPORT_PATH"])
if not report.is_file():
    sys.exit(f"ERROR: report not found: {report}")

msg = EmailMessage()
msg["Subject"] = os.environ["SUBJECT"]
msg["From"] = os.environ["SENDER"]
msg["To"] = os.environ["RECIPIENTS"]
msg.set_content("Attached is the latest container security scan report.")
msg.add_attachment(report.read_bytes(), maintype="text",
                   subtype="html", filename=report.name)

with smtplib.SMTP(env("SMTP_SERVER"), int(env("SMTP_PORT", default="587"))) as s:
    s.starttls()
    s.login(env("SMTP_USERNAME"), env("SMTP_PASSWORD"))
    s.send_message(msg)
print(f"Email sent with {report.name} attached")
