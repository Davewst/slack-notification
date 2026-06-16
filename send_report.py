import os, sys, subprocess
from pathlib import Path

def env(name, default=None, required=True):
    val = os.environ.get(name, default)
    if required and not val:
        sys.exit(f"ERROR: {name} is empty or unset")
    return val

report = Path(env("REPORT_PATH"))
if not report.is_file():
    sys.exit(f"ERROR: report not found: {report}")

sender     = env("SENDER")
subject    = env("SUBJECT")
recipients = env("RECIPIENTS")     # comma-separated
body       = env("BODY",
                 default="Please find attached the latest container scan report.",
                 required=False)

# Split recipients into separate args so we don't rely on the shell to parse them.
to_list = [r.strip() for r in recipients.split(",") if r.strip()]
if not to_list:
    sys.exit("ERROR: no valid recipients")

# Delivery goes through the HOST's configured mail relay (mailx / MTA): no SMTP
# server, port, username, or password required. The attach flag is
# implementation-dependent -- RHEL/heirloom mailx uses -a, GNU mailutils uses -A.
cmd = ["mail", "-s", subject, "-r", sender, "-a", str(report), *to_list]

try:
    subprocess.run(cmd, input=body, text=True, check=True)   # no shell=True -> no injection
    print(f"Email sent: {report.name} -> {', '.join(to_list)}")
except FileNotFoundError:
    sys.exit("ERROR: 'mail' not found -- install mailx/mailutils on the runner host")
except subprocess.CalledProcessError as e:
    sys.exit(f"ERROR: mail command failed (exit {e.returncode})")
