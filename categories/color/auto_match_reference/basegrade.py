import numpy as np


def get_luma(img):
    return 0.2126*img[:,:,2] + 0.7152*img[:,:,1] + 0.0722*img[:,:,0]


def apply_basegrade(src_img, ref_img):

    src = src_img.astype("float32")
    ref = ref_img.astype("float32")

    src_luma = get_luma(src)
    ref_luma = get_luma(ref)

    # ===============================
    # BLACK LEVEL
    # ===============================
    src_black = np.percentile(src_luma, 2)
    ref_black = np.percentile(ref_luma, 2)

    src = src - src_black + ref_black

    # ===============================
    # WHITE LEVEL
    # ===============================
    src_white = np.percentile(src_luma, 98)
    ref_white = np.percentile(ref_luma, 98)

    scale = (ref_white - ref_black) / (src_white - src_black + 1e-6)
    src = (src - ref_black) * scale + ref_black

    # ===============================
    # RE-LUMA
    # ===============================
    src_luma = get_luma(src)

    # ===============================
    # SHADOW
    # ===============================
    shadow_mask = src_luma < np.percentile(src_luma, 30)
    src[shadow_mask] += (np.mean(ref[shadow_mask]) - np.mean(src[shadow_mask])) * 0.6

    # ===============================
    # MIDTONE
    # ===============================
    mid_mask = (src_luma >= np.percentile(src_luma, 30)) & (src_luma <= np.percentile(src_luma, 70))
    src[mid_mask] += (np.mean(ref[mid_mask]) - np.mean(src[mid_mask])) * 0.4

    # ===============================
    # HIGHLIGHT
    # ===============================
    high_mask = src_luma > np.percentile(src_luma, 70)
    src[high_mask] += (np.mean(ref[high_mask]) - np.mean(src[high_mask])) * 0.3

    # ===============================
    # GAMMA
    # ===============================
    src_mid = np.median(src_luma)
    ref_mid = np.median(ref_luma)

    gamma = np.clip(ref_mid / (src_mid + 1e-6), 0.85, 1.15)
    src = np.power(src / 255.0, gamma) * 255.0

    # ===============================
    # FINAL CONTRAST BOOST
    # ===============================
    mean = np.mean(src)
    src = (src - mean) * 1.15 + mean

    return np.clip(src, 0, 255).astype("uint8")
