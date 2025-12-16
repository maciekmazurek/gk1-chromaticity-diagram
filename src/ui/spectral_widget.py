from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QMenu, QWidget

from numerics.bezier import eval_bezier_curve
from numerics.spectral import calc_XYZ_from_bezier
from utils import load_color_matching_funcs

EPS = 1e-5


class SpectralDistributionWidget(QWidget):
    XYZChanged = Signal(list)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.bezier_control_points: List[Tuple[float, float]] = [
            (0.084, 0.0),
            (0.18, 0.5),
            (0.33, 0.12),
            (0.93, 0.0),
        ]
        self.margin: int = 50

        self.wavelengths, self.cmfs_values = load_color_matching_funcs()

        self._dragging_index: Optional[int] = None
        self._hit_radius_px: int = 8
        self.setMouseTracking(True)
        self.background: Optional[QPixmap] = None

    def paintEvent(self, event) -> None:
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

    def setup_painter(self, painter: QPainter) -> None:
        painter.setRenderHint(QPainter.Antialiasing)

    def draw_background(self) -> None:
        background = QPixmap(self.width(), self.height())
        background.fill(Qt.transparent)
        painter = QPainter(background)
        try:
            self.setup_painter(painter)
            self.setup_coord_system_origin(painter)
            self.draw_color_matching_funcs(painter)
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            self.draw_coord_system(painter)
        finally:
            painter.end()
        self.background = background

    def setup_coord_system_origin(self, painter: QPainter) -> None:
        painter.translate(self.margin, self.height() - self.margin)
        painter.scale(1, -1)

    def calc_axis_lengths(self) -> tuple[int, int]:
        x_axis_length = self.width() - 2 * self.margin
        y_axis_length = self.height() - 2 * self.margin
        return x_axis_length, y_axis_length

    def draw_coord_system(self, painter: QPainter) -> None:
        x_axis_length, y_axis_length = self.calc_axis_lengths()
        painter.drawLine(0, 0, x_axis_length, 0)
        painter.drawLine(0, 0, 0, y_axis_length)
        self.draw_axis_ticks_and_labels(painter, x_axis_length, y_axis_length)

    def scale_norm_to_widget(self, point: tuple[float, float]) -> QPointF:
        x_axis_length, y_axis_length = self.calc_axis_lengths()
        x = point[0] * x_axis_length
        y = point[1] * y_axis_length
        return QPointF(x, y)

    def scale_widget_to_norm(self, point: QPointF) -> tuple[float, float]:
        x_axis_length, y_axis_length = self.calc_axis_lengths()
        # Scale values and then clamp to the normalized interval [0,1]
        # so points do not leave the drawn coordinate system
        x = max(0.0, min(1.0, point.x() / x_axis_length))
        y = max(0.0, min(1.0, point.y() / y_axis_length))
        return (x, y)

    def scale_spectral_to_norm(
        self, x: np.ndarray, y: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        norm_x = x.copy()
        norm_x -= norm_x.min()
        norm_x /= norm_x.max()

        norm_y = y.copy()
        norm_y -= norm_y.min()
        norm_y /= norm_y.max()

        return (norm_x, norm_y)

    def draw_color_matching_funcs(self, painter: QPainter) -> None:
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

    def draw_bezier_curve(self, painter: QPainter) -> None:
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
        painter.setBrush(QColor(237, 105, 240))
        painter.setPen(QPen(QColor(237, 105, 240), 2))
        for p in self.bezier_control_points:
            painter.drawEllipse(self.scale_norm_to_widget(p), 3, 3)

    def calc_XYZ(self) -> None:
        XYZ = calc_XYZ_from_bezier(
            self.bezier_control_points, self.wavelengths, self.cmfs_values
        )
        self.XYZChanged.emit(XYZ)

    def transform_to_widget(self, point: QPointF) -> QPointF:
        """Transform a point from the widget's default coordinate system to the
        drawing coordinate system accounting for margin and inverted Y axis"""
        x = point.x() - self.margin
        y = (self.height() - self.margin) - point.y()
        return QPointF(x, y)

    def control_point_hit_test(self, mouse_pos: QPointF) -> Optional[int]:
        candidates: list[int] = []
        widget_control_points = [
            self.scale_norm_to_widget(cp) for cp in self.bezier_control_points
        ]
        for i, cp in enumerate(widget_control_points):
            if (
                abs(cp.x() - mouse_pos.x()) <= self._hit_radius_px
                and abs(cp.y() - mouse_pos.y()) <= self._hit_radius_px
            ):
                candidates.append(i)

        if not candidates:
            return None

        n = len(self.bezier_control_points)
        inner = [i for i in candidates if i not in (0, n - 1)]
        if inner:
            return max(inner)
        return max(candidates)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.draw_background()

    def enforce_moving_point_position(self, x: float, y: float, point_index: int):
        """Enforce point position while moving so the Bézier curve remains
        a properly defined function"""
        n = len(self.bezier_control_points)
        if n < 2:
            return (x, y)

        # Left endpoint — keep it within (>= EPS, <= neighbor_x - EPS)
        if point_index == 0:
            right_cp_x = self.bezier_control_points[1][0]
            x = max(EPS, min(x, right_cp_x - EPS))
        # Right endpoint — keep it within (>= neighbor_x + EPS, <= 1 - EPS)
        elif point_index == n - 1:
            left_cp_x = self.bezier_control_points[n - 2][0]
            x = min(1.0 - EPS, max(x, left_cp_x + EPS))
        # Inner points — always between neighbors
        else:
            left_cp_x = self.bezier_control_points[point_index - 1][0]
            right_cp_x = self.bezier_control_points[point_index + 1][0]
            if x <= left_cp_x:
                x = left_cp_x + EPS
            if x >= right_cp_x:
                x = right_cp_x - EPS

        return (x, y)

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.LeftButton:
            return
        mouse_pos = self.transform_to_widget(event.position())
        self._dragging_index = self.control_point_hit_test(mouse_pos)

    def mouseMoveEvent(self, event) -> None:
        if self._dragging_index is None:
            return
        mouse_pos = self.transform_to_widget(event.position())
        x, y = self.scale_widget_to_norm(mouse_pos)
        x, y = self.enforce_moving_point_position(x, y, self._dragging_index)

        # Move end control points only along X (y = 0)
        if self._dragging_index in (0, len(self.bezier_control_points) - 1):
            y = 0.0

        self.bezier_control_points[self._dragging_index] = (x, y)
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._dragging_index = None

    def contextMenuEvent(self, event) -> None:
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
            # Force the new point between neighbors so it does not overlap by X
            # with existing points
            prev_x = cps[insert_idx - 1][0]
            next_x = cps[insert_idx][0]
            x = max(prev_x + EPS, min(x, next_x - EPS))
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

    def draw_axis_ticks_and_labels(
        self, painter: QPainter, x_axis_length: int, y_axis_length: int
    ):
        painter.save()
        tick_len = 6
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)

        # X axis
        wl_min = float(self.wavelengths[0])
        wl_max = float(self.wavelengths[-1])
        wl_step = 50

        # Drawing ticks
        for wl in range(int(wl_min), int(wl_max) + 1, wl_step):
            t = (wl - wl_min) / (wl_max - wl_min)  # [0, 1]
            x = t * x_axis_length
            painter.drawLine(x, 0, x, -tick_len)

        # Flip Y so the text isn't upside down
        painter.scale(1, -1)
        label_y = 21  # pixels below X axis

        # Drawing text
        for wl in range(int(wl_min), int(wl_max) + 1, wl_step):
            t = (wl - wl_min) / (wl_max - wl_min)
            x = t * x_axis_length
            text = f"{wl} [nm]" if wl == int(wl_max) else f"{wl}"
            # shift slightly to the left to place text under the tick
            painter.drawText(x - 12, label_y, text)

        # Y axis
        painter.scale(1, -1)  # return to the coordinate system with Y up
        y_max = 1.8
        y_step = 0.2

        # Drawing ticks
        for i in range(int(y_max / y_step) + 1):
            val = i * y_step
            t = val / y_max  # [0,1]
            y = t * y_axis_length
            painter.drawLine(0, y, -tick_len, y)  # tick to the left

        # Flip Y so the text isn't upside down
        painter.scale(1, -1)
        label_x = -30  # pixels to the left of the Y axis

        # Drawing text
        for i in range(int(y_max / y_step) + 1):
            val = i * y_step
            t = val / y_max
            y = -t * y_axis_length  # after flipping, Y has the opposite sign
            text = f"{val:.1f}"
            painter.drawText(label_x, y + 3, text)

        painter.restore()
