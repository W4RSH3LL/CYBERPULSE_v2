import json
from datetime import datetime

def generate_report(scans: list):
    report = {
        "generated_at": datetime.now().isoformat(),
        "scans": [scan.report() for scan in scans]
    }

    with open("security_report.json", "w") as f:
        json.dump(report, f, indent=4)

    return "security_report.json"
