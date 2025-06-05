from flask import Flask, request
app = Flask(__name__)

status = {"approved": None, "reason": ""}

@app.route("/approve", methods=["GET"])
def approve():
    status["approved"] = True
    return "<h2>✅ Approved</h2>"

@app.route("/reject", methods=["GET"])
def reject():
    status["approved"] = False
    reason = request.args.get("reason", "No reason provided")
    status["reason"] = reason
    return f"<h2>❌ Rejected</h2><p>Reason: {reason}</p>"

@app.route("/status", methods=["GET"])
def get_status():
    return status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)