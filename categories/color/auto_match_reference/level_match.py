import numpy as np


def solve_levels(ref, src):

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
    gamma = ref["mid"] / (src["mid"] + 1e-6)

    # clamp gamma (avoid extreme curves)
    gamma = np.clip(gamma, 0.5, 2.0)

    # -----------------------------
    # Contrast difference
    # -----------------------------
    contrast = (ref["contrast"] - src["contrast"]) * 0.05

    # clamp contrast
    contrast = np.clip(contrast, -1.0, 1.0)

    # -----------------------------
    # Return normalized data
    # -----------------------------
    return {
        "black_shift": float(black_shift),
        "white_shift": float(white_shift),
        "gamma": float(gamma),
        "contrast": float(contrast)
    }
