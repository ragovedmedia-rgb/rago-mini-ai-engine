from categories.color.auto_lut_generator.processor import generate_lut

def run(data):
    return generate_lut(
        data.get("source"),
        data.get("reference"),
        data.get("intensity", 1),
        data.get("lut_size", 33)
    )
