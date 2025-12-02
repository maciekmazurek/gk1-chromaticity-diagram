from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget


class SpectralDistributionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bezier_control_points = [(0.2, 0), (0.4, 0.4), (0.7, 0.5), (0.9, 0)]
        self.min_wavelength = 380
        self.max_wavelength = 780
        self.max_coefficient = 1.8
        self.margin = 40

        self._dragging_index = None
        self._hit_radius_px = 8
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            self.setup_painter(painter)
            self.setup_coord_system_origin(painter)
            self.draw_coord_system(painter)
            self.draw_bezier_curve(painter)
        finally:
            painter.end()

    def setup_painter(self, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)

    def setup_coord_system_origin(self, painter: QPainter):
        painter.translate(self.margin, self.height() - self.margin)
        painter.scale(1, -1)

    def draw_coord_system(self, painter: QPainter):
        x_axis_length = self.width() - 2 * self.margin
        y_axis_length = self.height() - 2 * self.margin
        painter.drawLine(0, 0, x_axis_length, 0)
        painter.drawLine(0, 0, 0, y_axis_length)

    def calc_axis_lengths(self):
        x_axis_length = self.width() - 2 * self.margin
        y_axis_length = self.height() - 2 * self.margin
        return x_axis_length, y_axis_length

    def scale_to_coord_sys(self, point: tuple[float, float]) -> QPointF:
        x_axis_length, y_axis_length = self.calc_axis_lengths()
        scaled_x = point[0] * x_axis_length
        scaled_y = point[1] * y_axis_length
        return QPointF(scaled_x, scaled_y)

    def scale_to_normalized(self, point: QPointF) -> tuple[float, float]:
        x_axis_length, y_axis_length = self.calc_axis_lengths()
        scaled_x = point.x() / x_axis_length
        scaled_y = point.y() / y_axis_length
        return (scaled_x, scaled_y)

    def draw_bezier_curve(self, painter: QPainter):
        cp0, cp1, cp2, cp3 = [
            self.scale_to_coord_sys(cp) for cp in self.bezier_control_points
        ]
        path = QPainterPath()
        path.moveTo(cp0)
        path.cubicTo(cp1, cp2, cp3)

        # Curve
        painter.drawPath(path)

        # Control points
        painter.setBrush(QColor(255, 200, 255))
        painter.setPen(QPen(QColor(255, 200, 255), 2))
        for p in (cp0, cp1, cp2, cp3):
            painter.drawEllipse(p, 3, 3)

    def transform_to_coord_sys(self, point: QPointF) -> QPointF:
        """Przekształca punkt z układu współrzędnych widgetu do układu współrzędnych rysowania uwzględniając margines i odwrócenie osi Y."""
        x = point.x() - self.margin
        y = (self.height() - self.margin) - point.y()
        return QPointF(x, y)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        pos = self.transform_to_coord_sys(event.position())
        coord_control_points = [
            self.scale_to_coord_sys(cp) for cp in self.bezier_control_points
        ]
        index = None
        for i, cp in enumerate(coord_control_points):
            if (
                abs(cp.x() - pos.x()) <= self._hit_radius_px
                and abs(cp.y() - pos.y()) <= self._hit_radius_px
            ):
                index = i
                break
        self._dragging_index = index

    def mouseMoveEvent(self, event):
        if self._dragging_index is None:
            return
        pos = self.transform_to_coord_sys(event.position())
        norm_control_point = self.scale_to_normalized(pos)
        self.bezier_control_points[self._dragging_index] = (
            norm_control_point[0],
            norm_control_point[1],
        )
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging_index = None
