import cv2
import numpy as np

def histogram_match(src_img, ref_img):

    src_yuv = cv2.cvtColor(src_img, cv2.COLOR_BGR2YUV)
    ref_yuv = cv2.cvtColor(ref_img, cv2.COLOR_BGR2YUV)

    src_y = src_yuv[:,:,0].astype("float32")
    ref_y = ref_yuv[:,:,0].astype("float32")

    # -------- BLACK POINT NORMALIZATION --------

    src_black = np.percentile(src_y,1)
    src_white = np.percentile(src_y,99)

    src_y = (src_y - src_black) / (src_white - src_black + 1e-6) * 255
    src_y = np.clip(src_y,0,255)

    # -------- HISTOGRAM MATCH --------

    src_hist,_ = np.histogram(src_y.flatten(),256,[0,256])
    ref_hist,_ = np.histogram(ref_y.flatten(),256,[0,256])

    src_cdf = src_hist.cumsum()
    ref_cdf = ref_hist.cumsum()

    src_cdf = src_cdf / src_cdf[-1]
    ref_cdf = ref_cdf / ref_cdf[-1]

    lookup = np.zeros(256)

    for i in range(256):
        lookup[i] = np.argmin(np.abs(ref_cdf - src_cdf[i]))

    lookup = lookup * 0.85 + np.arange(256) * 0.15

    matched = cv2.LUT(src_y.astype("uint8"), lookup.astype("uint8"))

    src_yuv[:,:,0] = matched

    return cv2.cvtColor(src_yuv, cv2.COLOR_YUV2BGR)
