from flask import Flask, request, jsonify
from engine.loader import load_tool

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Rago Mini AI Engine running",
        "endpoints": ["/run"]
    })

@app.route("/run", methods=["POST"])
def run_tool():
    data = request.json

    category = data.get("category")
    tool = data.get("tool")

    result = load_tool(category, tool)

    return jsonify({
        "result": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
