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

    try:

        # ===============================
        # DECODE BASE64 IMAGES
        # ===============================

        ref_bytes = base64.b64decode(reference.split(",")[1])
        src_bytes = base64.b64decode(source.split(",")[1])

        ref_np = np.frombuffer(ref_bytes, np.uint8)
        src_np = np.frombuffer(src_bytes, np.uint8)

        ref_img = cv2.imdecode(ref_np, cv2.IMREAD_COLOR)
        src_img = cv2.imdecode(src_np, cv2.IMREAD_COLOR)

        if ref_img is None or src_img is None:
            return {
                "success": False,
                "error": "Image decode failed"
            }

        # ===============================
        # MATCH IMAGE SIZE
        # ===============================

        h, w = src_img.shape[:2]
        ref_img = cv2.resize(ref_img, (w, h))

        # ===============================
        # CONVERT TO LAB COLOR SPACE
        # ===============================

        ref_lab = cv2.cvtColor(ref_img, cv2.COLOR_BGR2LAB)
        src_lab = cv2.cvtColor(src_img, cv2.COLOR_BGR2LAB)

        # ===============================
        # CALCULATE COLOR STATISTICS
        # ===============================

        ref_mean = cv2.mean(ref_lab)[:3]
        src_mean = cv2.mean(src_lab)[:3]

        # ===============================
# ADVANCED COLOR MATCH (STD + MEAN)
# ===============================

ref_std = np.std(ref_lab, axis=(0,1))
src_std = np.std(src_lab, axis=(0,1))

# Avoid divide by zero
src_std = np.where(src_std == 0, 1, src_std)

# Apply color transfer
result_lab = (src_lab - src_mean) * (ref_std / src_std) + ref_mean

# Clip values
result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)

# ===============================
# CALCULATE SLIDERS FROM RESULT
# ===============================

diff = cv2.mean(result_lab.astype(np.float32) - src_lab.astype(np.float32))

exposure = diff[0] * 0.4
contrast = diff[1] * 0.3
saturation = diff[2] * 0.3

        sliders = {
            "exposure": float(exposure),
            "contrast": float(contrast),
            "saturation": float(saturation),
            "temperature": 0.0,
            "tint": 0.0
        }

        # ===============================
        # RETURN RESULT
        # ===============================

        return {
            "success": True,
            "sliders": sliders
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
