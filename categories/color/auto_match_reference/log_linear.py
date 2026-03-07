# ----------------------------------------
# RAGO AI
# Log → Linear Conversion
# Gamma Normalization
# ----------------------------------------

import numpy as np


# ----------------------------------------
# Gamma → Linear
# ----------------------------------------

def gamma_to_linear(img):

    img = img.astype(np.float32) / 255.0

    linear = np.power(img, 2.2)

    return linear


# ----------------------------------------
# Linear → Gamma
# ----------------------------------------

def linear_to_gamma(img):

    gamma = np.power(img, 1.0 / 2.2)

    gamma = np.clip(gamma, 0, 1)

    return (gamma * 255).astype(np.uint8)


# ----------------------------------------
# Normalize dynamic range
# ----------------------------------------

def normalize_image(img):

    img = img.astype(np.float32)

    min_val = np.min(img)
    max_val = np.max(img)

    if max_val - min_val < 1e-6:
        return img

    norm = (img - min_val) / (max_val - min_val)

    return norm


# ----------------------------------------
# Full preprocessing pipeline
# ----------------------------------------

def prepare_for_analysis(img):

    # convert gamma encoded image → linear light
    linear = gamma_to_linear(img)

    # normalize dynamic range
    linear = normalize_image(linear)

    return linear
