import numpy as np
from .utils import compute_luma

def analyze_source(img):

    luma = compute_luma(img)

    black = np.percentile(luma,5)
    white = np.percentile(luma,95)
    mid = np.median(luma)

    contrast = white - black
    brightness = np.mean(luma)

    return {
        "black": float(black),
        "white": float(white),
        "mid": float(mid),
        "contrast": float(contrast),
        "brightness": float(brightness)
    }
