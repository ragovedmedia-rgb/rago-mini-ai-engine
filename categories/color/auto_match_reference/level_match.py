import numpy as np


def solve_levels(ref, src):

    # ----------------------------------------
    # Safe read values
    # ----------------------------------------

    src_black = float(src.get("black", 0.0))
    src_white = float(src.get("white", 255.0))
    src_mid   = float(src.get("mid", 128.0))

    ref_black = float(ref.get("black", 0.0))
    ref_white = float(ref.get("white", 255.0))
    ref_mid   = float(ref.get("mid", 128.0))

    src_contrast = float(src.get("contrast", 1.0))
    ref_contrast = float(ref.get("contrast", 1.0))

    # ----------------------------------------
    # Black point alignment
    # ----------------------------------------

    black_shift = ref_black - src_black
    black_shift = np.clip(black_shift, -50.0, 50.0)

    # ----------------------------------------
    # White point alignment
    # ----------------------------------------

    white_shift = ref_white - src_white
    white_shift = np.clip(white_shift, -50.0, 50.0)

    # ----------------------------------------
    # Gamma solve (midtone alignment)
    # ----------------------------------------

    safe_src_mid = max(src_mid, 1e-6)

    gamma = ref_mid / safe_src_mid

    # stabilize gamma curve
    gamma = np.sqrt(gamma)

    gamma = np.clip(gamma, 0.65, 1.6)

    # ----------------------------------------
    # Contrast solve (dynamic range)
    # ----------------------------------------

    src_range = max(src_white - src_black, 1e-6)
    ref_range = ref_white - ref_black

    contrast_ratio = (ref_range / src_range) - 1.0

    stat_contrast = (ref_contrast - src_contrast) * 0.2

    contrast = (contrast_ratio * 0.7) + stat_contrast

    contrast = np.clip(contrast, -1.5, 1.5)

    # ----------------------------------------
    # Return normalized values
    # ----------------------------------------

    return {
        "black_shift": float(black_shift),
        "white_shift": float(white_shift),
        "gamma": float(gamma),
        "contrast": float(contrast)
    }
