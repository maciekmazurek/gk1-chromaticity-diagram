from pathlib import Path

import numpy as np


def load_color_matching_funcs() -> tuple[np.ndarray, np.ndarray]:
    """Load CIE color matching functions values.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Tuple (wavelengths_nm, xyz) where wavelengths are in nm and
        xyz has shape (N, 3).
    """
    file_path = get_path_from_resources("color_matching_functions.txt")

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    wavelenghts = np.loadtxt(file_path, usecols=0, dtype=float)
    xyz = np.loadtxt(file_path, usecols=(1, 2, 3), dtype=float)

    return (wavelenghts, xyz)


def get_path_from_resources(relative_path: str) -> str:
    project_dir = Path(__file__).resolve().parent.parent
    return project_dir / "resources" / relative_path
