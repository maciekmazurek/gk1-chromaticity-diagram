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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

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
        self.verticalLayout_2 = QVBoxLayout(self.spectralDistributionWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.XYZWidget = QWidget(self.spectralDistributionWidget)
        self.XYZWidget.setObjectName(u"XYZWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.XYZWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(471, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.XYZLabelsWidget = QWidget(self.XYZWidget)
        self.XYZLabelsWidget.setObjectName(u"XYZLabelsWidget")
        self.verticalLayout_3 = QVBoxLayout(self.XYZLabelsWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.XLabel = QLabel(self.XYZLabelsWidget)
        self.XLabel.setObjectName(u"XLabel")

        self.verticalLayout_3.addWidget(self.XLabel)

        self.YLabel = QLabel(self.XYZLabelsWidget)
        self.YLabel.setObjectName(u"YLabel")

        self.verticalLayout_3.addWidget(self.YLabel)

        self.ZLabel = QLabel(self.XYZLabelsWidget)
        self.ZLabel.setObjectName(u"ZLabel")

        self.verticalLayout_3.addWidget(self.ZLabel)


        self.horizontalLayout_5.addWidget(self.XYZLabelsWidget)


        self.verticalLayout_2.addWidget(self.XYZWidget)

        self.verticalSpacer_2 = QSpacerItem(20, 334, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_3.addWidget(self.spectralDistributionWidget)

        self.chromacityDiagramWidget = ChromacityDiagramWidget(self.centralwidget)
        self.chromacityDiagramWidget.setObjectName(u"chromacityDiagramWidget")
        sizePolicy.setHeightForWidth(self.chromacityDiagramWidget.sizePolicy().hasHeightForWidth())
        self.chromacityDiagramWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.chromacityDiagramWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.colorWidget = QWidget(self.chromacityDiagramWidget)
        self.colorWidget.setObjectName(u"colorWidget")
        self.horizontalLayout = QHBoxLayout(self.colorWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 5, 5, 0)
        self.horizontalSpacer = QSpacerItem(405, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.colorDescriptionLabel = QLabel(self.colorWidget)
        self.colorDescriptionLabel.setObjectName(u"colorDescriptionLabel")

        self.horizontalLayout.addWidget(self.colorDescriptionLabel)

        self.colorLabel = QLabel(self.colorWidget)
        self.colorLabel.setObjectName(u"colorLabel")
        self.colorLabel.setMinimumSize(QSize(50, 10))

        self.horizontalLayout.addWidget(self.colorLabel)


        self.verticalLayout.addWidget(self.colorWidget)

        self.gamutWidget = QWidget(self.chromacityDiagramWidget)
        self.gamutWidget.setObjectName(u"gamutWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.gamutWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 5, 0)
        self.horizontalSpacer_2 = QSpacerItem(303, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.gamutCheckBox = QCheckBox(self.gamutWidget)
        self.gamutCheckBox.setObjectName(u"gamutCheckBox")
        self.gamutCheckBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.gamutCheckBox)


        self.verticalLayout.addWidget(self.gamutWidget)

        self.spectralLocusWidget = QWidget(self.chromacityDiagramWidget)
        self.spectralLocusWidget.setObjectName(u"spectralLocusWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.spectralLocusWidget)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 5, 0)
        self.horizontalSpacer_3 = QSpacerItem(296, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.spectralLocusCheckBox = QCheckBox(self.spectralLocusWidget)
        self.spectralLocusCheckBox.setObjectName(u"spectralLocusCheckBox")
        self.spectralLocusCheckBox.setChecked(True)

        self.horizontalLayout_4.addWidget(self.spectralLocusCheckBox)


        self.verticalLayout.addWidget(self.spectralLocusWidget)

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
        self.XLabel.setText(QCoreApplication.translate("MainWindow", u"X:  ", None))
        self.YLabel.setText(QCoreApplication.translate("MainWindow", u"Y:  ", None))
        self.ZLabel.setText(QCoreApplication.translate("MainWindow", u"Z:  ", None))
        self.colorDescriptionLabel.setText(QCoreApplication.translate("MainWindow", u"Current Color:  ", None))
        self.colorLabel.setText("")
        self.gamutCheckBox.setText(QCoreApplication.translate("MainWindow", u"Show sRGB gamut", None))
        self.spectralLocusCheckBox.setText(QCoreApplication.translate("MainWindow", u"Show spectral locus", None))
    # retranslateUi

