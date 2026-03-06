import numpy as np

def zone_harmony(src_img, ref_img):

    src = src_img.astype("float32")
    ref = ref_img.astype("float32")

    src_luma = 0.2126*src[:,:,2] + 0.7152*src[:,:,1] + 0.0722*src[:,:,0]
    ref_luma = 0.2126*ref[:,:,2] + 0.7152*ref[:,:,1] + 0.0722*ref[:,:,0]

    shadow_mask = src_luma < 85
    mid_mask = (src_luma >= 85) & (src_luma <=170)
    high_mask = src_luma > 170

    def avg_color(img,mask):
        if np.sum(mask)==0:
            return np.array([0,0,0])
        return np.mean(img[mask],axis=0)

    src_shadow = avg_color(src,shadow_mask)
    ref_shadow = avg_color(ref,shadow_mask)

    src_mid = avg_color(src,mid_mask)
    ref_mid = avg_color(ref,mid_mask)

    src_high = avg_color(src,high_mask)
    ref_high = avg_color(ref,high_mask)

    shadow_shift = ref_shadow - src_shadow
    mid_shift = ref_mid - src_mid
    high_shift = ref_high - src_high

    src[shadow_mask] += shadow_shift
    src[mid_mask] += mid_shift
    src[high_mask] += high_shift

    return np.clip(src,0,255).astype("uint8")
