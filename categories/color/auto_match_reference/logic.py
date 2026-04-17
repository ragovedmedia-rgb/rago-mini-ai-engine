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
        # MATCH SIZE (CRITICAL FIX)
        # ===============================

        h, w = src_img.shape[:2]
        ref_img = cv2.resize(ref_img, (w, h))

        # ===============================
        # CONVERT TO LAB
        # ===============================

        ref_lab = cv2.cvtColor(ref_img, cv2.COLOR_BGR2LAB)
        src_lab = cv2.cvtColor(src_img, cv2.COLOR_BGR2LAB)

        # ===============================
        # SPLIT LUMA ZONES (🔥 MAIN FIX)
        # ===============================

        src_l = src_lab[:, :, 0]

        shadow_mask = src_l < 85
        mid_mask = (src_l >= 85) & (src_l <= 170)
        highlight_mask = src_l > 170

        result_lab = src_lab.copy().astype(np.float32)

        def match_zone(mask):
            if np.sum(mask) == 0:
                return

            src_vals = src_lab[mask]
            ref_vals = ref_lab[mask]

            src_mean = np.mean(src_vals, axis=0)
            ref_mean = np.mean(ref_vals, axis=0)

            src_std = np.std(src_vals, axis=0)
            ref_std = np.std(ref_vals, axis=0)

            src_std = np.where(src_std == 0, 1, src_std)

            result_lab[mask] = (src_vals - src_mean) * (ref_std / src_std) + ref_mean

        # Apply zones
        match_zone(shadow_mask)
        match_zone(mid_mask)
        match_zone(highlight_mask)

        result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)

        # ===============================
        # BACK TO BGR
        # ===============================

        result_bgr = cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)

        # ===============================
        # CALCULATE SLIDERS (SMART)
        # ===============================

        ref_mean = cv2.mean(ref_img)[:3]
        src_mean = cv2.mean(src_img)[:3]

        exposure = (ref_mean[0] - src_mean[0]) * 0.6
        contrast = (ref_mean[1] - src_mean[1]) * 0.5
        saturation = (ref_mean[2] - src_mean[2]) * 0.5

        # Slight boost for cinematic feel
        exposure *= 1.1
        contrast *= 1.2
        saturation *= 1.1

        sliders = {
            "exposure": float(exposure),
            "contrast": float(contrast),
            "saturation": float(saturation),
            "temperature": 0.0,
            "tint": 0.0
        }

        # ===============================
        # RETURN FINAL
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
