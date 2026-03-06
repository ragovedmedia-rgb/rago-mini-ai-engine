import cv2
import numpy as np

def accurate_color_match(source, reference):

    src = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    ref = cv2.cvtColor(reference, cv2.COLOR_BGR2LAB).astype("float32")

    l_s, a_s, b_s = cv2.split(src)
    l_r, a_r, b_r = cv2.split(ref)

    # mean/std
    l_s_mean, l_s_std = l_s.mean(), l_s.std()
    a_s_mean, a_s_std = a_s.mean(), a_s.std()
    b_s_mean, b_s_std = b_s.mean(), b_s.std()

    l_r_mean, l_r_std = l_r.mean(), l_r.std()
    a_r_mean, a_r_std = a_r.mean(), a_r.std()
    b_r_mean, b_r_std = b_r.mean(), b_r.std()

    # luminance protection
    l = (l_s - l_s_mean) * (l_r_std / (l_s_std + 1e-6)) + l_r_mean
    l = 0.6 * l + 0.4 * l_s

    # chroma transfer
    a = (a_s - a_s_mean) * (a_r_std / (a_s_std + 1e-6)) + a_r_mean
    b = (b_s - b_s_mean) * (b_r_std / (b_s_std + 1e-6)) + b_r_mean

    merged = cv2.merge([l, a, b])
    merged = np.clip(merged, 0, 255).astype("uint8")

    result = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    return result
