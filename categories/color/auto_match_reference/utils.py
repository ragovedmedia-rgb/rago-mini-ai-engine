import base64
import cv2
import numpy as np

def decode_base64_image(data):

    if "," in data:
        data = data.split(",")[1]

    img_bytes = base64.b64decode(data)
    img_np = np.frombuffer(img_bytes, np.uint8)

    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    return img


def compute_luma(img):

    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]

    return 0.2126*r + 0.7152*g + 0.0722*b
