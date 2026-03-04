from .tone_curve import apply_tone_curve
from .white_balance import apply_white_balance
from .zone_match import apply_zone_match
from .matrix_solver import apply_matrix


def build_lut(sliders=None, wheels=None, size=33):

    # Safety defaults
    sliders = sliders or {}
    wheels = wheels or []

    lut = []

    for b in range(size):
        for g in range(size):
            for r in range(size):

                # Normalize RGB
                rr = r / (size - 1)
                gg = g / (size - 1)
                bb = b / (size - 1)

                # -----------------------------
                # Tone adjustments (Exposure / Contrast / Sat)
                # -----------------------------
                rr, gg, bb = apply_tone_curve(rr, gg, bb, sliders)

                # -----------------------------
                # White balance (Temp / Tint)
                # -----------------------------
                rr, gg, bb = apply_white_balance(rr, gg, bb, sliders)

                # -----------------------------
                # Color wheels (Shadow/Mid/Highlight)
                # -----------------------------
                rr, gg, bb = apply_zone_match(rr, gg, bb, wheels)

                # -----------------------------
                # Final matrix color transform
                # -----------------------------
                rr, gg, bb = apply_matrix(rr, gg, bb)

                # -----------------------------
                # Clamp values
                # -----------------------------
                rr = max(0.0, min(1.0, rr))
                gg = max(0.0, min(1.0, gg))
                bb = max(0.0, min(1.0, bb))

                lut.append((rr, gg, bb))

    return lut
