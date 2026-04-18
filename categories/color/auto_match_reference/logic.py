import base64
import cv2
import numpy as np


def decode_image(base64_string):
    try:
        img_data = base64.b64decode(base64_string.split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception:
        return None


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
        # DECODE IMAGES
        # ===============================

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
        # COLOR TRANSFER (MEAN + STD)
        # ===============================

        ref_mean, ref_std = cv2.meanStdDev(ref_lab)
        src_mean, src_std = cv2.meanStdDev(src_lab)

        ref_mean = ref_mean.flatten()
        ref_std = ref_std.flatten()
        src_mean = src_mean.flatten()
        src_std = src_std.flatten()

        # avoid divide by zero
        src_std = np.where(src_std == 0, 1, src_std)

        # transfer
        result_lab = (src_lab - src_mean) * (ref_std / src_std) + ref_mean
        result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)

        # ===============================
        # BACK TO BGR
        # ===============================

        result_bgr = cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)

        # ===============================
        # IMAGE OUTPUT ADD
        # ===============================
        _, buffer = cv2.imencode('.jpg', result_bgr)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        image_output = f"data:image/jpeg;base64,{img_base64}"

        # ===============================
        # 🎯 BETTER SLIDER CALCULATION
        # ===============================

        # Luminance (brightness)
        ref_l = ref_lab[:, :, 0]
        src_l = src_lab[:, :, 0]

        exposure = np.mean(ref_l - src_l) * 0.8

        # Contrast (std difference)
        contrast = (np.std(ref_l) - np.std(src_l)) * 1.5

        # Saturation (color channels spread)
        ref_ab = ref_lab[:, :, 1:3]
        src_ab = src_lab[:, :, 1:3]

        sat_ref = np.std(ref_ab)
        sat_src = np.std(src_ab)

        saturation = (sat_ref - sat_src) * 1.2

        # Temperature (blue-yellow axis)
        temperature = np.mean(ref_lab[:, :, 2] - src_lab[:, :, 2]) * 0.3

        # Tint (green-magenta axis)
        tint = np.mean(ref_lab[:, :, 1] - src_lab[:, :, 1]) * 0.3

        # ===============================
        # FINAL NORMALIZATION (IMPORTANT)
        # ===============================

        sliders = {
            "exposure": float(np.clip(exposure, -100, 100)),
            "contrast": float(np.clip(contrast, -100, 100)),
            "saturation": float(np.clip(saturation, -100, 100)),
            "temperature": float(np.clip(temperature, -100, 100)),
            "tint": float(np.clip(tint, -100, 100))
        }

        return {
    "success": True,
    "sliders": sliders,
    "image": image_output
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
