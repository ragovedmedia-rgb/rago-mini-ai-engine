import numpy as np
from .basegrade import apply_basegrade


def zone_harmony(src_img, ref_img):

    # ===============================
    # BASE GRADE (FIRST)
    # ===============================
    base = apply_basegrade(src_img, ref_img).astype("float32")
    ref = ref_img.astype("float32")

    # ===============================
    # LAB COLOR SPACE
    # ===============================
    import cv2
    base_uint8 = np.clip(base, 0, 255).astype("uint8")
    ref_uint8  = np.clip(ref, 0, 255).astype("uint8")

    base_lab = cv2.cvtColor(base_uint8, cv2.COLOR_BGR2LAB).astype("float32")
    ref_lab  = cv2.cvtColor(ref_uint8, cv2.COLOR_BGR2LAB).astype("float32")
    # ===============================
    # TEMPERATURE (B channel)
    # ===============================
    temp_shift = np.clip(np.mean(ref_lab[:,:,2] - base_lab[:,:,2]) * 0.6, -20, 20)
    base_lab[:,:,2] += temp_shift

    # ===============================
    # TINT (A channel)
    # ===============================
    tint_shift = np.clip(np.mean(ref_lab[:,:,1] - base_lab[:,:,1]) * 0.5, -20, 20)
    base_lab[:,:,1] += tint_shift

    # ===============================
    # SATURATION MATCH (REFERENCE BASED)
    # ===============================
    ref_sat = np.std(ref_lab[:,:,1:3])
    base_sat = np.std(base_lab[:,:,1:3])

    sat_scale = np.clip(sat_scale, 0.85, 1.25)

    # clamp to avoid over boost
    sat_scale = np.clip(sat_scale, 0.8, 1.3)

    base_lab[:,:,1:3] = (base_lab[:,:,1:3] - 128) * sat_scale + 128

    # ===============================
    # BACK TO BGR
    # ===============================
    result = cv2.cvtColor(base_lab.astype("uint8"), cv2.COLOR_LAB2BGR)

    return np.clip(result, 0, 255).astype("uint8")
