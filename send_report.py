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

to_list = [r.strip() for r in recipients.split(",") if r.strip()]
if not to_list:
    sys.exit("ERROR: no valid recipients")

# The attach flag differs by mail implementation:
#   GNU mailutils -> -A     s-nail / heirloom mailx (RHEL) -> -a
# Detect it so the same action works on any host (your box AND EPA's th878).
attach_flag = "-a"
try:
    ver = subprocess.run(["mail", "--version"], capture_output=True, text=True)
    if "mailutils" in (ver.stdout + ver.stderr).lower():
        attach_flag = "-A"
except Exception:
    pass   # detection failed -> default -a (correct for s-nail / mailx)

# Delivery goes through the HOST's configured mail relay: no SMTP creds needed.
cmd = ["mail", "-s", subject, "-r", sender, attach_flag, str(report), *to_list]

try:
    subprocess.run(cmd, input=body, text=True, check=True)   # no shell=True -> no injection
    print(f"Email sent ({attach_flag} attach): {report.name} -> {', '.join(to_list)}")
except FileNotFoundError:
    sys.exit("ERROR: 'mail' not found -- install s-nail or mailutils on the runner host")
except subprocess.CalledProcessError as e:
    sys.exit(f"ERROR: mail command failed (exit {e.returncode})")
