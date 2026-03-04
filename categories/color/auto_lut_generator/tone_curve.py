def apply_tone_curve(r, g, b, sliders):

    exposure = sliders.get("exposure", 0) / 100.0
    contrast = sliders.get("contrast", 0) / 100.0
    saturation = sliders.get("saturation", 0) / 100.0
    whites = sliders.get("whites", 0) / 100.0
    blacks = sliders.get("blacks", 0) / 100.0

    # Exposure
    r += exposure
    g += exposure
    b += exposure

    # Contrast
    r = (r - 0.5) * (1 + contrast) + 0.5
    g = (g - 0.5) * (1 + contrast) + 0.5
    b = (b - 0.5) * (1 + contrast) + 0.5

    # Saturation
    avg = (r + g + b) / 3.0
    r = avg + (r - avg) * (1 + saturation)
    g = avg + (g - avg) * (1 + saturation)
    b = avg + (b - avg) * (1 + saturation)

    # Whites
    lum = (r + g + b) / 3.0
    if lum > 0.7:
        r += whites * 0.1
        g += whites * 0.1
        b += whites * 0.1

    # Blacks
    if lum < 0.3:
        r -= blacks * 0.1
        g -= blacks * 0.1
        b -= blacks * 0.1

    return r, g, b
