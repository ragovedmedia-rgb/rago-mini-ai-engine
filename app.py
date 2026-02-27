from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from engine.loader import load_tool
import os

app = Flask(__name__)

# ✅ Proper CORS for cross-domain (Frontend → Render)
CORS(app, resources={r"/*": {"origins": "*"}})


# ===============================
# Health Check Route
# ===============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Rago Mini AI Engine running",
        "endpoints": ["/run"]
    })


# ===============================
# Run Tool Route
# ===============================
@app.route("/run", methods=["POST"])
def run_tool():
    try:
        data = request.json

        category = data.get("category")
        tool = data.get("tool")

        # Load & execute tool
        result = load_tool(category, tool)

        # Directly return tool response
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


# ===============================
# LUT Download Route
# ===============================
@app.route("/storage/luts/<path:filename>")
def download_lut(filename):
    return send_from_directory("storage/luts", filename, as_attachment=True)


# ===============================
# Render Dynamic Port (IMPORTANT)
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
