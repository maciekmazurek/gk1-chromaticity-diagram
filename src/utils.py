from pathlib import Path

import numpy as np


def load_color_matching_funcs() -> np.ndarray:
    """Load CIE color matching functions values.

    Returns
    -------
    np.ndarray
        Array of shape (N, 3) with XYZ-like values.
    """
    project_dir = Path(__file__).resolve().parent.parent
    file_path = project_dir / "resources" / "color_matching_functions.txt"

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    wavelenghts = np.loadtxt(file_path, usecols=0, dtype=float)
    XYZ = np.loadtxt(file_path, usecols=(1, 2, 3), dtype=float)

    return (wavelenghts, XYZ)
