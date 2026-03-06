import cv2
import numpy as np

def lab_transfer(src_img, ref_img):

    src_lab = cv2.cvtColor(src_img, cv2.COLOR_BGR2LAB).astype("float32")
    ref_lab = cv2.cvtColor(ref_img, cv2.COLOR_BGR2LAB).astype("float32")

    src_mean, src_std = cv2.meanStdDev(src_lab)
    ref_mean, ref_std = cv2.meanStdDev(ref_lab)

    src_mean = src_mean.flatten()
    src_std = src_std.flatten()
    ref_mean = ref_mean.flatten()
    ref_std = ref_std.flatten()

    l,a,b = cv2.split(src_lab)

    l = ((l - src_mean[0]) * (ref_std[0] / (src_std[0] + 1e-6))) + ref_mean[0]
    a = ((a - src_mean[1]) * (ref_std[1] / (src_std[1] + 1e-6))) + ref_mean[1]
    b = ((b - src_mean[2]) * (ref_std[2] / (src_std[2] + 1e-6))) + ref_mean[2]

    merged = cv2.merge([l,a,b])

    result = cv2.cvtColor(merged.astype("uint8"), cv2.COLOR_LAB2BGR)

    return result
