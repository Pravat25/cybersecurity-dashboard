from flask import Flask, render_template

app = Flask(__name__)

def read_logs():
    try:
        with open("../packet-sniffer/packet_log.txt", "r") as f:
            logs = f.readlines()
            return logs[::-1]
    except:
        return ["No logs found"]

@app.route("/")
def home():
    logs = read_logs()
    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
