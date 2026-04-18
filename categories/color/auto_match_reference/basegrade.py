import numpy as np


def get_luma(img):
    return 0.2126 * img[:, :, 2] + 0.7152 * img[:, :, 1] + 0.0722 * img[:, :, 0]


def apply_basegrade(src_img, ref_img):

    src = src_img.astype("float32")
    ref = ref_img.astype("float32")

    src_luma = get_luma(src)
    ref_luma = get_luma(ref)

    # ===============================
    # BLACK / WHITE POINT
    # ===============================
    src_black, src_white = np.percentile(src_luma, [2, 98])
    ref_black, ref_white = np.percentile(ref_luma, [2, 98])

    src_norm = (src - src_black) / (src_white - src_black + 1e-6)
    src = src_norm * (ref_white - ref_black) + ref_black

    src = np.clip(src, 0, 255)

    # ===============================
    # LUMA AGAIN
    # ===============================
    src_luma = get_luma(src)

    s_low, s_high = np.percentile(src_luma, [25, 75])
    r_low, r_high = np.percentile(ref_luma, [25, 75])

    # masks
    shadow_mask = src_luma < s_low
    mid_mask = (src_luma >= s_low) & (src_luma <= s_high)
    high_mask = src_luma > s_high

    # ===============================
    # SAFE SHIFT (LUMA BASED)
    # ===============================
    def luma_shift(mask, strength):
        if np.sum(mask) == 0:
            return

        src_mean = np.mean(src_luma[mask])
        ref_mean = np.mean(ref_luma[mask])

        delta = (ref_mean - src_mean) * strength

        # apply ONLY as brightness (not RGB tint)
        src[mask] += delta

    luma_shift(shadow_mask, 0.6)
    luma_shift(mid_mask, 0.45)
    luma_shift(high_mask, 0.3)

    src = np.clip(src, 0, 255)

    # ===============================
    # GAMMA
    # ===============================
    src_mid = np.median(get_luma(src))
    ref_mid = np.median(ref_luma)

    gamma = np.clip(ref_mid / (src_mid + 1e-6), 0.9, 1.1)

    src = np.power(src / 255.0, gamma) * 255.0

    # ===============================
    # CONTRAST (SOFT)
    # ===============================
    src_mean = np.mean(src)
    ref_std = np.std(ref_luma)
    src_std = np.std(get_luma(src))

    contrast = np.clip(ref_std / (src_std + 1e-6), 0.9, 1.15)

    src = (src - src_mean) * contrast + src_mean

    return np.clip(src, 0, 255).astype("uint8")
