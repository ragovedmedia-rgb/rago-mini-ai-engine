import numpy as np
from .basegrade import apply_basegrade


def zone_harmony(src_img, ref_img):

    # ===============================
    # 1. BASE GRADE (TONE MATCH)
    # ===============================
    base = apply_basegrade(src_img, ref_img).astype("float32")
    ref = ref_img.astype("float32")

    # ===============================
    # 2. SAFE CONVERSION
    # ===============================
    import cv2

    base_uint8 = np.clip(base, 0, 255).astype("uint8")
    ref_uint8  = np.clip(ref, 0, 255).astype("uint8")

    base_lab = cv2.cvtColor(base_uint8, cv2.COLOR_BGR2LAB).astype("float32")
    ref_lab  = cv2.cvtColor(ref_uint8, cv2.COLOR_BGR2LAB).astype("float32")

    # ===============================
    # 3. SMART MIDTONE MASK (skin safe)
    # ===============================
    ref_l = ref_lab[:, :, 0]
    mask = (ref_l > 80) & (ref_l < 180)

    # ===============================
    # 4. SMART TEMPERATURE
    # ===============================
    if np.sum(mask) > 100:
        ref_temp = np.mean(ref_lab[:, :, 2][mask])
        base_temp = np.mean(base_lab[:, :, 2][mask])
    else:
        ref_temp = np.mean(ref_lab[:, :, 2])
        base_temp = np.mean(base_lab[:, :, 2])

    temp_shift = (ref_temp - base_temp) * 0.8
    temp_shift = np.clip(temp_shift, -25, 25)

    base_lab[:, :, 2] += temp_shift

    # ===============================
    # 5. SMART TINT
    # ===============================
    if np.sum(mask) > 100:
        ref_tint = np.mean(ref_lab[:, :, 1][mask])
        base_tint = np.mean(base_lab[:, :, 1][mask])
    else:
        ref_tint = np.mean(ref_lab[:, :, 1])
        base_tint = np.mean(base_lab[:, :, 1])

    tint_shift = (ref_tint - base_tint) * 0.7
    tint_shift = np.clip(tint_shift, -20, 20)

    base_lab[:, :, 1] += tint_shift

    # ===============================
    # 6. SATURATION MATCH
    # ===============================
    ref_sat = np.std(ref_lab[:, :, 1:3])
    base_sat = np.std(base_lab[:, :, 1:3])

    sat_scale = ref_sat / (base_sat + 1e-6)
    sat_scale = np.clip(sat_scale, 0.85, 1.25)

    base_lab[:, :, 1:3] = (base_lab[:, :, 1:3] - 128) * sat_scale + 128

    # ===============================
    # 7. LUMINANCE MATCH
    # ===============================
    ref_l = ref_lab[:, :, 0]
    base_l = base_lab[:, :, 0]

    l_scale = np.mean(ref_l) / (np.mean(base_l) + 1e-6)
    l_scale = np.clip(l_scale, 0.9, 1.1)

    base_lab[:, :, 0] = np.clip(base_lab[:, :, 0] * l_scale, 0, 255)

    # ===============================
    # 8. FINAL
    # ===============================
    base_lab = np.clip(base_lab, 0, 255)
    result = cv2.cvtColor(base_lab.astype("uint8"), cv2.COLOR_LAB2BGR)

    return np.clip(result, 0, 255).astype("uint8")
