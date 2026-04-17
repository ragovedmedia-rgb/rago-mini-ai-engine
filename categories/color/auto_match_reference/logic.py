import base64
import cv2
import numpy as np


def decode_image(base64_string):
    img_data = base64.b64decode(base64_string.split(",")[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def run(data):

    reference = data.get("reference")
    source = data.get("source")

    if not reference or not source:
        return {
            "success": False,
            "error": "Missing reference or source image"
        }

    try:

        ref_img = decode_image(reference)
        src_img = decode_image(source)

        if ref_img is None or src_img is None:
            return {
                "success": False,
                "error": "Image decode failed"
            }

        # ===============================
        # MATCH SIZE
        # ===============================

        h, w = src_img.shape[:2]
        ref_img = cv2.resize(ref_img, (w, h))

        # ===============================
        # LAB CONVERSION
        # ===============================

        ref_lab = cv2.cvtColor(ref_img, cv2.COLOR_BGR2LAB).astype(np.float32)
        src_lab = cv2.cvtColor(src_img, cv2.COLOR_BGR2LAB).astype(np.float32)

        # ===============================
        # FULL IMAGE COLOR TRANSFER (FIXED)
        # ===============================

        ref_mean, ref_std = cv2.meanStdDev(ref_lab)
        src_mean, src_std = cv2.meanStdDev(src_lab)

        ref_mean = ref_mean.flatten()
        ref_std = ref_std.flatten()
        src_mean = src_mean.flatten()
        src_std = src_std.flatten()

        src_std = np.where(src_std == 0, 1, src_std)

        result_lab = (src_lab - src_mean) * (ref_std / src_std) + ref_mean

        result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)

        # ===============================
        # BACK TO BGR
        # ===============================

        result_bgr = cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)

        # ===============================
        # SLIDER CALCULATION (BASED ON RESULT)
        # ===============================

        diff = cv2.mean(result_bgr.astype(np.float32) - src_img.astype(np.float32))

        exposure = diff[0] * 0.6
        contrast = diff[1] * 0.6
        saturation = diff[2] * 0.6

        # Cinematic boost
        contrast *= 1.3
        saturation *= 1.2

        sliders = {
            "exposure": float(exposure),
            "contrast": float(contrast),
            "saturation": float(saturation),
            "temperature": float((diff[2] - diff[0]) * 0.2),
            "tint": float((diff[1] - diff[2]) * 0.2)
        }

        return {
            "success": True,
            "sliders": sliders
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
