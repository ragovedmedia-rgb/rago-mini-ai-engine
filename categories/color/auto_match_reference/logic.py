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
        # SIMPLE COLOR MATCH LOGIC
        # ===============================

        exposure = (ref_mean[0] - src_mean[0]) * 0.5
        contrast = (ref_mean[1] - src_mean[1]) * 0.3
        saturation = (ref_mean[2] - src_mean[2]) * 0.3

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
