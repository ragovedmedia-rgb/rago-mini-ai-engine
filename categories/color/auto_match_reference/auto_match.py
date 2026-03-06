import numpy as np
from PIL import Image
import base64
import io

# NEW IMPORT (REAL COLOR TRANSFER)
from .color_transfer import color_transfer


# ==============================
# BASE64 IMAGE → NUMPY
# ==============================

def decode_base64_image(data):

    if "," in data:
        data = data.split(",")[1]

    img_bytes = base64.b64decode(data)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    img = img.resize((220,220))

    return np.asarray(img) / 255.0


# ==============================
# IMAGE ANALYSIS
# ==============================

def analyze_image(img):

    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]

    luma = 0.2126*r + 0.7152*g + 0.0722*b

    shadow_mask = luma < 0.33
    mid_mask = (luma >= 0.33) & (luma <= 0.66)
    highlight_mask = luma > 0.66

    def avg(mask):
        if np.sum(mask) == 0:
            return np.array([0,0,0])
        return np.array([
            np.mean(r[mask]),
            np.mean(g[mask]),
            np.mean(b[mask])
        ])

    return {
        "shadow": avg(shadow_mask),
        "mid": avg(mid_mask),
        "highlight": avg(highlight_mask),
        "avg_luma": np.mean(luma),
        "avg_sat": np.mean(np.max(img,axis=2) - np.min(img,axis=2))
    }


# ==============================
# AUTO MATCH ENGINE
# ==============================

def auto_match(reference_base64, source_base64):

    # Decode original images
    ref_img = decode_base64_image(reference_base64)

    # Apply real LAB color transfer
    matched_img = color_transfer(reference_base64, source_base64)

    # Analyze images
    ref = analyze_image(ref_img)
    src = analyze_image(matched_img)

    sliders = {}

    # EXPOSURE
    exposure = (ref["avg_luma"] - src["avg_luma"]) * 200
    sliders["exposure"] = float(np.clip(exposure, -100, 100))

    # SATURATION
    sat = (ref["avg_sat"] - src["avg_sat"]) * 150
    sliders["saturation"] = float(np.clip(sat, -100, 100))

    # CONTRAST
    ref_contrast = ref["highlight"][0] - ref["shadow"][0]
    src_contrast = src["highlight"][0] - src["shadow"][0]

    contrast = (ref_contrast - src_contrast) * 120
    sliders["contrast"] = float(np.clip(contrast, -100, 100))

    # TEMPERATURE
    ref_temp = ref["mid"][0] - ref["mid"][2]
    src_temp = src["mid"][0] - src["mid"][2]

    temp = (ref_temp - src_temp) * 80
    sliders["temperature"] = float(np.clip(temp, -100, 100))

    # TINT
    ref_tint = ref["mid"][1] - (ref["mid"][0]+ref["mid"][2])/2
    src_tint = src["mid"][1] - (src["mid"][0]+src["mid"][2])/2

    tint = (src_tint - ref_tint) * 120
    sliders["tint"] = float(np.clip(tint, -100, 100))

    return sliders
