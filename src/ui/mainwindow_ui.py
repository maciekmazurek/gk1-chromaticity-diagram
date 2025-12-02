# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QVBoxLayout, QWidget)

from .chromacity_widget import ChromacityDiagramWidget
from .spectral_widget import SpectralDistributionWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spectralDistributionWidget = SpectralDistributionWidget(self.centralwidget)
        self.spectralDistributionWidget.setObjectName(u"spectralDistributionWidget")
        self.verticalLayout = QVBoxLayout(self.spectralDistributionWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bezierPointsWidget = QWidget(self.spectralDistributionWidget)
        self.bezierPointsWidget.setObjectName(u"bezierPointsWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.bezierPointsWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.label = QLabel(self.bezierPointsWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.spinBox = QSpinBox(self.bezierPointsWidget)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_4.addWidget(self.spinBox)


        self.verticalLayout.addWidget(self.bezierPointsWidget)

        self.verticalSpacer = QSpacerItem(20, 469, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addWidget(self.spectralDistributionWidget)

        self.chromacityDiagramWidget = ChromacityDiagramWidget(self.centralwidget)
        self.chromacityDiagramWidget.setObjectName(u"chromacityDiagramWidget")

        self.horizontalLayout_3.addWidget(self.chromacityDiagramWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"gk1-chromacity-diagram", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Number of points:", None))
    # retranslateUi

