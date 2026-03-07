import cv2
import numpy as np


# ---------------------------------------------------
# Extract dominant color palette using K-Means
# ---------------------------------------------------

def extract_palette(img, k=5):

    # reshape image → list of pixels
    pixels = img.reshape((-1, 3))
    pixels = np.float32(pixels)

    # kmeans stop condition
    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        20,
        1.0
    )

    # run kmeans
    _, labels, centers = cv2.kmeans(
        pixels,
        k,
        None,
        criteria,
        10,
        cv2.KMEANS_RANDOM_CENTERS
    )

    centers = np.uint8(centers)

    # sort palette by brightness (stable order)
    brightness = np.sum(centers, axis=1)
    order = np.argsort(brightness)

    centers = centers[order]

    return centers


# ---------------------------------------------------
# Solve palette difference between reference & source
# ---------------------------------------------------

def solve_palette(ref_img, src_img):

    # extract palettes
    ref_palette = extract_palette(ref_img)
    src_palette = extract_palette(src_img)

    # convert to float
    ref_palette = ref_palette.astype("float32")
    src_palette = src_palette.astype("float32")

    # compute palette difference
    diff = ref_palette - src_palette

    # average shift across palette
    mean_diff = np.mean(diff, axis=0)

    # BGR → convert to RGB logic
    blue_shift = mean_diff[0]
    green_shift = mean_diff[1]
    red_shift = mean_diff[2]

    return {
        "red_shift": float(red_shift),
        "green_shift": float(green_shift),
        "blue_shift": float(blue_shift)
    }
