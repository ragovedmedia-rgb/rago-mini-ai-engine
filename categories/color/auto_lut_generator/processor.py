import numpy as np


def apply_exposure(r, g, b, value):
    return r + value, g + value, b + value


def apply_contrast(r, g, b, value):
    r = (r - 0.5) * (1 + value) + 0.5
    g = (g - 0.5) * (1 + value) + 0.5
    b = (b - 0.5) * (1 + value) + 0.5
    return r, g, b


def apply_temperature(r, g, b, value):
    r += value * 0.1
    b -= value * 0.1
    return r, g, b


def apply_tint(r, g, b, value):
    g += value * 0.1
    return r, g, b


def apply_saturation(r, g, b, value):
    avg = (r + g + b) / 3
    r = avg + (r - avg) * (1 + value)
    g = avg + (g - avg) * (1 + value)
    b = avg + (b - avg) * (1 + value)
    return r, g, b


def build_lut(sliders, size):

    exposure = sliders.get("exposure", 0) / 100.0
    contrast = sliders.get("contrast", 0) / 100.0
    saturation = sliders.get("saturation", 0) / 100.0
    temperature = sliders.get("temperature", 0) / 100.0
    tint = sliders.get("tint", 0) / 100.0

    lut = []

    for b in np.linspace(0, 1, size):
        for g in np.linspace(0, 1, size):
            for r in np.linspace(0, 1, size):

                rr, gg, bb = r, g, b

                rr, gg, bb = apply_exposure(rr, gg, bb, exposure)
                rr, gg, bb = apply_contrast(rr, gg, bb, contrast)
                rr, gg, bb = apply_temperature(rr, gg, bb, temperature)
                rr, gg, bb = apply_tint(rr, gg, bb, tint)
                rr, gg, bb = apply_saturation(rr, gg, bb, saturation)

                rr = np.clip(rr, 0, 1)
                gg = np.clip(gg, 0, 1)
                bb = np.clip(bb, 0, 1)

                lut.append((rr, gg, bb))

    return lut
