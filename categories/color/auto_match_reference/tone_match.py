import cv2
import numpy as np


def solve_tone(ref_img, src_img):

    src_lab = cv2.cvtColor(src_img, cv2.COLOR_BGR2LAB)
    ref_lab = cv2.cvtColor(ref_img, cv2.COLOR_BGR2LAB)

    src_l = src_lab[:, :, 0].astype("float32")
    ref_l = ref_lab[:, :, 0].astype("float32")

    # percentile tone points
    src_p = np.percentile(src_l, [5, 25, 50, 75, 95])
    ref_p = np.percentile(ref_l, [5, 25, 50, 75, 95])

    # build tone curve
    curve = np.interp(src_l.flatten(), src_p, ref_p)

    tone_mapped = curve.reshape(src_l.shape)

    src_lab[:, :, 0] = tone_mapped

    result = cv2.cvtColor(src_lab.astype("uint8"), cv2.COLOR_LAB2BGR)

    return result
