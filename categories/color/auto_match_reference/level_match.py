import numpy as np


def level_match(ref, src):

    # -----------------------------
    # Black point match
    # -----------------------------
    black_shift = (ref["black"] - src["black"]) * 0.08

    # -----------------------------
    # White point match
    # -----------------------------
    white_shift = (ref["white"] - src["white"]) * 0.08

    # -----------------------------
    # Gamma / midtone match
    # -----------------------------
    gamma = (ref["mid"] - src["mid"]) * 0.04

    # -----------------------------
    # Contrast solve
    # -----------------------------
    contrast = (ref["contrast"] - src["contrast"]) * 0.06

    # -----------------------------
    # Exposure
    # -----------------------------
    exposure = (ref["brightness"] - src["brightness"]) * 0.05

    return {
        "black_shift": float(black_shift),
        "white_shift": float(white_shift),
        "gamma": float(gamma),
        "contrast": float(contrast),
        "exposure": float(exposure)
    }
