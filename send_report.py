import os, sys, subprocess 

report = os.environ["REPORT_PATH"]
if not os.path.isfile(report):
    sys.exit(f"ERROR: report not found: {report}")

recipients = [r.strip() for r in os.environ["RECIPIENTS"].split(",") if r.strip()]
body = os.environ.get("BODY", " find attached the latest container scan report.")

# mailutils attaches with -A; RHEL/s-nail mailx uses -a
cmd = ["mail", "-s", os.environ["SUBJECT"], "-r", os.environ["SENDER"],
       "-A", report, *recipients]

subprocess.run(cmd, input=body, text=True, check=True)
print(f"Email sent: {report}")
