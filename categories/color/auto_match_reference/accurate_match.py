import cv2
import numpy as np
import base64


def decode_image(data):

    header, encoded = data.split(",", 1)
    img_bytes = base64.b64decode(encoded)

    arr = np.frombuffer(img_bytes, np.uint8)

    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    return img


def accurate_color_match(reference, source):

    ref = decode_image(reference)
    src = decode_image(source)

    ref = ref.astype("float32")
    src = src.astype("float32")

    # ---------- White balance match ----------
    ref_mean = np.mean(ref, axis=(0,1))
    src_mean = np.mean(src, axis=(0,1))

    wb_gain = ref_mean / (src_mean + 1e-6)

    src_wb = src * wb_gain

    # ---------- Convert to LAB ----------
    ref_lab = cv2.cvtColor(ref.astype("uint8"), cv2.COLOR_BGR2LAB).astype("float32")
    src_lab = cv2.cvtColor(src_wb.astype("uint8"), cv2.COLOR_BGR2LAB).astype("float32")

    l_s, a_s, b_s = cv2.split(src_lab)
    l_r, a_r, b_r = cv2.split(ref_lab)

    # ---------- Luminance match ----------
    l_gain = l_r.mean() / (l_s.mean() + 1e-6)

    # ---------- Chroma difference ----------
    tint = a_r.mean() - a_s.mean()
    temp = b_r.mean() - b_s.mean()

    # ---------- Saturation estimate ----------
    sat_s = np.std(a_s) + np.std(b_s)
    sat_r = np.std(a_r) + np.std(b_r)

    saturation = (sat_r - sat_s) / 50

    exposure = (l_gain - 1)

    return {
        "exposure": float(exposure),
        "contrast": 0,
        "saturation": float(saturation),
        "temperature": float(temp),
        "tint": float(tint)
    }
