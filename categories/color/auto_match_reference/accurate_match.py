from .lab_transfer import lab_transfer
from .histogram_match import histogram_match
from .zone_harmony import zone_harmony

def accurate_match(src_img, ref_img):

    # stage 1 LAB transfer
    img = lab_transfer(src_img, ref_img)

    # stage 2 histogram alignment
    img = histogram_match(img, ref_img)

    # stage 3 tone harmony
    img = zone_harmony(img, ref_img)

    return img
