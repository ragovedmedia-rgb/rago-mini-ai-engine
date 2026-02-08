import importlib
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_tool(category, tool):
    module_path = f"categories.{category}.{tool}.main"

    try:
        module = importlib.import_module(module_path)
        return module
    except Exception as e:
        raise Exception(f"Tool load failed: {str(e)}")

