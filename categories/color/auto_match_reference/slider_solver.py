import numpy as np


def clamp(v, limit=100):
    return float(max(-limit, min(limit, v)))


def build_sliders(ref, src, palette):

    # -----------------------------
    # Safe value extraction
    # -----------------------------

    ref_brightness = float(ref.get("brightness", 0.0))
    src_brightness = float(src.get("brightness", 0.0))

    ref_contrast = float(ref.get("contrast", 1.0))
    src_contrast = float(src.get("contrast", 1.0))

    ref_sat = float(ref.get("saturation", 1.0))
    src_sat = float(src.get("saturation", 1.0))

    ref_temp = float(ref.get("temperature", 0.0))
    src_temp = float(src.get("temperature", 0.0))

    ref_tint = float(ref.get("tint", 0.0))
    src_tint = float(src.get("tint", 0.0))

    # -----------------------------
    # Exposure (ratio + diff)
    # -----------------------------

    exp_diff = (ref_brightness - src_brightness) * 0.08

    exp_ratio = (ref_brightness / (src_brightness + 1e-6)) - 1
    exp_ratio *= 0.3

    exposure = exp_diff + exp_ratio

    # -----------------------------
    # Contrast (dynamic range based)
    # -----------------------------

    src_black = float(src.get("black", 0.0))
    src_white = float(src.get("white", 255.0))

    ref_black = float(ref.get("black", 0.0))
    ref_white = float(ref.get("white", 255.0))

    src_range = src_white - src_black
    ref_range = ref_white - ref_black

    if src_range < 1e-6:
        contrast = 0.0
    else:
        contrast = (ref_range / src_range) - 1.0

    contrast += (ref_contrast - src_contrast) * 0.2

    contrast = np.clip(contrast * 1.2, -1.5, 1.5)

    # -----------------------------
    # Saturation (strong solver)
    # -----------------------------

    sat_ratio = (ref_sat / (src_sat + 1e-6)) - 1
    sat_diff = (ref_sat - src_sat) * 0.5

    saturation = (sat_ratio * 0.7) + sat_diff

    # -----------------------------
    # Temperature
    # -----------------------------

    temp_diff = (ref_temp - src_temp) * 0.05
    temp_ratio = (ref_temp / (abs(src_temp) + 1e-6)) * 0.02

    temperature = temp_diff + temp_ratio

    # -----------------------------
    # Tint
    # -----------------------------

    tint_diff = (ref_tint - src_tint) * 0.05
    tint = tint_diff

    # -----------------------------
    # Palette correction
    # -----------------------------

    red_shift = float(palette.get("red_shift", 0.0))
    green_shift = float(palette.get("green_shift", 0.0))
    blue_shift = float(palette.get("blue_shift", 0.0))

    palette_temp = (red_shift - blue_shift) * 0.015
    palette_tint = green_shift * 0.015

    temperature += palette_temp
    tint += palette_tint

    # -----------------------------
    # Final sliders
    # -----------------------------

    sliders = {
        "exposure": clamp(exposure),
        "contrast": clamp(contrast),
        "saturation": clamp(saturation),
        "temperature": clamp(temperature),
        "tint": clamp(tint)
    }

    return sliders
