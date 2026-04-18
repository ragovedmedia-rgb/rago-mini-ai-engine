# ----------------------------------------
# RAGO AI - AUTO MATCH ENGINE
# ----------------------------------------

from .utils import decode_base64_image
from .log_linear import prepare_for_analysis

from .analyzer_reference import analyze_reference
from .analyzer_source import analyze_source

from .level_match import solve_levels
from .color_match import solve_color
from .tone_match import solve_tone
from .palette_match import solve_palette

from .slider_solver import build_sliders
from .color_wheel_solver import solve_color_wheels

from .histogram_match import histogram_match
from .zone_harmony import zone_harmony

import base64
import cv2


def run(data):

    try:

        # ----------------------------------------
        # 1. INPUT
        # ----------------------------------------
        reference = data.get("reference")
        source = data.get("source")

        if not reference or not source:
            return {
                "success": False,
                "error": "Missing reference or source frame"
            }

        # ----------------------------------------
        # 2. DECODE
        # ----------------------------------------
        ref_img = decode_base64_image(reference)
        src_img = decode_base64_image(source)

        if ref_img is None or src_img is None:
            return {
                "success": False,
                "error": "Image decode failed"
            }

        # ----------------------------------------
        # 3. MATCHING (VISIBLE OUTPUT)
        # ----------------------------------------
        matched = histogram_match(src_img, ref_img)

        graded = zone_harmony(matched, ref_img)

        # 👉 keep final image separate
        final_img = graded.copy()

        # ----------------------------------------
        # 4. ANALYSIS (LINEAR SPACE)
        # ----------------------------------------
        ref_linear = prepare_for_analysis(ref_img)
        src_linear = prepare_for_analysis(final_img)

        # ----------------------------------------
        # 5. ANALYZE
        # ----------------------------------------
        ref_stats = analyze_reference(ref_linear)
        src_stats = analyze_source(src_linear)

        # ----------------------------------------
        # 6. SOLVE
        # ----------------------------------------
        level_data = solve_levels(ref_stats, src_stats)
        color_data = solve_color(ref_linear, src_linear)
        tone_data = solve_tone(ref_linear, src_linear)
        palette_data = solve_palette(ref_linear, src_linear)

        sliders = build_sliders(ref_stats, src_stats, palette_data)
        wheels = solve_color_wheels(ref_linear, src_linear)

        # ----------------------------------------
        # 7. RESPONSE
        # ----------------------------------------
        debug_mode = data.get("debug", False)

        response = {
            "success": True,
            "sliders": sliders,
            "wheels": wheels
        }

        # Debug info
        if debug_mode:
            response["reference_stats"] = ref_stats
            response["source_stats"] = src_stats
            response["levels"] = level_data
            response["color"] = color_data
            response["tone"] = tone_data
            response["palette"] = palette_data

        # ----------------------------------------
        # 🔥 ALWAYS RETURN IMAGE (FIXED)
        # ----------------------------------------
        _, buffer = cv2.imencode('.jpg', final_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        response["image"] = f"data:image/jpeg;base64,{img_base64}"

        return response

    # ----------------------------------------
    # ERROR HANDLER
    # ----------------------------------------
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
