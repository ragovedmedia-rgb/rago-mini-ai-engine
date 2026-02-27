import importlib.util
import os

def load_tool(category, tool, data):

    base_path = os.path.join("categories", category, tool)
    main_file = os.path.join(base_path, "main.py")

    if not os.path.exists(main_file):
        return {"success": False, "error": "Tool main.py not found"}

    try:
        spec = importlib.util.spec_from_file_location("tool_main", main_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "run"):
            return module.run(data)
        else:
            return {"success": False, "error": "run() not found in tool"}

    except Exception as e:
        return {"success": False, "error": str(e)}
