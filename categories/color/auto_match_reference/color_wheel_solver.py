import numpy as np


def compute_luma(img):

    return (
        0.2126 * img[:, :, 2] +
        0.7152 * img[:, :, 1] +
        0.0722 * img[:, :, 0]
    )


def avg_color(img, mask):

    if np.sum(mask) == 0:
        return np.array([0, 0, 0], dtype="float32")

    return np.mean(img[mask], axis=0)


def color_wheel_solver(ref_img, src_img):

    ref = ref_img.astype("float32")
    src = src_img.astype("float32")

    ref_luma = compute_luma(ref)
    src_luma = compute_luma(src)

    # adaptive zones
    s_low = np.percentile(src_luma, 30)
    s_high = np.percentile(src_luma, 70)

    shadow_mask = src_luma < s_low
    mid_mask = (src_luma >= s_low) & (src_luma <= s_high)
    high_mask = src_luma > s_high

    # reference zones
    ref_shadow = avg_color(ref, shadow_mask)
    ref_mid = avg_color(ref, mid_mask)
    ref_high = avg_color(ref, high_mask)

    src_shadow = avg_color(src, shadow_mask)
    src_mid = avg_color(src, mid_mask)
    src_high = avg_color(src, high_mask)

    # wheel solve
    lift = (ref_shadow - src_shadow) / 255.0
    gamma = (ref_mid - src_mid) / 255.0
    gain = (ref_high - src_high) / 255.0

    # brightness
    ref_mean = np.mean(ref_luma)
    src_mean = np.mean(src_luma)

    brightness = (ref_mean - src_mean) / 255.0

    # contrast
    ref_std = np.std(ref_luma)
    src_std = np.std(src_luma)

    contrast = (ref_std - src_std) / 255.0

    return {
        "lift": lift.tolist(),
        "gamma": gamma.tolist(),
        "gain": gain.tolist(),
        "brightness": float(brightness),
        "contrast": float(contrast)
    }
