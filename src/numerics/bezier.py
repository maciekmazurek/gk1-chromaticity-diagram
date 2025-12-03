def de_casteljau(
    control_points: list[tuple[float, float]], t: float
) -> tuple[float, float]:
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
    control_points: list[tuple[float, float]], samples: int
) -> list[tuple[float, float]]:
    if samples < 2:
        raise ValueError("Samples must be at least 2")
    return [de_casteljau(control_points, t / (samples - 1)) for t in range(samples)]
