import numpy as np
import base64
import io
from PIL import Image


# =====================================
# BASE64 → IMAGE → NUMPY
# =====================================

def decode_base64_image(data):

    if "," in data:
        data = data.split(",")[1]

    img_bytes = base64.b64decode(data)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # small resize for fast analysis
    img = img.resize((200,200))

    return np.asarray(img) / 255.0


# =====================================
# RGB → LAB CONVERSION
# =====================================

def rgb_to_lab(img):

    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]

    # gamma
    r = r ** 2.2
    g = g ** 2.2
    b = b ** 2.2

    # RGB → XYZ
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    x /= 0.95047
    z /= 1.08883

    def f(t):
        return np.where(t > 0.008856, t ** (1/3), (7.787 * t) + (16/116))

    fx = f(x)
    fy = f(y)
    fz = f(z)

    L = (116 * fy) - 16
    A = 500 * (fx - fy)
    B = 200 * (fy - fz)

    return np.stack([L,A,B], axis=2)


# =====================================
# LAB COLOR STATISTICS
# =====================================

def compute_stats(lab):

    mean = np.mean(lab.reshape(-1,3), axis=0)
    std  = np.std(lab.reshape(-1,3), axis=0)

    return mean, std


# =====================================
# COLOR TRANSFER
# =====================================

def transfer_lab(src_lab, ref_mean, ref_std, src_mean, src_std):

    result = src_lab.copy()

    for i in range(3):

        result[:,:,i] = (
            (result[:,:,i] - src_mean[i])
            * (ref_std[i] / (src_std[i] + 1e-6))
        ) + ref_mean[i]

    return result


# =====================================
# LAB → RGB
# =====================================

def lab_to_rgb(lab):

    L = lab[:,:,0]
    A = lab[:,:,1]
    B = lab[:,:,2]

    fy = (L + 16) / 116
    fx = A / 500 + fy
    fz = fy - B / 200

    def inv(t):
        return np.where(t**3 > 0.008856, t**3, (t - 16/116)/7.787)

    x = 0.95047 * inv(fx)
    y = inv(fy)
    z = 1.08883 * inv(fz)

    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    rgb = np.stack([r,g,b], axis=2)

    return np.clip(rgb,0,1)


# =====================================
# MAIN FUNCTION
# =====================================

def color_transfer(reference_base64, source_base64):

    ref_img = decode_base64_image(reference_base64)
    src_img = decode_base64_image(source_base64)

    ref_lab = rgb_to_lab(ref_img)
    src_lab = rgb_to_lab(src_img)

    ref_mean, ref_std = compute_stats(ref_lab)
    src_mean, src_std = compute_stats(src_lab)

    transferred_lab = transfer_lab(src_lab, ref_mean, ref_std, src_mean, src_std)

    result_rgb = lab_to_rgb(transferred_lab)

    return result_rgb
