# ----------------------------------------
# RAGO AI - AUTO MATCH ENGINE
# Main entry point for auto_match_reference
# ----------------------------------------

# Image decode helper
from .utils import decode_base64_image

# Log → Linear conversion
from .log_linear import prepare_for_analysis

# Color transfer (look matching)
from .color_transfer import color_transfer

# Image analyzers
from .analyzer_reference import analyze_reference
from .analyzer_source import analyze_source

# Solvers
from .level_match import solve_levels
from .color_match import solve_color
from .tone_match import solve_tone
from .palette_match import solve_palette

# Slider & wheel builders
from .slider_solver import build_sliders
from .color_wheel_solver import solve_color_wheels


from .histogram_match import histogram_match
from .zone_harmony import zone_harmony

def run(data):

    try:

        # ----------------------------------------
        # 1. Get reference and source images
        # ----------------------------------------

        reference = data.get("reference")
        source = data.get("source")

        if not reference or not source:
            return {
                "success": False,
                "error": "Missing reference or source frame"
            }

        # ----------------------------------------
        # 2. Decode Base64 images → numpy arrays
        # ----------------------------------------

        ref_img = decode_base64_image(reference)
        src_img = decode_base64_image(source)

        if ref_img is None or src_img is None:
            return {
                "success": False,
                "error": "Image decode failed"
            }

        # ----------------------------------------
        # 3. Convert images to linear light
        # (Log/Gamma → Linear normalization)
        # ----------------------------------------

       # STEP 1: match in normal space (0–255)
        matched = histogram_match(src_img, ref_img)
        src_img = zone_harmony(matched, ref_img)

        # STEP 2: convert for analysis (linear)
        ref_img = prepare_for_analysis(ref_img)
        src_img = prepare_for_analysis(src_img)
        

        # ----------------------------------------
        # 4. Apply color transfer
        # (Reference look → Source image)
        # ----------------------------------------

       # ========================================
# TEMP DISABLE COLOR TRANSFER (FIX)
# ========================================

# try:
#     matched_img = color_transfer(reference, source)
#
#     if matched_img is not None:
#         src_img = matched_img
#
# except Exception:
#     pass
        # ----------------------------------------
        # 5. Analyze images (color statistics)
        # ----------------------------------------

        ref_stats = analyze_reference(ref_img)
        src_stats = analyze_source(src_img)

        # ----------------------------------------
        # 6. Solve level differences
        # ----------------------------------------

        level_data = solve_levels(ref_stats, src_stats)

        # ----------------------------------------
        # 7. Solve color differences
        # ----------------------------------------

        color_data = solve_color(ref_img, src_img)

        # ----------------------------------------
        # 8. Solve tone differences
        # ----------------------------------------

        tone_data = solve_tone(ref_img, src_img)

        # ----------------------------------------
        # 9. Palette harmony match
        # ----------------------------------------

        palette_data = solve_palette(ref_img, src_img)

        # ----------------------------------------
        # 10. Build grading sliders
        # ----------------------------------------

        sliders = build_sliders(ref_stats, src_stats, palette_data)

        # ----------------------------------------
        # 11. Solve Lift / Gamma / Gain wheels
        # ----------------------------------------

        wheels = solve_color_wheels(ref_img, src_img)

        # ----------------------------------------
        # 12. Return final grading data
        # ----------------------------------------

        debug_mode = data.get("debug", False)

        response = {
            "success": True,
            "sliders": sliders,
            "wheels": wheels
        }

        # Debug mode: include analysis stats
        if debug_mode:
            response["reference_stats"] = ref_stats
            response["source_stats"] = src_stats
            response["levels"] = level_data
            response["color"] = color_data
            response["tone"] = tone_data
            response["palette"] = palette_data

        return response

    # ----------------------------------------
    # Global safety catch
    # ----------------------------------------

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
