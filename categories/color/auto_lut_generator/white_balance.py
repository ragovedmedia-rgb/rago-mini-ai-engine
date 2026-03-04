def apply_white_balance(r, g, b, sliders):

    temperature = sliders.get("temperature", 0) / 100.0
    tint = sliders.get("tint", 0) / 100.0

    # Temperature shift
    r += temperature * 0.1
    b -= temperature * 0.1

    # Tint shift
    g += tint * 0.1

    return r, g, b
