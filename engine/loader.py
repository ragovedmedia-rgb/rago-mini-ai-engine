import importlib

def load_tool(category, tool, data):

    try:
        # Build module path properly
        module_path = f"categories.{category}.{tool}.main"

        module = importlib.import_module(module_path)

        if hasattr(module, "run"):
            return module.run(data)
        else:
            return {
                "success": False,
                "error": "run() not found in tool"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
