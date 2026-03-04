import math


def apply_zone_match(r, g, b, wheels):

    if not wheels:
        return r, g, b

    lum = (r + g + b) / 3.0

    if lum < 0.33:
        zone = wheels[0]
    elif lum < 0.66:
        zone = wheels[1]
    else:
        zone = wheels[2]

    hue = zone.get("hue", 0)
    intensity = zone.get("intensity", 0)
    luma = zone.get("luma", 0)

    rad = hue * math.pi / 180.0

    r += math.cos(rad) * intensity * 0.3
    g += math.sin(rad) * intensity * 0.3
    b += math.cos(rad + 2) * intensity * 0.3

    r += luma * 0.002
    g += luma * 0.002
    b += luma * 0.002

    return r, g, b
