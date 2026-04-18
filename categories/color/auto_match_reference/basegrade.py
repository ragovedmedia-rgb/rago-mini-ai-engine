import numpy as np


def get_luma(img):
    return 0.2126 * img[:, :, 2] + 0.7152 * img[:, :, 1] + 0.0722 * img[:, :, 0]


def apply_basegrade(src_img, ref_img):

    src = src_img.astype("float32")
    ref = ref_img.astype("float32")

    # ===============================
    # LUMA
    # ===============================
    src_luma = get_luma(src)
    ref_luma = get_luma(ref)

    # ===============================
    # BLACK & WHITE POINT MATCH (SAFE)
    # ===============================
    src_black = np.percentile(src_luma, 2)
    src_white = np.percentile(src_luma, 98)

    ref_black = np.percentile(ref_luma, 2)
    ref_white = np.percentile(ref_luma, 98)

    # normalize src → 0–1
    src_norm = (src - src_black) / (src_white - src_black + 1e-6)

    # scale to ref range
    src = src_norm * (ref_white - ref_black) + ref_black

    # ===============================
    # RE-CALCULATE LUMA
    # ===============================
    src_luma = get_luma(src)

    # ===============================
    # SHADOW / MID / HIGHLIGHT MATCH
    # ===============================
    s_low = np.percentile(src_luma, 25)
    s_high = np.percentile(src_luma, 75)

    r_low = np.percentile(ref_luma, 25)
    r_high = np.percentile(ref_luma, 75)

    shadow_mask = src_luma < s_low
    mid_mask = (src_luma >= s_low) & (src_luma <= s_high)
    high_mask = src_luma > s_high

    def shift(mask, strength):
        if np.sum(mask) == 0:
            return

        src_mean = np.mean(src[mask])
        ref_mean = np.mean(ref[mask])

        src[mask] += (ref_mean - src_mean) * strength

    # tuned strengths
    shift(shadow_mask, 0.7)
    shift(mid_mask, 0.5)
    shift(high_mask, 0.35)

    # ===============================
    # GAMMA (MID ALIGN)
    # ===============================
    src_mid = np.median(get_luma(src))
    ref_mid = np.median(ref_luma)

    gamma = np.clip(ref_mid / (src_mid + 1e-6), 0.9, 1.1)

    src = np.power(np.clip(src / 255.0, 0, 1), gamma) * 255.0

    # ===============================
    # CONTRAST (CONTROLLED)
    # ===============================
    src_mean = np.mean(src)
    ref_contrast = np.std(ref_luma)
    src_contrast = np.std(get_luma(src))

    contrast_scale = ref_contrast / (src_contrast + 1e-6)
    contrast_scale = np.clip(contrast_scale, 0.9, 1.2)

    src = (src - src_mean) * contrast_scale + src_mean

    # ===============================
    # FINAL CLIP
    # ===============================
    return np.clip(src, 0, 255).astype("uint8")
