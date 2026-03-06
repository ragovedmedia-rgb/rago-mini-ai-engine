from .auto_match import auto_match
from .accurate_match import accurate_color_match


def run(data):

    reference = data.get("reference")
    source = data.get("source")

    if not reference or not source:
        return {
            "success": False,
            "error": "Missing reference or source frame"
        }

    try:
        # 🔥 Use new accurate matching engine
        sliders = accurate_color_match(reference, source)

    except Exception as e:
        # fallback to old engine if anything fails
        print("Accurate match failed, using auto_match:", e)
        sliders = auto_match(reference, source)

    return {
        "success": True,
        "sliders": sliders
    }
