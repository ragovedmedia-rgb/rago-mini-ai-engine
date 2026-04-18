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
    base_lab = cv2.cvtColor(base.astype("uint8"), cv2.COLOR_BGR2LAB).astype("float32")
    ref_lab = cv2.cvtColor(ref.astype("uint8"), cv2.COLOR_BGR2LAB).astype("float32")

    # ===============================
    # TEMPERATURE (B channel)
    # ===============================
    temp_shift = np.mean(ref_lab[:,:,2] - base_lab[:,:,2]) * 0.6
    base_lab[:,:,2] += temp_shift

    # ===============================
    # TINT (A channel)
    # ===============================
    tint_shift = np.mean(ref_lab[:,:,1] - base_lab[:,:,1]) * 0.5
    base_lab[:,:,1] += tint_shift

    # ===============================
    # SATURATION
    # ===============================
    base_lab[:,:,1:3] = (base_lab[:,:,1:3] - 128) * 1.25 + 128

    # ===============================
    # BACK TO BGR
    # ===============================
    result = cv2.cvtColor(base_lab.astype("uint8"), cv2.COLOR_LAB2BGR)

    return np.clip(result, 0, 255).astype("uint8")
