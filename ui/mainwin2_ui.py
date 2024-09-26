# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_win_new.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)
import ui.res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1148, 780)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionImport_article = QAction(MainWindow)
        self.actionImport_article.setObjectName(u"actionImport_article")
        self.actionImport_article.setIconVisibleInMenu(True)
        self.actionImport_batch = QAction(MainWindow)
        self.actionImport_batch.setObjectName(u"actionImport_batch")
        self.actionImport_manually = QAction(MainWindow)
        self.actionImport_manually.setObjectName(u"actionImport_manually")
        self.actionLoad_Library = QAction(MainWindow)
        self.actionLoad_Library.setObjectName(u"actionLoad_Library")
        self.actionDump_Library = QAction(MainWindow)
        self.actionDump_Library.setObjectName(u"actionDump_Library")
        self.actionMicrosoft_Modern = QAction(MainWindow)
        self.actionMicrosoft_Modern.setObjectName(u"actionMicrosoft_Modern")
        self.actionSave_layout = QAction(MainWindow)
        self.actionSave_layout.setObjectName(u"actionSave_layout")
        self.actionMain_Browser = QAction(MainWindow)
        self.actionMain_Browser.setObjectName(u"actionMain_Browser")
        self.actionNote_Browser = QAction(MainWindow)
        self.actionNote_Browser.setObjectName(u"actionNote_Browser")
        self.actionNote_View = QAction(MainWindow)
        self.actionNote_View.setObjectName(u"actionNote_View")
        self.actionAdvanced_Search = QAction(MainWindow)
        self.actionAdvanced_Search.setObjectName(u"actionAdvanced_Search")
        self.actionOnline_Search = QAction(MainWindow)
        self.actionOnline_Search.setObjectName(u"actionOnline_Search")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.workwidget = QWidget(self.centralwidget)
        self.workwidget.setObjectName(u"workwidget")
        self.horizontalLayout = QHBoxLayout(self.workwidget)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetL = QWidget(self.workwidget)
        self.widgetL.setObjectName(u"widgetL")

        self.horizontalLayout.addWidget(self.widgetL)

        self.widgetR = QWidget(self.workwidget)
        self.widgetR.setObjectName(u"widgetR")

        self.horizontalLayout.addWidget(self.widgetR)

        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 6)

        self.verticalLayout.addWidget(self.workwidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1023, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setGeometry(QRect(269, 129, 155, 169))
        self.menuFile.setMinimumSize(QSize(120, 0))
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuEdit.setGeometry(QRect(304, 129, 120, 50))
        self.menuEdit.setMinimumSize(QSize(120, 0))
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuTheme = QMenu(self.menuView)
        self.menuTheme.setObjectName(u"menuTheme")
        self.menuRecover_layout = QMenu(self.menuView)
        self.menuRecover_layout.setObjectName(u"menuRecover_layout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setMouseTracking(False)
        self.statusbar.setTabletTracking(True)
        self.statusbar.setAutoFillBackground(False)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionImport_article)
        self.menuFile.addAction(self.actionImport_batch)
        self.menuFile.addAction(self.actionImport_manually)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_Library)
        self.menuFile.addAction(self.actionDump_Library)
        self.menuView.addAction(self.menuTheme.menuAction())
        self.menuView.addAction(self.menuRecover_layout.menuAction())
        self.menuView.addAction(self.actionSave_layout)
        self.menuTheme.addAction(self.actionMicrosoft_Modern)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionImport_article.setText(QCoreApplication.translate("MainWindow", u"Import article", None))
        self.actionImport_batch.setText(QCoreApplication.translate("MainWindow", u"Import batch", None))
        self.actionImport_manually.setText(QCoreApplication.translate("MainWindow", u"Import manually", None))
        self.actionLoad_Library.setText(QCoreApplication.translate("MainWindow", u"Load Library", None))
        self.actionDump_Library.setText(QCoreApplication.translate("MainWindow", u"Dump Library", None))
        self.actionMicrosoft_Modern.setText(QCoreApplication.translate("MainWindow", u"Microsoft Modern", None))
        self.actionSave_layout.setText(QCoreApplication.translate("MainWindow", u"Save layout", None))
        self.actionMain_Browser.setText(QCoreApplication.translate("MainWindow", u"Main Browser", None))
        self.actionNote_Browser.setText(QCoreApplication.translate("MainWindow", u"Note Browser", None))
        self.actionNote_View.setText(QCoreApplication.translate("MainWindow", u"Note View", None))
        self.actionAdvanced_Search.setText(QCoreApplication.translate("MainWindow", u"Advanced Search", None))
        self.actionOnline_Search.setText(QCoreApplication.translate("MainWindow", u"Online Search", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuTheme.setTitle(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.menuRecover_layout.setTitle(QCoreApplication.translate("MainWindow", u"Recover layout", None))
    # retranslateUi

