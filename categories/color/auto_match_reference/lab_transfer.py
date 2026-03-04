import numpy as np


# ===============================
# RGB → LAB conversion helpers
# ===============================

def rgb_to_xyz(r, g, b):

    r = r ** 2.2
    g = g ** 2.2
    b = b ** 2.2

    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    return x, y, z


def xyz_to_lab(x, y, z):

    x /= 0.95047
    y /= 1.00000
    z /= 1.08883

    def f(t):
        if t > 0.008856:
            return t ** (1/3)
        else:
            return (7.787 * t) + (16 / 116)

    fx = f(x)
    fy = f(y)
    fz = f(z)

    L = (116 * fy) - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)

    return L, a, b


def lab_to_xyz(L, a, b):

    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200

    def f_inv(t):
        if t ** 3 > 0.008856:
            return t ** 3
        else:
            return (t - 16/116) / 7.787

    x = 0.95047 * f_inv(fx)
    y = 1.00000 * f_inv(fy)
    z = 1.08883 * f_inv(fz)

    return x, y, z


def xyz_to_rgb(x, y, z):

    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return r, g, b


# ===============================
# MAIN COLOR TRANSFER
# ===============================

def lab_color_transfer(src_pixels, ref_pixels):

    src_lab = []
    ref_lab = []

    for r, g, b in src_pixels:
        x, y, z = rgb_to_xyz(r, g, b)
        src_lab.append(xyz_to_lab(x, y, z))

    for r, g, b in ref_pixels:
        x, y, z = rgb_to_xyz(r, g, b)
        ref_lab.append(xyz_to_lab(x, y, z))

    src_lab = np.array(src_lab)
    ref_lab = np.array(ref_lab)

    src_mean = np.mean(src_lab, axis=0)
    src_std = np.std(src_lab, axis=0)

    ref_mean = np.mean(ref_lab, axis=0)
    ref_std = np.std(ref_lab, axis=0)

    result_pixels = []

    for L, a, b in src_lab:

        L = ((L - src_mean[0]) * (ref_std[0] / (src_std[0] + 1e-6))) + ref_mean[0]
        a = ((a - src_mean[1]) * (ref_std[1] / (src_std[1] + 1e-6))) + ref_mean[1]
        b = ((b - src_mean[2]) * (ref_std[2] / (src_std[2] + 1e-6))) + ref_mean[2]

        x, y, z = lab_to_xyz(L, a, b)
        r, g, bb = xyz_to_rgb(x, y, z)

        result_pixels.append((r, g, bb))

    return result_pixels
