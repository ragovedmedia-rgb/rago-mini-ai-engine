import numpy as np


# ===============================
# LUMINANCE FUNCTION
# ===============================
def get_luma(img):
    return 0.2126*img[:,:,2] + 0.7152*img[:,:,1] + 0.0722*img[:,:,0]


# ===============================
# BLACK LEVEL
# ===============================
def match_black(src, ref):
    src_l = get_luma(src)
    ref_l = get_luma(ref)

    src_black = np.percentile(src_l, 2)
    ref_black = np.percentile(ref_l, 2)

    return src - src_black + ref_black


# ===============================
# WHITE LEVEL
# ===============================
def match_white(src, ref):
    src_l = get_luma(src)
    ref_l = get_luma(ref)

    src_black = np.percentile(src_l, 2)
    src_white = np.percentile(src_l, 98)

    ref_black = np.percentile(ref_l, 2)
    ref_white = np.percentile(ref_l, 98)

    scale = (ref_white - ref_black) / (src_white - src_black + 1e-6)

    return (src - ref_black) * scale + ref_black


# ===============================
# SHADOW
# ===============================
def match_shadow(src, ref):
    src_l = get_luma(src)

    mask = src_l < np.percentile(src_l, 30)

    shift = (np.mean(ref[mask]) - np.mean(src[mask])) * 0.5
    src[mask] += shift

    return src


# ===============================
# GAMMA
# ===============================
def match_gamma(src, ref):
    src_l = get_luma(src)
    ref_l = get_luma(ref)

    src_mid = np.median(src_l)
    ref_mid = np.median(ref_l)

    gamma = np.clip(ref_mid / (src_mid + 1e-6), 0.85, 1.15)

    return np.power(src / 255.0, gamma) * 255.0


# ===============================
# HIGHLIGHT
# ===============================
def match_highlight(src, ref):
    src_l = get_luma(src)

    mask = src_l > np.percentile(src_l, 70)

    shift = (np.mean(ref[mask]) - np.mean(src[mask])) * 0.3
    src[mask] += shift

    return src


# ===============================
# MASTER FUNCTION
# ===============================
def apply_basegrade(src_img, ref_img):

    src = src_img.astype("float32")
    ref = ref_img.astype("float32")

    src = match_black(src, ref)
    src = match_white(src, ref)
    src = match_shadow(src, ref)
    src = match_gamma(src, ref)
    src = match_highlight(src, ref)

    return np.clip(src, 0, 255).astype("uint8")
