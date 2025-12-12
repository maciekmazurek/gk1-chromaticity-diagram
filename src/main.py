import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui.mainwindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_slots()

    def setup_slots(self):
        self.spectralDistributionWidget.XYZChanged.connect(
            self.chromacityDiagramWidget.set_XYZ
        )
        self.gamutCheckBox.toggled.connect(self.chromacityDiagramWidget.set_show_gamut)
        self.spectralLocusCheckBox.toggled.connect(
            self.chromacityDiagramWidget.set_show_spectral_locus
        )
        self.chromacityDiagramWidget.colorChanged.connect(self.update_color_label)
        self.spectralDistributionWidget.XYZChanged.connect(self.update_XYZ_labels)

    def update_color_label(self, rgb: tuple[int]):
        self.colorLabel.setStyleSheet(
            f"background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]}); border: 1px solid black;"
        )

    def update_XYZ_labels(self, XYZ: list[float]):
        x, y, z = (float(XYZ[0]), float(XYZ[1]), float(XYZ[2]))
        self.XLabel.setText(f"X:  {x:.3f}")
        self.YLabel.setText(f"Y:  {y:.3f}")
        self.ZLabel.setText(f"Z:  {z:.3f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
