import cv2
import numpy as np

def solve_color(ref_img, src_img):

    ref_lab = cv2.cvtColor(ref_img, cv2.COLOR_BGR2LAB)
    src_lab = cv2.cvtColor(src_img, cv2.COLOR_BGR2LAB)

    ref_mean = np.mean(ref_lab, axis=(0,1))
    src_mean = np.mean(src_lab, axis=(0,1))

    temp = (ref_mean[2] - src_mean[2]) * 0.1
    tint = (ref_mean[1] - src_mean[1]) * 0.1

    ref_sat = np.std(ref_lab[:,:,1]) + np.std(ref_lab[:,:,2])
    src_sat = np.std(src_lab[:,:,1]) + np.std(src_lab[:,:,2])

    saturation = (ref_sat - src_sat) * 0.01

    return {
        "temperature": float(temp),
        "tint": float(tint),
        "saturation": float(saturation)
    }
