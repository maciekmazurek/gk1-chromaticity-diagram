from typing import List, Tuple


def de_casteljau(
    control_points: List[Tuple[float, float]], t: float
) -> Tuple[float, float]:
    """Evaluate a Bézier curve at parameter t using de Casteljau's algorithm.

    This stable, recursive linear interpolation method avoids explicit
    Bernstein polynomial evaluation and works for any control point count.
    """
    points = control_points.copy()
    n = len(points)
    if n == 0:
        return (0.0, 0.0)
    for r in range(1, n):
        for i in range(n - r):
            x = (1 - t) * points[i][0] + t * points[i + 1][0]
            y = (1 - t) * points[i][1] + t * points[i + 1][1]
            points[i] = (x, y)

    return points[0]


def eval_bezier_curve(
    control_points: List[Tuple[float, float]], samples: int
) -> List[Tuple[float, float]]:
    """Sample a Bézier curve uniformly in t ∈ [0,1].

    Parameters
    ----------
    control_points : list[tuple[float, float]]
        Control points ordered in increasing x to represent a function.
    samples : int
        Number of uniformly spaced samples; must be ≥ 2.
    """
    if samples < 2:
        raise ValueError("Samples must be at least 2")
    return [de_casteljau(control_points, t / (samples - 1)) for t in range(samples)]
