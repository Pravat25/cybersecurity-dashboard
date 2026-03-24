from flask import Flask, render_template

app = Flask(__name__)

def read_logs():
    try:
        with open("../packet-sniffer/packet_log.txt", "r") as f:
            logs = f.readlines()[::-1]
    except:
        logs = ["No logs found"]

    stats = {
        "total": 0,
        "tcp": 0,
        "udp": 0,
        "icmp": 0,
        "warning": 0,
        "critical": 0
    }

    processed_logs = []

    for log in logs:
        stats["total"] += 1

        if "TCP" in log:
            stats["tcp"] += 1
        elif "UDP" in log:
            stats["udp"] += 1
        elif "ICMP" in log:
            stats["icmp"] += 1

        # Detection rules
        if "22" in log or "3389" in log:
            stats["warning"] += 1
            log = "WARNING: Suspicious port activity | " + log

        elif "Failed" in log or "error" in log.lower():
            stats["critical"] += 1
            log = "CRITICAL: Possible attack detected | " + log

        processed_logs.append(log)

    return processed_logs, stats


@app.route("/")
def home():
    logs, stats = read_logs()
    return render_template("index.html", logs=logs, stats=stats)


if __name__ == "__main__":
    app.run(debug=True)
