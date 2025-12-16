from typing import Tuple


def xyY_to_XYZ(x: float, y: float, Y: float) -> Tuple[float, float, float]:
    """Convert chromaticity-luminance (x, y, Y) to tristimulus XYZ.

    Uses the identities X = x·Y/y, Z = (1−x−y)·Y/y with guarding for y ≤ 0.
    """
    if y <= 0:
        return (0.0, 0.0, 0.0)
    X = x * Y / y
    Z = (1.0 - x - y) * Y / y
    return (X, Y, Z)


def XYZ_to_sRGB(X: float, Y: float, Z: float) -> Tuple[int, int, int]:
    """Convert XYZ (D65) to 8-bit sRGB with gamma correction.

    Applies XYZ→linear sRGB (D65) matrix, then IEC 61966-2-1 transfer
    function (gamma) and clamps to [0,1] before quantizing to 0–255.
    """
    # XYZ -> linear sRGB (D65)
    r_linear = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
    g_linear = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
    b_linear = 0.0557 * X - 0.2040 * Y + 1.0570 * Z

    def sRGB_gamma_correct(color_val: float) -> float:
        if color_val <= 0:
            return 0.0
        if color_val <= 0.0031308:
            return 12.92 * color_val
        return 1.055 * (color_val ** (1.0 / 2.4)) - 0.055

    r = max(0.0, min(1.0, sRGB_gamma_correct(r_linear)))
    g = max(0.0, min(1.0, sRGB_gamma_correct(g_linear)))
    b = max(0.0, min(1.0, sRGB_gamma_correct(b_linear)))

    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))
