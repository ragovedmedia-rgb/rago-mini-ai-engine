import numpy as np

def solve_color_wheels(ref_img, src_img):

    ref = ref_img.astype("float32")
    src = src_img.astype("float32")

    ref_luma = 0.2126*ref[:,:,2] + 0.7152*ref[:,:,1] + 0.0722*ref[:,:,0]
    src_luma = 0.2126*src[:,:,2] + 0.7152*src[:,:,1] + 0.0722*src[:,:,0]

    s_low = np.percentile(src_luma,30)
    s_high = np.percentile(src_luma,70)

    shadow_mask = src_luma < s_low
    mid_mask = (src_luma>=s_low) & (src_luma<=s_high)
    high_mask = src_luma > s_high

    def avg(img,mask):
        if mask.sum()==0:
            return np.array([0,0,0])
        return np.mean(img[mask],axis=0)

    ref_shadow = avg(ref,shadow_mask)
    src_shadow = avg(src,shadow_mask)

    ref_mid = avg(ref,mid_mask)
    src_mid = avg(src,mid_mask)

    ref_high = avg(ref,high_mask)
    src_high = avg(src,high_mask)

    lift = (ref_shadow - src_shadow)/255
    gamma = (ref_mid - src_mid)/255
    gain = (ref_high - src_high)/255

    return {
        "lift": lift.tolist(),
        "gamma": gamma.tolist(),
        "gain": gain.tolist()
    }
