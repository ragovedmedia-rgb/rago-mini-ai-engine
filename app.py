from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "Rago Mini AI Engine running",
        "engine": "rago-mini-ai",
        "version": "0.1"
    })

@app.route("/health")
def health():
    return jsonify({"ok": True})

@app.route("/run", methods=["POST"])
def run_tool():
    data = request.json or {}

    category = data.get("category")
    tool = data.get("tool")

    if not category or not tool:
        return jsonify({
            "error": "category and tool required"
        }), 400

    return jsonify({
        "message": "Tool request received",
        "category": category,
        "tool": tool,
        "status": "next: tool execution"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

