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
    QMenuBar, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

from .chromacity_widget import ChromacityDiagramWidget
from .spectral_widget import SpectralDistributionWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 500)
        MainWindow.setMinimumSize(QSize(1000, 500))
        MainWindow.setMaximumSize(QSize(1000, 500))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.spectralDistributionWidget = SpectralDistributionWidget(self.centralwidget)
        self.spectralDistributionWidget.setObjectName(u"spectralDistributionWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spectralDistributionWidget.sizePolicy().hasHeightForWidth())
        self.spectralDistributionWidget.setSizePolicy(sizePolicy)
        self.spectralDistributionWidget.setMinimumSize(QSize(550, 0))

        self.horizontalLayout_3.addWidget(self.spectralDistributionWidget)

        self.chromacityDiagramWidget = ChromacityDiagramWidget(self.centralwidget)
        self.chromacityDiagramWidget.setObjectName(u"chromacityDiagramWidget")
        sizePolicy.setHeightForWidth(self.chromacityDiagramWidget.sizePolicy().hasHeightForWidth())
        self.chromacityDiagramWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.chromacityDiagramWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.diagramWidget = QWidget(self.chromacityDiagramWidget)
        self.diagramWidget.setObjectName(u"diagramWidget")
        self.horizontalLayout = QHBoxLayout(self.diagramWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(405, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.colorLabel = QLabel(self.diagramWidget)
        self.colorLabel.setObjectName(u"colorLabel")
        self.colorLabel.setMinimumSize(QSize(50, 10))

        self.horizontalLayout.addWidget(self.colorLabel)


        self.verticalLayout.addWidget(self.diagramWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addWidget(self.chromacityDiagramWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"gk1-chromacity-diagram", None))
        self.colorLabel.setText("")
    # retranslateUi

