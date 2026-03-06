import numpy as np


def zone_harmony(src_img, ref_img):

    src = src_img.astype("float32")
    ref = ref_img.astype("float32")

    # luminance
    src_luma = 0.2126*src[:,:,2] + 0.7152*src[:,:,1] + 0.0722*src[:,:,0]
    ref_luma = 0.2126*ref[:,:,2] + 0.7152*ref[:,:,1] + 0.0722*ref[:,:,0]

    # adaptive zones
    s_low = np.percentile(src_luma, 25)
    s_high = np.percentile(src_luma, 75)

    shadow_mask = src_luma < s_low
    mid_mask = (src_luma >= s_low) & (src_luma <= s_high)
    high_mask = src_luma > s_high

    def avg(img,mask):
        if np.sum(mask)==0:
            return np.array([0,0,0])
        return np.mean(img[mask],axis=0)

    src_shadow = avg(src,shadow_mask)
    ref_shadow = avg(ref,shadow_mask)

    src_mid = avg(src,mid_mask)
    ref_mid = avg(ref,mid_mask)

    src_high = avg(src,high_mask)
    ref_high = avg(ref,high_mask)

    # stronger shadow correction
    shadow_shift = (ref_shadow - src_shadow) * 0.9
    mid_shift = (ref_mid - src_mid) * 0.55
    high_shift = (ref_high - src_high) * 0.35

    src[shadow_mask] += shadow_shift
    src[mid_mask] += mid_shift
    src[high_mask] += high_shift

    # gamma correction for shadow depth
    src_luma_new = 0.2126*src[:,:,2] + 0.7152*src[:,:,1] + 0.0722*src[:,:,0]
    ref_mid = np.median(ref_luma)
    src_mid = np.median(src_luma_new)

    gamma = ref_mid / (src_mid + 1e-6)

    src = np.power(src/255.0, gamma) * 255.0

    return np.clip(src,0,255).astype("uint8")
