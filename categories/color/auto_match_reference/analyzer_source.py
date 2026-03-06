import cv2
import numpy as np


def analyze_source(img):

    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    l, a, b = cv2.split(lab)

    luma = l.astype("float32")

    # -----------------------------
    # Level analysis
    # -----------------------------

    black = np.percentile(luma, 2)
    white = np.percentile(luma, 98)
    mid = np.median(luma)

    brightness = np.mean(luma)
    contrast = white - black

    luma_std = np.std(luma)

    # -----------------------------
    # Saturation strength
    # -----------------------------

    a_f = a.astype("float32")
    b_f = b.astype("float32")

    chroma = np.sqrt(a_f**2 + b_f**2)

    saturation = np.mean(chroma)

    # -----------------------------
    # Temperature / Tint estimate
    # -----------------------------

    temperature = np.mean(b_f)
    tint = np.mean(a_f)

    # -----------------------------
    # RGB channel balance
    # -----------------------------

    bgr_mean = np.mean(img, axis=(0, 1))

    blue_mean = float(bgr_mean[0])
    green_mean = float(bgr_mean[1])
    red_mean = float(bgr_mean[2])

    # -----------------------------
    # Final metrics
    # -----------------------------

    return {
        "black": float(black),
        "white": float(white),
        "mid": float(mid),
        "brightness": float(brightness),
        "contrast": float(contrast),
        "luma_std": float(luma_std),
        "saturation": float(saturation),
        "temperature": float(temperature),
        "tint": float(tint),
        "red_mean": red_mean,
        "green_mean": green_mean,
        "blue_mean": blue_mean
    }
