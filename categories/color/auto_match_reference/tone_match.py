import numpy as np
from .utils import compute_luma

def solve_tone(ref_img, src_img):

    ref_luma = compute_luma(ref_img)
    src_luma = compute_luma(src_img)

    shadow_ref = np.mean(ref_luma[ref_luma < 85])
    shadow_src = np.mean(src_luma[src_luma < 85])

    highlight_ref = np.mean(ref_luma[ref_luma > 170])
    highlight_src = np.mean(src_luma[src_luma > 170])

    shadow_shift = (shadow_ref - shadow_src) / 255
    highlight_shift = (highlight_ref - highlight_src) / 255

    return {
        "shadow_shift": float(shadow_shift),
        "highlight_shift": float(highlight_shift)
    }
