import cv2
import numpy as np
import base64

def decode_image(data):

    header, encoded = data.split(",", 1)
    img_bytes = base64.b64decode(encoded)

    np_arr = np.frombuffer(img_bytes, np.uint8)

    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return img


def accurate_color_match(reference, source):

    ref = decode_image(reference)
    src = decode_image(source)

    ref_lab = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB).astype("float32")
    src_lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype("float32")

    l_s, a_s, b_s = cv2.split(src_lab)
    l_r, a_r, b_r = cv2.split(ref_lab)

    # means
    l_s_mean, a_s_mean, b_s_mean = l_s.mean(), a_s.mean(), b_s.mean()
    l_r_mean, a_r_mean, b_r_mean = l_r.mean(), a_r.mean(), b_r.mean()

    # slider estimation
    exposure = (l_r_mean - l_s_mean) / 100
    saturation = ((abs(a_r_mean) + abs(b_r_mean)) -
                  (abs(a_s_mean) + abs(b_s_mean))) / 100

    temperature = (b_r_mean - b_s_mean)
    tint = (a_r_mean - a_s_mean)

    return {
        "exposure": float(exposure),
        "contrast": 0,
        "saturation": float(saturation),
        "temperature": float(temperature),
        "tint": float(tint)
    }
