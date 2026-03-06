from .utils import decode_base64_image
from .analyzer_reference import analyze_reference
from .analyzer_source import analyze_source
from .level_match import solve_levels
from .color_match import solve_color
from .tone_match import solve_tone
from .slider_solver import build_sliders
from .color_wheel_solver import solve_color_wheels


def run(data):

    reference = data.get("reference")
    source = data.get("source")

    if not reference or not source:
        return {
            "success": False,
            "error": "Missing reference or source frame"
        }

    # ----------------------------------------
    # Decode images
    # ----------------------------------------

    ref_img = decode_base64_image(reference)
    src_img = decode_base64_image(source)

    # ----------------------------------------
    # Analyze reference and source
    # ----------------------------------------

    ref_stats = analyze_reference(ref_img)
    src_stats = analyze_source(src_img)

    # ----------------------------------------
    # Level matching (black / white / gamma)
    # ----------------------------------------

    level_data = solve_levels(ref_stats, src_stats)

    # ----------------------------------------
    # Color matching (temperature / tint / sat)
    # ----------------------------------------

    color_data = solve_color(ref_img, src_img)

    # ----------------------------------------
    # Tone matching (curve alignment)
    # ----------------------------------------

    tone_data = solve_tone(ref_img, src_img)

    # ----------------------------------------
    # Build sliders
    # ----------------------------------------

    sliders = build_sliders(level_data, color_data, tone_data)

    # ----------------------------------------
    # NEW: Solve Lift / Gamma / Gain wheels
    # ----------------------------------------

    wheels = solve_color_wheels(ref_img, src_img)

    # ----------------------------------------
    # Final response
    # ----------------------------------------

    return {
        "success": True,
        "sliders": sliders,
        "wheels": wheels
    }
