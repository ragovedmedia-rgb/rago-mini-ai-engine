import cv2
import numpy as np


def histogram_match(src_img, ref_img):

    src_yuv = cv2.cvtColor(src_img, cv2.COLOR_BGR2YUV)
    ref_yuv = cv2.cvtColor(ref_img, cv2.COLOR_BGR2YUV)

    src_y = src_yuv[:,:,0].astype("float32")
    ref_y = ref_yuv[:,:,0].astype("float32")

    # normalize dynamic range
    src_y = cv2.normalize(src_y, None, 0, 255, cv2.NORM_MINMAX)
    ref_y = cv2.normalize(ref_y, None, 0, 255, cv2.NORM_MINMAX)

    src_hist,_ = np.histogram(src_y.flatten(),256,[0,256])
    ref_hist,_ = np.histogram(ref_y.flatten(),256,[0,256])

    src_cdf = src_hist.cumsum()
    ref_cdf = ref_hist.cumsum()

    src_cdf = src_cdf / src_cdf[-1]
    ref_cdf = ref_cdf / ref_cdf[-1]

    lookup = np.zeros(256)

    for i in range(256):
        diff = np.abs(ref_cdf - src_cdf[i])
        lookup[i] = np.argmin(diff)

    lookup = lookup.astype("uint8")

    matched = cv2.LUT(src_y.astype("uint8"), lookup)

    src_yuv[:,:,0] = matched

    result = cv2.cvtColor(src_yuv, cv2.COLOR_YUV2BGR)

    return result
