from engine.loader import load_tool

@app.route("/run", methods=["POST"])
def run_tool():
    data = request.json or {}
    category = data.get("category")
    tool = data.get("tool")

    if not category or not tool:
        return jsonify({"error": "category and tool required"}), 400

    try:
        tool_module = load_tool(category, tool)

        if not hasattr(tool_module, "run"):
            return jsonify({"error": "Tool has no run()"}), 500

        result = tool_module.run(data)
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
