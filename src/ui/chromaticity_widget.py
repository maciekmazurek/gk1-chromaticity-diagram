from PySide6.QtCore import Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap, Qt
from PySide6.QtWidgets import QWidget

from utils import get_path_from_resources, load_color_matching_funcs
from color.space import xyY_to_XYZ, XYZ_to_sRGB


class ChromaticityDiagramWidget(QWidget):
    colorChanged = Signal(tuple)

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

        self.chromaticity_point_XYZ = [0.0, 0.0, 0.0]

        self.show_gamut = True
        self.show_spectral_locus = True

        self.locus_points = self.calc_spectral_locus_points()

    def set_XYZ(self, XYZ: list[float]):
        self.chromaticity_point_XYZ = XYZ
        self.colorChanged.emit(self.calc_current_RGB_val())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(0, self.fitted_offset_y, self.diagram_image)
            self.setup_coord_system_origin(painter)
            if self.show_spectral_locus:
                self.draw_spectral_locus(painter)
            if self.show_gamut:
                self.draw_sRGB_gamut(painter)
            self.draw_chromaticity_point(painter)
        finally:
            painter.end()

    def setup_coord_system_origin(self, painter: QPainter):
        painter.translate(
            self.coord_origin_x, self.coord_origin_y + self.fitted_offset_y
        )
        painter.scale(1, -1)

    def calc_chromaticity_point_xyz_values(self) -> tuple[float, float, float]:
        XYZ_sum = sum(self.chromaticity_point_XYZ)
        x = self.chromaticity_point_XYZ[0] / XYZ_sum
        y = self.chromaticity_point_XYZ[1] / XYZ_sum
        z = self.chromaticity_point_XYZ[2] / XYZ_sum
        return (x, y, z)

    def draw_circle(self, painter: QPainter, x: float, y: float, radius_px: int):
        diameter_px = radius_px * 2
        painter.drawEllipse(
            x * self.coord_scale - radius_px,
            y * self.coord_scale - radius_px,
            diameter_px,
            diameter_px,
        )

    def draw_chromaticity_point(self, painter: QPainter):
        x, y, _ = self.calc_chromaticity_point_xyz_values()
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        try:
            self.draw_circle(painter, x, y, 4)
            self.draw_chromaticity_point_text(
                painter, x, y, f"(x={round(x, 2)},y={round(y, 2)})"
            )
        except OverflowError:
            pass

    def draw_chromaticity_point_text(
        self, painter: QPainter, x: float, y: float, text: str
    ):
        painter.save()
        # Odwracamy układ, aby napis nie był odwrócony do góry nogami
        painter.scale(1, -1)
        font = painter.font()
        font.setPointSize(8)
        font.setBold(True)
        painter.setFont(font)
        shift = 10
        x_scaled = x * self.coord_scale + shift
        y_scaled = -(y * self.coord_scale) - shift
        painter.drawText(x_scaled, y_scaled, text)
        painter.restore()

    def draw_spectral_locus(self, painter: QPainter):
        for point in self.locus_points:
            x = point[0]
            y = point[1]
            color = point[2]
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color))
            self.draw_circle(painter, x, y, 2)

    def calc_spectral_locus_points(self) -> list[tuple[float, float, QColor]]:
        wavelenghts, cmfs_values = load_color_matching_funcs()
        locus_points = []

        # Ucinamy zakres aby dopasować dane do obrazka
        mask = wavelenghts <= 680
        cmfs_values = cmfs_values[mask]

        for cmf_x_val, cmf_y_val, cmf_z_val in cmfs_values:
            XYZ_sum = cmf_x_val + cmf_y_val + cmf_z_val
            if XYZ_sum == 0:
                continue
            x = cmf_x_val / XYZ_sum
            y = cmf_y_val / XYZ_sum
            X, Y, Z = xyY_to_XYZ(x, y, 1.0)
            r, g, b = XYZ_to_sRGB(X, Y, Z)
            locus_points.append((x, y, QColor(r, g, b)))

        return locus_points

    def draw_sRGB_gamut(self, painter: QPainter):
        # Współrzędne 3 barw podstawowych na diagramie chromatyczności
        # (kolejno czerwony, zielony, niebieski)
        primary_colors_coords = [(0.64, 0.33), (0.3, 0.6), (0.15, 0.06)]
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QPen(QColor(0, 0, 0)))

        for x, y in primary_colors_coords:
            self.draw_circle(painter, x, y, 2)

        lines = [
            (primary_colors_coords[0], primary_colors_coords[1]),
            (primary_colors_coords[1], primary_colors_coords[2]),
            (primary_colors_coords[2], primary_colors_coords[0]),
        ]
        for (x1, y1), (x2, y2) in lines:
            painter.drawLine(
                x1 * self.coord_scale,
                y1 * self.coord_scale,
                x2 * self.coord_scale,
                y2 * self.coord_scale,
            )

    def calc_current_RGB_val(self) -> tuple[int]:
        x, y, _ = self.calc_chromaticity_point_xyz_values()
        X, Y, Z = xyY_to_XYZ(x, y, 1.0)
        r, g, b = XYZ_to_sRGB(X, Y, Z)
        return (r, g, b)

    def set_show_gamut(self, checked: bool):
        self.show_gamut = checked
        self.update()

    def set_show_spectral_locus(self, checked: bool):
        self.show_spectral_locus = checked
        self.update()
