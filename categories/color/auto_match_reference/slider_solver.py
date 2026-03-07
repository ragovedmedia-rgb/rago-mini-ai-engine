import numpy as np


def clamp(v, limit=100):
    return float(max(-limit, min(limit, v)))


def build_sliders(ref, src, palette):

    # -----------------------------
    # Safe value extraction
    # -----------------------------

    ref_brightness = ref.get("brightness", 0.0)
    src_brightness = src.get("brightness", 0.0)

    ref_contrast = ref.get("contrast", 1.0)
    src_contrast = src.get("contrast", 1.0)

    ref_sat = ref.get("saturation", 1.0)
    src_sat = src.get("saturation", 1.0)

    ref_temp = ref.get("temperature", 0.0)
    src_temp = src.get("temperature", 0.0)

    ref_tint = ref.get("tint", 0.0)
    src_tint = src.get("tint", 0.0)

    # -----------------------------
    # Exposure (ratio + diff)
    # -----------------------------

    exp_diff = (ref_brightness - src_brightness) * 0.08

    exp_ratio = (ref_brightness / (src_brightness + 1e-6)) - 1
    exp_ratio *= 0.3

    exposure = exp_diff + exp_ratio

    # -----------------------------
    # Contrast (range + stat)
    # -----------------------------

    contrast_diff = (ref_contrast - src_contrast) * 0.4

    contrast_ratio = (ref_contrast / (src_contrast + 1e-6)) - 1
    contrast_ratio *= 0.6

    contrast = contrast_diff + contrast_ratio

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

    red_shift = palette.get("red_shift", 0.0)
    green_shift = palette.get("green_shift", 0.0)
    blue_shift = palette.get("blue_shift", 0.0)

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
