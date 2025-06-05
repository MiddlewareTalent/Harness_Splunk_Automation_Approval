from flask import Flask, request, jsonify

app = Flask(__name__)

# Global dictionary to track approval status and reason
status = {"approved": None, "reason": None}

@app.route("/approve", methods=["GET"])
def approve():
    status["approved"] = True
    status["reason"] = None
    return "<h2>✅ Approved</h2>"

@app.route("/reject", methods=["GET"])
def reject():
    reason = request.args.get("reason", "No reason provided")
    status["approved"] = False
    status["reason"] = reason
    return f"<h2>❌ Rejected</h2><p>Reason: {reason}</p>"

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(status)

@app.route("/reset", methods=["POST"])
def reset():
    status["approved"] = None
    status["reason"] = None
    return jsonify({"message": "Approval status reset."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
