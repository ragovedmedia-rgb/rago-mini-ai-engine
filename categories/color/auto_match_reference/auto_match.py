from .accurate_match import accurate_match
import numpy as np

def auto_match(ref_img, src_img):

    matched = accurate_match(src_img, ref_img)

    ref_mean = np.mean(ref_img)
    src_mean = np.mean(matched)

    exposure = (ref_mean - src_mean) * 0.02

    ref_std = np.std(ref_img)
    src_std = np.std(matched)

    contrast = (ref_std - src_std) * 0.02

    saturation = 0

    sliders = {
        "exposure": float(exposure),
        "contrast": float(contrast),
        "saturation": float(saturation),
        "temperature": 0,
        "tint": 0
    }

    return sliders
