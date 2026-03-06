import numpy as np


def clamp(v, limit=100):

    return float(max(-limit, min(limit, v)))


def solve_sliders(ref, src, palette):

    # -----------------------------
    # Exposure
    # -----------------------------

    exposure = (ref["brightness"] - src["brightness"]) * 0.08

    # -----------------------------
    # Contrast
    # -----------------------------

    contrast = (ref["contrast"] - src["contrast"]) * 0.05

    # -----------------------------
    # Saturation
    # -----------------------------

    saturation = (ref["saturation"] - src["saturation"]) * 0.02

    # -----------------------------
    # Temperature
    # -----------------------------

    temperature = (ref["temperature"] - src["temperature"]) * 0.02

    # -----------------------------
    # Tint
    # -----------------------------

    tint = (ref["tint"] - src["tint"]) * 0.02

    # -----------------------------
    # Palette correction
    # -----------------------------

    palette_temp = (palette["red_shift"] - palette["blue_shift"]) * 0.01
    palette_tint = palette["green_shift"] * 0.01

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
