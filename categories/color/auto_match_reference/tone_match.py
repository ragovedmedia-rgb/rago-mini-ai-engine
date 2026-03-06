import cv2
import numpy as np


def solve_tone(ref_img, src_img):

    src_lab = cv2.cvtColor(src_img, cv2.COLOR_BGR2LAB)
    ref_lab = cv2.cvtColor(ref_img, cv2.COLOR_BGR2LAB)

    src_l = src_lab[:, :, 0].astype("float32")
    ref_l = ref_lab[:, :, 0].astype("float32")

    # Percentile tone points
    src_p = np.percentile(src_l, [5, 25, 50, 75, 95])
    ref_p = np.percentile(ref_l, [5, 25, 50, 75, 95])

    # tone difference
    tone_shift = ref_p - src_p

    shadow_shift = tone_shift[0]
    midtone_shift = tone_shift[2]
    highlight_shift = tone_shift[4]

    contrast_shift = (ref_p[4] - ref_p[0]) - (src_p[4] - src_p[0])

    return {
        "shadow": float(shadow_shift),
        "mid": float(midtone_shift),
        "highlight": float(highlight_shift),
        "contrast": float(contrast_shift)
    }
