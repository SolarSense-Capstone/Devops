import json
from datetime import datetime

with open('render-logs-feb21-22.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

logs = []
for i, line in enumerate(lines):
    line = line.strip()
    if line:
        log_entry = {
            "line_number": i + 1,
            "timestamp": datetime.now().isoformat(),
            "message": line
        }
        logs.append(log_entry)

with open('render-logs-feb21-22.json', 'w', encoding='utf-8') as f:
    json.dump(logs, f, indent=2)

print(f"Converted {len(logs)} log lines to JSON")
print("Saved as: render-logs-feb21-22.json")
