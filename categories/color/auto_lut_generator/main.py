from .validator import validate_request
from .processor import build_lut
from .cube_writer import save_cube


def run(data):

    try:

        # =============================
        # VALIDATE REQUEST
        # =============================

        valid, error = validate_request(data)

        if not valid:
            return {
                "success": False,
                "error": error
            }

        # =============================
        # INPUT DATA
        # =============================

        sliders = data.get("sliders", {})
        wheels  = data.get("wheels", [])

        try:
            size = int(data.get("lut_size", 33))
        except:
            size = 33

        # =============================
        # BUILD LUT
        # =============================

        lut_data = build_lut(sliders, wheels, size)

        # =============================
        # SAVE LUT FILE
        # =============================

        filename = save_cube(lut_data, size)

        # =============================
        # RESPONSE TO FRONTEND
        # =============================

        return {
            "success": True,
            "lut_path": f"storage/luts/{filename}"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
