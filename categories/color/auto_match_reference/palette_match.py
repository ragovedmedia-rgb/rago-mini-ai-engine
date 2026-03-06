import cv2
import numpy as np


def extract_palette(img, k=5):

    pixels = img.reshape((-1,3))
    pixels = np.float32(pixels)

    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        20,
        1.0
    )

    _, labels, centers = cv2.kmeans(
        pixels,
        k,
        None,
        criteria,
        10,
        cv2.KMEANS_RANDOM_CENTERS
    )

    centers = np.uint8(centers)

    return centers


def palette_difference(ref_img, src_img):

    ref_palette = extract_palette(ref_img)
    src_palette = extract_palette(src_img)

    diff = ref_palette.astype("float32") - src_palette.astype("float32")

    mean_diff = np.mean(diff, axis=0)

    return {
        "red_shift": float(mean_diff[2]),
        "green_shift": float(mean_diff[1]),
        "blue_shift": float(mean_diff[0])
    }
