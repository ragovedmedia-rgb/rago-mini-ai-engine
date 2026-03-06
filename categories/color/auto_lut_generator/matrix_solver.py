import numpy as np

# Example color transform matrix
# This simulates reference color shift

COLOR_MATRIX = np.array([
    [1.05, 0.02, -0.02],
    [0.01, 1.03, -0.01],
    [-0.02, 0.02, 1.05]
])


def apply_matrix(r, g, b):

    rgb = np.array([r, g, b])

    transformed = COLOR_MATRIX.dot(rgb)

    rr = max(0.0, min(1.0, transformed[0]))
    gg = max(0.0, min(1.0, transformed[1]))
    bb = max(0.0, min(1.0, transformed[2]))

    return rr, gg, bb
