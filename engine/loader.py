import json
import os

def load_tool(category, tool):
    base_path = os.path.join("categories", category, tool)
    tool_json = os.path.join(base_path, "tool.json")

    if not os.path.exists(tool_json):
        return {"error": "Tool not found"}

    with open(tool_json, "r") as f:
        tool_config = json.load(f)

    return {
        "status": "loaded",
        "tool": tool_config
    }
