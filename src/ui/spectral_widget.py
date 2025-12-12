import numpy as np
from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QMenu, QWidget
from scipy.interpolate import CubicSpline, interp1d

from numerics.bezier import eval_bezier_curve
from utils import load_color_matching_funcs

EPS = 1e-5


class SpectralDistributionWidget(QWidget):
    XYZChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bezier_control_points = [(0.2, 0), (0.4, 0.4), (0.7, 0.4), (0.9, 0)]
        self.margin = 50

        self.wavelengths, self.cmfs_values = load_color_matching_funcs()
        self.cmfs = self.calc_cmfs()

        self._dragging_index = None
        self._hit_radius_px = 8
        self.setMouseTracking(True)

        self.background: QPixmap = None

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            self.setup_painter(painter)
            if self.background is None:
                self.draw_background()
            else:
                painter.drawPixmap(0, 0, self.background)
            self.setup_coord_system_origin(painter)
            self.draw_bezier_curve(painter)
            self.calc_XYZ()
        finally:
            painter.end()

    def setup_painter(self, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)

    def draw_background(self):
        background = QPixmap(self.width(), self.height())
        background.fill(Qt.transparent)
        painter = QPainter(background)
        try:
            self.setup_painter(painter)
            self.draw_coord_system(painter)
            self.draw_color_matching_funcs(painter)
        finally:
            painter.end()
        self.background = background

    def setup_coord_system_origin(self, painter: QPainter):
        painter.translate(self.margin, self.height() - self.margin)
        painter.scale(1, -1)

    def calc_axis_lengths(self) -> tuple[int, int]:
        x_axis_length = self.width() - 2 * self.margin
        y_axis_length = self.height() - 2 * self.margin
        return x_axis_length, y_axis_length

    def draw_coord_system(self, painter: QPainter):
        self.setup_coord_system_origin(painter)
        x_axis_length, y_axis_length = self.calc_axis_lengths()
        painter.drawLine(0, 0, x_axis_length, 0)
        painter.drawLine(0, 0, 0, y_axis_length)

    def scale_norm_to_widget(self, point: tuple[float, float]) -> QPointF:
        x_axis_length, y_axis_length = self.calc_axis_lengths()
        x = point[0] * x_axis_length
        y = point[1] * y_axis_length
        return QPointF(x, y)

    def scale_widget_to_norm(self, point: QPointF) -> tuple[float, float]:
        x_axis_length, y_axis_length = self.calc_axis_lengths()
        # Skalujemy wartości, a następnie clamp-ujemy do znormalizowanego
        # przedziału [0,1], tak aby punkty nie wychodziły poza rysowany
        # układ współrzędnych
        x = max(0.0, min(1.0, point.x() / x_axis_length))
        y = max(0.0, min(1.0, point.y() / y_axis_length))
        return (x, y)

    def scale_spectral_to_norm(self, x: np.ndarray, y: np.ndarray):
        norm_x = x.copy()
        norm_x -= norm_x.min()
        norm_x /= norm_x.max()

        norm_y = y.copy()
        norm_y -= norm_y.min()
        norm_y /= norm_y.max()

        return (norm_x, norm_y)

    def scale_norm_to_spectral(self, norm_x: np.ndarray, norm_y: np.ndarray):
        x = norm_x.copy()
        x *= self.wavelengths.max() - self.wavelengths.min()
        x += self.wavelengths.min()

        y = norm_y.copy()
        y *= self.cmfs_values.max() - self.cmfs_values.min()
        y += self.cmfs_values.min()

        return (x, y)

    def draw_color_matching_funcs(self, painter: QPainter):
        norm_wavelengths, norm_cmfs_values = self.scale_spectral_to_norm(
            self.wavelengths, self.cmfs_values
        )
        opacity = 50
        for i in range(3):
            path = QPainterPath()
            rgba_value = [0, 0, 0, opacity]
            rgba_value[i] = 255
            painter.setPen(QPen(QColor(*rgba_value), 2))
            norm_cmf_values = norm_cmfs_values[:, i]
            first_point = self.scale_norm_to_widget(
                (norm_wavelengths[0], norm_cmf_values[0])
            )
            path.moveTo(first_point)
            for wl, fv in zip(norm_wavelengths[1:], norm_cmf_values[1:]):
                path.lineTo(self.scale_norm_to_widget((wl, fv)))
            painter.drawPath(path)

    def draw_bezier_curve(self, painter: QPainter):
        samples = 100
        curve_points = eval_bezier_curve(self.bezier_control_points, samples)

        # Drawing the control polygon
        painter.setPen(QPen(QColor(122, 130, 122), 1))
        for p1, p2 in zip(self.bezier_control_points, self.bezier_control_points[1:]):
            painter.drawLine(
                self.scale_norm_to_widget(p1), self.scale_norm_to_widget(p2)
            )

        # Drawing the curve
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        path = QPainterPath()
        first_point = self.scale_norm_to_widget(curve_points[0])
        path.moveTo(first_point)
        for point in curve_points[1:]:
            path.lineTo(self.scale_norm_to_widget(point))
        painter.drawPath(path)

        # Drawing control points
        painter.setBrush(QColor(255, 200, 255))
        painter.setPen(QPen(QColor(255, 200, 255), 2))
        for p in self.bezier_control_points:
            painter.drawEllipse(self.scale_norm_to_widget(p), 3, 3)

    def transform_to_widget(self, point: QPointF) -> QPointF:
        """Przekształca punkt z oryginalnego, domyślnego układu współrzędnych widgetu do układu
        współrzędnych wykorzystywanego do rysowania uwzględniającego margines i odwrócenie osi Y"""
        x = point.x() - self.margin
        y = (self.height() - self.margin) - point.y()
        return QPointF(x, y)

    def control_point_hit_test(self, mouse_pos: QPointF) -> int | None:
        """Sprawdza czy kursor myszy wchodzi w interakcję z punktem kontrolnym.
        Jeżeli tak zwraca jego indeks, jeżeli nie zwraca None"""
        index = None
        widget_control_points = [
            self.scale_norm_to_widget(cp) for cp in self.bezier_control_points
        ]
        for i, cp in enumerate(widget_control_points):
            if (
                abs(cp.x() - mouse_pos.x()) <= self._hit_radius_px
                and abs(cp.y() - mouse_pos.y()) <= self._hit_radius_px
            ):
                index = i
                break
        return index

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.draw_background()

    def enforce_moving_point_position(self, x: float, y: float, point_index: int):
        """Wymusza położenie punktu, tak aby krzywa beziera zawsze
        była poprawnie zdefiniowaną funkcją"""
        if point_index != 0:
            left_cp_x = self.bezier_control_points[point_index - 1][0]
            if x <= left_cp_x:
                x = left_cp_x + EPS
        if point_index != len(self.bezier_control_points) - 1:
            right_cp_x = self.bezier_control_points[point_index + 1][0]
            if x >= right_cp_x:
                x = right_cp_x - EPS
        return (x, y)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        mouse_pos = self.transform_to_widget(event.position())
        self._dragging_index = self.control_point_hit_test(mouse_pos)

    def mouseMoveEvent(self, event):
        if self._dragging_index is None:
            return
        mouse_pos = self.transform_to_widget(event.position())
        x, y = self.scale_widget_to_norm(mouse_pos)
        x, y = self.enforce_moving_point_position(x, y, self._dragging_index)

        # Końcowe punkty kontrolne poruszamy tylko po osi X (y = 0)
        if self._dragging_index in (0, len(self.bezier_control_points) - 1):
            y = 0.0

        self.bezier_control_points[self._dragging_index] = (x, y)
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging_index = None

    def contextMenuEvent(self, event):
        mouse_pos = self.transform_to_widget(event.pos())
        x_axis_length, y_axis_length = self.calc_axis_lengths()

        # Only allow adding when click is inside the axes rectangle
        if not (
            0 <= mouse_pos.x() <= x_axis_length and 0 <= mouse_pos.y() <= y_axis_length
        ):
            return

        menu = QMenu(self)
        add_cp_action = None
        del_cp_action = None
        cp_idx = self.control_point_hit_test(mouse_pos)
        control_point_hit = True if cp_idx is not None else False
        if control_point_hit:
            del_cp_action = menu.addAction("Delete control point")
        else:
            add_cp_action = menu.addAction("Add control point")
        chosen = menu.exec(event.globalPos())
        if chosen is not None and add_cp_action is not None and chosen is add_cp_action:
            x, y = self.scale_widget_to_norm(mouse_pos)
            # Insert point keeping list ordered by x
            cps = list(self.bezier_control_points)
            insert_idx = 1
            while insert_idx < len(cps) - 1 and cps[insert_idx][0] <= x:
                insert_idx += 1
            # Enforcing proper control point x coordinate to keep the bezier
            # curve a correct mathematical function
            if insert_idx == 1:
                start_cp_x = cps[0][0]
                if x <= start_cp_x:
                    x = start_cp_x + EPS
            elif insert_idx == len(cps) - 1:
                end_cp_x = cps[-1][0]
                if x >= end_cp_x:
                    x = end_cp_x - EPS
            cps.insert(insert_idx, (x, y))
            self.bezier_control_points = cps
        elif (
            chosen is not None
            and del_cp_action is not None
            and chosen is del_cp_action
            and cp_idx is not None
        ):
            n = len(self.bezier_control_points)
            if n > 2 and cp_idx not in (0, n - 1):
                del self.bezier_control_points[cp_idx]

        self.update()

    def calc_spectral_func(self) -> interp1d:
        # Liczymy funkcję widmową poprzez interpolację krzywej beziera
        samples = 100
        curve_points = eval_bezier_curve(self.bezier_control_points, samples)
        x = np.array([p[0] for p in curve_points], dtype=float)
        y = np.array([p[1] for p in curve_points], dtype=float)
        # Skalujemy do [380, 780] x [0, ~1.8]
        x, y = self.scale_norm_to_spectral(x, y)
        # Dla wartości x z poza zakresu zwracamy 0
        S_func = interp1d(x, y, kind="cubic", bounds_error=False, fill_value=0)
        return S_func

    def calc_cmfs(self) -> list[interp1d]:
        cmfs = []
        x = self.wavelengths
        for i in range(3):
            y = self.cmfs_values[:, i]
            cmfs.append(interp1d(x, y, kind="cubic", bounds_error=False, fill_value=0))
        return cmfs

    def calc_XYZ(self):
        XYZ = []
        S_func = self.calc_spectral_func()
        x = S_func.x
        for cmf in self.cmfs:
            y_product = cmf(x) * S_func(x)
            integral = CubicSpline(x, y_product).integrate(x[0], x[-1])
            XYZ.append(integral)

        self.XYZChanged.emit(XYZ)
