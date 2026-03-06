from .auto_match import auto_match


def run(data):

    reference = data.get("reference")
    source = data.get("source")

    if not reference or not source:
        return {
            "success": False,
            "error": "Missing reference or source frame"
        }

    sliders = auto_match(reference, source)

    return {
        "success": True,
        "sliders": sliders
    }
