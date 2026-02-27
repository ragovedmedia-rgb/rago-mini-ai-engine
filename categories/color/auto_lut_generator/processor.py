import base64
import numpy as np
from PIL import Image
from io import BytesIO
import os
import uuid


# ===============================
# SAFE BASE64 TO NUMPY
# ===============================
def base64_to_array(data):
    try:
        if not data or "," not in data:
            raise ValueError("Invalid base64 image data")

        header, encoded = data.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(img_bytes)).convert("RGB")

        return np.array(img) / 255.0

    except Exception as e:
        raise Exception(f"Image decode failed: {str(e)}")


# ===============================
# LUT GENERATOR
# ===============================
def generate_lut(source_b64, reference_b64, intensity, size):

    try:
        # Validate inputs
        if not source_b64 or not reference_b64:
            raise ValueError("Source or Reference image missing")

        size = int(size)
        if size < 2 or size > 65:
            raise ValueError("Invalid LUT size (2-65 allowed)")

        intensity = float(intensity)

        # Convert images
        src = base64_to_array(source_b64)
        ref = base64_to_array(reference_b64)

        # Compute color shift
        src_mean = src.mean(axis=(0, 1))
        ref_mean = ref.mean(axis=(0, 1))
        shift = (ref_mean - src_mean) * intensity

        # Generate LUT content
        lines = []
        lines.append('TITLE "RagoAI Generated LUT"')
        lines.append(f"LUT_3D_SIZE {size}")

        for b in np.linspace(0, 1, size):
            for g in np.linspace(0, 1, size):
                for r in np.linspace(0, 1, size):
                    rr = np.clip(r + shift[0], 0, 1)
                    gg = np.clip(g + shift[1], 0, 1)
                    bb = np.clip(b + shift[2], 0, 1)
                    lines.append(f"{rr:.6f} {gg:.6f} {bb:.6f}")

        # Ensure folder exists
        output_dir = os.path.join("storage", "luts")
        os.makedirs(output_dir, exist_ok=True)

        # Unique filename (important for production)
        filename = f"generated_{size}_{uuid.uuid4().hex[:8]}.cube"
        file_path = os.path.join(output_dir, filename)

        # Write file
        with open(file_path, "w") as f:
            f.write("\n".join(lines))

        return {
            "success": True,
            "lut_path": file_path
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
