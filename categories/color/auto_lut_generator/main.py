from .validator import validate_request
from .processor import build_lut
from .cube_writer import save_cube


def run(data):

    valid, error = validate_request(data)

    if not valid:
        return {
            "success": False,
            "error": error
        }

    sliders = data.get("sliders")
    size = int(data.get("lut_size", 33))

    lut_data = build_lut(sliders, size)

    filename = save_cube(lut_data, size)

    return {
        "success": True,
        "lut_path": f"storage/luts/{filename}"
    }
