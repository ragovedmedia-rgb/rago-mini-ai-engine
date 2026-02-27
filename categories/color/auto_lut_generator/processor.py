import base64
import numpy as np
from PIL import Image
from io import BytesIO
import os

def base64_to_array(data):
    header, encoded = data.split(",",1)
    img = Image.open(BytesIO(base64.b64decode(encoded))).convert("RGB")
    return np.array(img) / 255.0

def generate_lut(source_b64, reference_b64, intensity, size):

    src = base64_to_array(source_b64)
    ref = base64_to_array(reference_b64)

    src_mean = src.mean(axis=(0,1))
    ref_mean = ref.mean(axis=(0,1))

    shift = (ref_mean - src_mean) * intensity

    lines = []
    lines.append('TITLE "RagoAI LUT"')
    lines.append(f"LUT_3D_SIZE {size}")

    for b in np.linspace(0,1,size):
        for g in np.linspace(0,1,size):
            for r in np.linspace(0,1,size):
                rr = np.clip(r + shift[0], 0, 1)
                gg = np.clip(g + shift[1], 0, 1)
                bb = np.clip(b + shift[2], 0, 1)
                lines.append(f"{rr:.6f} {gg:.6f} {bb:.6f}")

    os.makedirs("storage/luts", exist_ok=True)
    file_path = f"storage/luts/generated_{size}.cube"

    with open(file_path, "w") as f:
        f.write("\n".join(lines))

    return {
        "success": True,
        "lut_path": file_path
    }
