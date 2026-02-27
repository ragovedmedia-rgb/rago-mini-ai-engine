from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from engine.loader import load_tool
import os

app = Flask(__name__)

# ===============================
# CORS (CRITICAL FOR FRONTEND)
# ===============================
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)


# ===============================
# HEALTH CHECK
# ===============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Rago Mini AI Engine running",
        "endpoints": ["/run"]
    })


# ===============================
# RUN TOOL (CORS SAFE)
# ===============================
@app.route("/run", methods=["POST", "OPTIONS"])
def run_tool():

    # Handle browser preflight request
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400

        data = request.get_json()

        category = data.get("category")
        tool = data.get("tool")

        if not category or not tool:
            return jsonify({
                "success": False,
                "error": "Missing category or tool"
            }), 400

        # Execute tool
        result = load_tool(category, tool, data)

        # Ensure proper JSON response
        if isinstance(result, dict):
            return jsonify(result), 200
        else:
            return jsonify({
                "success": True,
                "data": result
            }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ===============================
# LUT DOWNLOAD ROUTE
# ===============================
@app.route("/storage/luts/<path:filename>", methods=["GET"])
def download_lut(filename):
    return send_from_directory(
        os.path.join("storage", "luts"),
        filename,
        as_attachment=True
    )


# ===============================
# RENDER DYNAMIC PORT
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
