def validate_request(data):

    sliders = data.get("sliders")
    wheels = data.get("wheels")
    lut_size = data.get("lut_size", 33)
    lut_format = data.get("lut_format", ".cube")
    dimension = data.get("lut_dimension", "3d")

    if sliders is None:
        return False, "Missing sliders data"

    if lut_format != ".cube":
        return False, "Only .cube supported"

    if dimension != "3d":
        return False, "Only 3D LUT supported"

    if int(lut_size) not in [17, 33, 65]:
        return False, "Invalid LUT size"

    return True, None
