import numpy as np


def level_match(ref, src):

    # -----------------------------
    # Black point alignment
    # -----------------------------

    black_shift = ref["black"] - src["black"]

    # -----------------------------
    # White point alignment
    # -----------------------------

    white_shift = ref["white"] - src["white"]

    # -----------------------------
    # Midtone gamma solve
    # -----------------------------

    gamma = (ref["mid"] / (src["mid"] + 1e-6))

    # -----------------------------
    # Contrast difference
    # -----------------------------

    contrast = (ref["contrast"] - src["contrast"]) * 0.05

    return {
        "black_shift": float(black_shift),
        "white_shift": float(white_shift),
        "gamma": float(gamma),
        "contrast": float(contrast)
    }
