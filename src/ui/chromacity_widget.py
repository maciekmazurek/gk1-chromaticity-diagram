from multiprocessing.sharedctypes import Synchronized
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap, Qt
from PySide6.QtWidgets import QWidget

from utils import get_path_from_resources


class ChromacityDiagramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        diagram_image_original = QPixmap(get_path_from_resources("cie_xyz.png"))
        # Współrzędne piksela będącego środkiem układu współrzędnych w
        # oryginalnym obrazie
        coord_origin_x_original = 145
        coord_origin_y_original = 1153
        # Liczba pikseli przypadająca na długość zakresu [0.0, 1.0] w układzie
        # współrzędnych z oryginalnego obrazu
        coord_scale_original = 1220
        # Stała, dopasowana wysokość i szerokość obrazka oraz przesunięcie we
        # współrzędnej Y-owej, tak aby obraz ładnie wpasowywał się w widget
        fitted_width = 450
        fitted_height = 440
        self.fitted_offset_y = 30

        self.diagram_image = diagram_image_original.scaled(
            fitted_width, fitted_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        scale_factor = self.diagram_image.width() / diagram_image_original.width()
        self.coord_origin_x = int(coord_origin_x_original * scale_factor)
        self.coord_origin_y = int(coord_origin_y_original * scale_factor)
        self.coord_scale = coord_scale_original * scale_factor

        self.XYZ = [0.0, 0.0, 0.0]

    def set_XYZ(self, XYZ: list[float]):
        self.XYZ = XYZ
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(0, self.fitted_offset_y, self.diagram_image)
            self.setup_coord_system_origin(painter)
            self.draw_chromacity_point(painter)
        finally:
            painter.end()

    def setup_coord_system_origin(self, painter: QPainter):
        painter.translate(
            self.coord_origin_x, self.coord_origin_y + self.fitted_offset_y
        )
        painter.scale(1, -1)

    def calc_xyz_values(self) -> tuple[float]:
        XYZ_sum = sum(self.XYZ)
        x = self.XYZ[0] / XYZ_sum
        y = self.XYZ[1] / XYZ_sum
        z = self.XYZ[2] / XYZ_sum
        return (x, y, z)

    def draw_chromacity_point(self, painter: QPainter):
        x, y, _ = self.calc_xyz_values()
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        radius_px = 4
        diameter_px = 2 * radius_px
        painter.drawEllipse(
            x * self.coord_scale - radius_px,
            y * self.coord_scale - radius_px,
            diameter_px,
            diameter_px,
        )
