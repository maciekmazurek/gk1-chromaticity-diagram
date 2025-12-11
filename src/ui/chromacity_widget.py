from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap, Qt
from PySide6.QtWidgets import QWidget

from utils import get_path_from_resources, load_color_matching_funcs


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
            self.draw_spectral_locus(painter)
            self.draw_sRGB_gamut(painter)
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

    def draw_circle(self, painter: QPainter, x: float, y: float, radius_px: int):
        diameter_px = radius_px * 2
        painter.drawEllipse(
            x * self.coord_scale - radius_px,
            y * self.coord_scale - radius_px,
            diameter_px,
            diameter_px,
        )

    def draw_chromacity_point(self, painter: QPainter):
        x, y, _ = self.calc_xyz_values()
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        self.draw_circle(painter, x, y, 4)

    def draw_spectral_locus(self, painter: QPainter):
        locus_points = self.calc_spectral_locus_points()
        for point in locus_points:
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
            X, Y, Z = self.xyY_to_XYZ(x, y, 1.0)
            r, g, b = self.XYZ_to_sRGB(X, Y, Z)
            locus_points.append((x, y, QColor(r, g, b)))

        return locus_points

    def xyY_to_XYZ(self, x: float, y: float, Y: float) -> tuple[float, float, float]:
        if y <= 0:
            return (0.0, 0.0, 0.0)
        X = x * Y / y
        Z = (1.0 - x - y) * Y / y
        return (X, Y, Z)

    def XYZ_to_sRGB(self, X: float, Y: float, Z: float) -> tuple[int, int, int]:
        # macierz XYZ -> linear sRGB (D65)
        r_linear = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
        g_linear = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
        b_linear = 0.0557 * X - 0.2040 * Y + 1.0570 * Z

        def sRGB_gamma_correct(color_val: float) -> float:
            color_val = max(0.0, min(1.0, color_val))
            if color_val <= 0.0031308:
                return 12.92 * color_val
            else:
                return 1.055 * (color_val ** (1.0 / 2.4)) - 0.055

        r = max(0.0, min(1.0, sRGB_gamma_correct(r_linear)))
        g = max(0.0, min(1.0, sRGB_gamma_correct(g_linear)))
        b = max(0.0, min(1.0, sRGB_gamma_correct(b_linear)))

        return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))

    def draw_sRGB_gamut(self, painter: QPainter):
        # Współrzędne 3 barw podstawowych - czerwony, zielony, niebieski
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
