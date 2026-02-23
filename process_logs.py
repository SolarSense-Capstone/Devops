import json

input_file = "render-logs-feb23.txt"
output_file = "render-logs-feb23.json"

logs = []

with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        # Only process lines that start with a proper ISO timestamp
        if not line.startswith("2026-"):
            continue

        try:
            parts = line.split(" - ")

            if len(parts) != 3:
                continue

            timestamp = parts[0]

            method_endpoint = parts[1].split()
            if len(method_endpoint) != 2:
                continue

            method = method_endpoint[0]
            endpoint = method_endpoint[1]

            ip = parts[2].replace("IP:", "").strip()

            logs.append({
                "timestamp": timestamp,
                "method": method,
                "endpoint": endpoint,
                "ip": ip
            })

        except Exception:
            continue

with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(logs, outfile, indent=2)

print(f"Finished. Extracted {len(logs)} log entries.")
