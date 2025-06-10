from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Global dictionary to track approval status and reasons
status = {"approved": None, "reason": None}

@app.route("/approve", methods=["GET"])
def approve():
    status["approved"] = True
    status["reason"] = None
    return "<h2>✅ Approved</h2><p>The deployment has been approved successfully.</p>"

@app.route("/reject", methods=["GET", "POST"])
def reject():
    if request.method == "GET":
        # Show a form to enter rejection reason
        return render_template_string("""
            <html>
            <head><title>Reject Deployment</title></head>
            <body style="font-family: Arial; text-align: center;">
                <h2>❌ Reject Deployment</h2>
                <form method="post">
                    <label for="reason">Please enter the reason for rejection:</label><br><br>
                    <textarea name="reason" rows="4" cols="50" required></textarea><br><br>
                    <button type="submit" style="padding: 10px 20px;">Submit Rejection</button>
                </form>
            </body>
            </html>
        """)
    else:
        # Handle the reason submitted via form
        reason = request.form.get("reason", "No reason provided")
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