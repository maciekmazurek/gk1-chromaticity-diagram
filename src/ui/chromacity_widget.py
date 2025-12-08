from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QPainter

from utils import get_path_from_resources

class ChromacityDiagramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = QPixmap(get_path_from_resources("cie_xyz.png"))
        # Współrzędne piksela będącego środkiem układu współrzędnych na obrazie cie_xyz.png
        self.origin_x = 145
        self.origin_y = 1153
        # Ile pikseli przypada na jednostkę 0.1 w układzie współrzędnych z obrazu cie_xyz.png
        self.scale = 63

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, self.background_image)