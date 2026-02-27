import os
import uuid


def save_cube(lut_data, size):

    os.makedirs("storage/luts", exist_ok=True)

    filename = f"rago_{size}_{uuid.uuid4().hex[:6]}.cube"
    path = os.path.join("storage/luts", filename)

    with open(path, "w") as f:
        f.write('TITLE "Rago AI LUT"\n')
        f.write(f"LUT_3D_SIZE {size}\n")
        f.write("DOMAIN_MIN 0.0 0.0 0.0\n")
        f.write("DOMAIN_MAX 1.0 1.0 1.0\n")

        for r, g, b in lut_data:
            f.write(f"{r:.6f} {g:.6f} {b:.6f}\n")

    return filename
