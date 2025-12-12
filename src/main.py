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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
