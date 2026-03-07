import numpy as np


def solve_levels(ref, src):

    # -----------------------------
    # Read values safely
    # -----------------------------

    src_black = src.get("black", 0.0)
    src_white = src.get("white", 255.0)
    src_mid   = src.get("mid", 128.0)

    ref_black = ref.get("black", 0.0)
    ref_white = ref.get("white", 255.0)
    ref_mid   = ref.get("mid", 128.0)

    src_contrast = src.get("contrast", 1.0)
    ref_contrast = ref.get("contrast", 1.0)

    # -----------------------------
    # Black point alignment
    # -----------------------------

    black_shift = ref_black - src_black
    black_shift = np.clip(black_shift, -50, 50)

    # -----------------------------
    # White point alignment
    # -----------------------------

    white_shift = ref_white - src_white
    white_shift = np.clip(white_shift, -50, 50)

    # -----------------------------
    # Midtone gamma solve
    # -----------------------------

    safe_src_mid = max(src_mid, 1e-6)

    gamma = ref_mid / safe_src_mid

    # stabilize gamma
    gamma = np.sqrt(gamma)

    gamma = np.clip(gamma, 0.65, 1.6)

    # -----------------------------
    # Contrast solve (dynamic range)
    # -----------------------------

    src_range = src_white - src_black
    ref_range = ref_white - ref_black

    if src_range < 1e-6:
        contrast_ratio = 0
    else:
        contrast_ratio = (ref_range / src_range) - 1

    stat_contrast = (ref_contrast - src_contrast) * 0.2

    contrast = (contrast_ratio * 0.7) + stat_contrast

    contrast = np.clip(contrast, -1.5, 1.5)

    # -----------------------------
    # Return normalized values
    # -----------------------------

    return {
        "black_shift": float(black_shift),
        "white_shift": float(white_shift),
        "gamma": float(gamma),
        "contrast": float(contrast)
    }
