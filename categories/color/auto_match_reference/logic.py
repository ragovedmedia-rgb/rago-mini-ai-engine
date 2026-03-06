import base64
import cv2
import numpy as np


def run(data):

    reference = data.get("reference")
    source = data.get("source")

    if not reference or not source:
        return {
            "success": False,
            "error": "Missing reference or source image"
        }

    # ===============================
    # DECODE BASE64 IMAGES
    # ===============================

    ref_bytes = base64.b64decode(reference.split(",")[1])
    src_bytes = base64.b64decode(source.split(",")[1])

    ref_np = np.frombuffer(ref_bytes, np.uint8)
    src_np = np.frombuffer(src_bytes, np.uint8)

    ref_img = cv2.imdecode(ref_np, cv2.IMREAD_COLOR)
    src_img = cv2.imdecode(src_np, cv2.IMREAD_COLOR)

    # ===============================
    # SIMPLE COLOR MATCH
    # ===============================

    ref_mean = cv2.mean(ref_img)[:3]
    src_mean = cv2.mean(src_img)[:3]

    exposure = (ref_mean[0] - src_mean[0]) * 0.4
    saturation = (ref_mean[1] - src_mean[1]) * 0.4
    contrast = (ref_mean[2] - src_mean[2]) * 0.4

    sliders = {
        "exposure": float(exposure),
        "contrast": float(contrast),
        "saturation": float(saturation),
        "temperature": 0,
        "tint": 0
    }

    return {
        "success": True,
        "sliders": sliders
    }
