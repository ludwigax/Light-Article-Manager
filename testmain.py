# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QToolBar, QWidget)

class Ui_CMainWindow(object):
    def setupUi(self, CMainWindow):
        if not CMainWindow.objectName():
            CMainWindow.setObjectName(u"CMainWindow")
        CMainWindow.resize(1284, 757)
        self.centralwidget = QWidget(CMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        CMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1284, 21))
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        CMainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(CMainWindow)
        self.toolBar.setObjectName(u"toolBar")
        CMainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(CMainWindow)

        QMetaObject.connectSlotsByName(CMainWindow)
    # setupUi

    def retranslateUi(self, CMainWindow):
        CMainWindow.setWindowTitle(QCoreApplication.translate("CMainWindow", u"MainWindow", None))
        self.menuView.setTitle(QCoreApplication.translate("CMainWindow", u"View", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("CMainWindow", u"toolBar", None))
    # retranslateUi

