from .matcher import auto_match

def run(data):

    reference = data.get("reference")
    source = data.get("source")

    if not reference or not source:
        return {
            "success": False,
            "error": "Missing frames"
        }

    sliders = auto_match(reference, source)

    return {
        "success": True,
        "sliders": sliders
    }
