import numpy as np


def zone_harmony(src_img, ref_img):

    src = src_img.astype("float32")
    ref = ref_img.astype("float32")

    # ===============================
    # LUMINANCE CALCULATION
    # ===============================
    src_luma = 0.2126 * src[:, :, 2] + 0.7152 * src[:, :, 1] + 0.0722 * src[:, :, 0]
    ref_luma = 0.2126 * ref[:, :, 2] + 0.7152 * ref[:, :, 1] + 0.0722 * ref[:, :, 0]

    # ===============================
    # SOURCE ZONES
    # ===============================
    s_low = np.percentile(src_luma, 25)
    s_high = np.percentile(src_luma, 75)

    shadow_mask = src_luma < s_low
    mid_mask = (src_luma >= s_low) & (src_luma <= s_high)
    high_mask = src_luma > s_high

    # ===============================
    # REFERENCE ZONES (🔥 FIXED)
    # ===============================
    r_low = np.percentile(ref_luma, 25)
    r_high = np.percentile(ref_luma, 75)

    ref_shadow_mask = ref_luma < r_low
    ref_mid_mask = (ref_luma >= r_low) & (ref_luma <= r_high)
    ref_high_mask = ref_luma > r_high

    # ===============================
    # SAFE AVG FUNCTION
    # ===============================
    def avg(img, mask):
        if np.sum(mask) == 0:
            return np.array([0, 0, 0])
        return np.mean(img[mask], axis=0)

    # ===============================
    # AVERAGES
    # ===============================
    src_shadow = avg(src, shadow_mask)
    src_mid = avg(src, mid_mask)
    src_high = avg(src, high_mask)

    ref_shadow = avg(ref, ref_shadow_mask)
    ref_mid = avg(ref, ref_mid_mask)
    ref_high = avg(ref, ref_high_mask)

    # ===============================
    # APPLY SHIFTS (balanced)
    # ===============================
    shadow_shift = (ref_shadow - src_shadow) * 0.8
    mid_shift = (ref_mid - src_mid) * 0.5
    high_shift = (ref_high - src_high) * 0.3

    src[shadow_mask] += shadow_shift
    src[mid_mask] += mid_shift
    src[high_mask] += high_shift

    # ===============================
    # GAMMA CORRECTION (stable)
    # ===============================
    src_luma_new = 0.2126 * src[:, :, 2] + 0.7152 * src[:, :, 1] + 0.0722 * src[:, :, 0]

    src_mid_val = np.median(src_luma_new)
    ref_mid_val = np.median(ref_luma)

    gamma = np.clip(ref_mid_val / (src_mid_val + 1e-6), 0.85, 1.15)

    src = np.power(src / 255.0, gamma) * 255.0

    # ===============================
    # FINAL CLIP
    # ===============================
    return np.clip(src, 0, 255).astype("uint8")
