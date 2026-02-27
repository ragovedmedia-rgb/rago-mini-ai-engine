from .processor import generate_lut
from engine.response import success, error

def run(data):
    try:
        lut_path = generate_lut(
            data.get("source"),
            data.get("reference"),
            float(data.get("intensity", 1)),
            int(data.get("lut_size", 33))
        )

        return success({
            "success": True,
            "lut_path": lut_path
        })

    except Exception as e:
        return error(str(e))
