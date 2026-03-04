from .tone_curve import apply_tone_curve
from .white_balance import apply_white_balance
from .zone_match import apply_zone_match
from .matrix_solver import apply_matrix


def build_lut(sliders, wheels, size):

    lut = []

    for b in range(size):
        for g in range(size):
            for r in range(size):

                rr = r / (size - 1)
                gg = g / (size - 1)
                bb = b / (size - 1)

                # Tone adjustments
                rr, gg, bb = apply_tone_curve(rr, gg, bb, sliders)

                # Temperature & tint
                rr, gg, bb = apply_white_balance(rr, gg, bb, sliders)

                # Shadow / Mid / Highlight wheels
                rr, gg, bb = apply_zone_match(rr, gg, bb, wheels)

                # Final matrix transform
                rr, gg, bb = apply_matrix(rr, gg, bb)

                # Clamp
                rr = max(0.0, min(1.0, rr))
                gg = max(0.0, min(1.0, gg))
                bb = max(0.0, min(1.0, bb))

                lut.append((rr, gg, bb))

    return lut
