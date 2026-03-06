def build_sliders(levels, color, tone):

    sliders = {}

    sliders["exposure"] = levels["exposure"]
    sliders["contrast"] = levels["contrast"]
    sliders["temperature"] = color["temperature"]
    sliders["tint"] = color["tint"]
    sliders["saturation"] = color["saturation"]

    return sliders
