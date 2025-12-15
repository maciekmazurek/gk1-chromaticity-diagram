from __future__ import annotations

from typing import List, Sequence, Tuple

import numpy as np
from scipy.interpolate import CubicSpline, interp1d

from .bezier import eval_bezier_curve


def scale_norm_to_spectral(
    norm_x: np.ndarray,
    norm_y: np.ndarray,
    wavelengths: np.ndarray,
    cmfs_values: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    x = norm_x.copy()
    x *= wavelengths.max() - wavelengths.min()
    x += wavelengths.min()

    y = norm_y.copy()
    y *= cmfs_values.max() - cmfs_values.min()
    y += cmfs_values.min()

    return x, y


def calc_cmfs(wavelengths: np.ndarray, cmfs_values: np.ndarray) -> List[interp1d]:
    cmfs: List[interp1d] = []
    x = wavelengths
    for i in range(3):
        y = cmfs_values[:, i]
        cmfs.append(interp1d(x, y, kind="cubic", bounds_error=False, fill_value=0))
    return cmfs


def calc_spectrum_function(
    control_points: Sequence[Tuple[float, float]],
    wavelengths: np.ndarray,
    cmfs_values: np.ndarray,
    samples: int = 100,
) -> interp1d:
    curve_points = eval_bezier_curve(control_points, samples)
    nx = np.array([p[0] for p in curve_points], dtype=float)
    ny = np.array([p[1] for p in curve_points], dtype=float)
    x, y = scale_norm_to_spectral(nx, ny, wavelengths, cmfs_values)
    # Outside support -> 0
    return interp1d(x, y, kind="cubic", bounds_error=False, fill_value=0)


def integrate_XYZ(S_func: interp1d, cmfs: Sequence[interp1d]) -> List[float]:
    x = S_func.x
    XYZ: list[float] = []
    Sx = S_func(x)
    for cmf in cmfs:
        y_prod = cmf(x) * Sx
        integral = CubicSpline(x, y_prod).integrate(x[0], x[-1])
        XYZ.append(float(integral))
    return XYZ


def calc_XYZ_from_bezier(
    control_points: Sequence[Tuple[float, float]],
    wavelengths: np.ndarray,
    cmfs_values: np.ndarray,
    samples: int = 100,
) -> List[float]:
    S = calc_spectrum_function(control_points, wavelengths, cmfs_values, samples)
    cmfs = calc_cmfs(wavelengths, cmfs_values)
    return integrate_XYZ(S, cmfs)
