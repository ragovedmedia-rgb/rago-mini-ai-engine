from .utils import decode_base64_image
from .analyzer_reference import analyze_reference
from .analyzer_source import analyze_source
from .level_match import solve_levels
from .color_match import solve_color
from .tone_match import solve_tone
from .slider_solver import build_sliders


def run(data):

    reference = data.get("reference")
    source = data.get("source")

    if not reference or not source:
        return {
            "success": False,
            "error": "Missing reference or source frame"
        }

    ref_img = decode_base64_image(reference)
    src_img = decode_base64_image(source)

    ref_stats = analyze_reference(ref_img)
    src_stats = analyze_source(src_img)

    level_data = solve_levels(ref_stats, src_stats)

    color_data = solve_color(ref_img, src_img)

    tone_data = solve_tone(ref_img, src_img)

    sliders = build_sliders(level_data, color_data, tone_data)

    return {
        "success": True,
        "sliders": sliders
    }
