# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_win.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStackedWidget, QStatusBar, QTabWidget,
    QTextBrowser, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)
import res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1023, 680)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.btn_search = QPushButton(self.centralwidget)
        self.btn_search.setObjectName(u"btn_search")
        self.btn_search.setGeometry(QRect(380, 50, 32, 32))
        self.btn_search.setStyleSheet(u"QPushButton {\n"
"    background-color: #E0E0E0;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #D3D3D3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #BEBEBE;\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u":/icons/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_search.setIcon(icon)
        self.textedit_search = QTextEdit(self.centralwidget)
        self.textedit_search.setObjectName(u"textedit_search")
        self.textedit_search.setEnabled(True)
        self.textedit_search.setGeometry(QRect(30, 50, 341, 32))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(9)
        self.textedit_search.setFont(font)
        self.textedit_search.setAcceptDrops(True)
        self.textedit_search.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit_search.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.btn_import = QPushButton(self.centralwidget)
        self.btn_import.setObjectName(u"btn_import")
        self.btn_import.setGeometry(QRect(30, 10, 88, 26))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_import.sizePolicy().hasHeightForWidth())
        self.btn_import.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setUnderline(False)
        self.btn_import.setFont(font1)
        self.btn_import.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.btn_import.setAutoFillBackground(False)
        self.btn_import.setStyleSheet(u"QPushButton {\n"
"    background-color: #4CAF50;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #45a049;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #397d3a;\n"
"}")
        self.btn_importb = QPushButton(self.centralwidget)
        self.btn_importb.setObjectName(u"btn_importb")
        self.btn_importb.setGeometry(QRect(130, 10, 88, 26))
        sizePolicy1.setHeightForWidth(self.btn_importb.sizePolicy().hasHeightForWidth())
        self.btn_importb.setSizePolicy(sizePolicy1)
        self.btn_importb.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.btn_importb.setStyleSheet(u"QPushButton {\n"
"    background-color: #4CAF50;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #45a049;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #397d3a;\n"
"}")
        self.btn_clear = QPushButton(self.centralwidget)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setGeometry(QRect(380, 90, 32, 32))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(16)
        font2.setBold(True)
        self.btn_clear.setFont(font2)
        self.btn_clear.setStyleSheet(u"QPushButton {\n"
"    background-color: #E0E0E0;\n"
"	color: red;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #D3D3D3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #BEBEBE;\n"
"}\n"
"")
        self.btn_addman = QPushButton(self.centralwidget)
        self.btn_addman.setObjectName(u"btn_addman")
        self.btn_addman.setGeometry(QRect(230, 10, 88, 26))
        sizePolicy1.setHeightForWidth(self.btn_addman.sizePolicy().hasHeightForWidth())
        self.btn_addman.setSizePolicy(sizePolicy1)
        self.btn_addman.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.btn_addman.setStyleSheet(u"QPushButton {\n"
"    background-color: #2196F3;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1E88E5;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1976D2;\n"
"}")
        self.btn_add_key = QPushButton(self.centralwidget)
        self.btn_add_key.setObjectName(u"btn_add_key")
        self.btn_add_key.setGeometry(QRect(330, 10, 88, 26))
        sizePolicy1.setHeightForWidth(self.btn_add_key.sizePolicy().hasHeightForWidth())
        self.btn_add_key.setSizePolicy(sizePolicy1)
        self.btn_add_key.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.btn_add_key.setStyleSheet(u"QPushButton {\n"
"    background-color: #FF5722;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #F4511E;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #E64A19;\n"
"}\n"
"")
        self.btn_add_note = QPushButton(self.centralwidget)
        self.btn_add_note.setObjectName(u"btn_add_note")
        self.btn_add_note.setGeometry(QRect(430, 10, 88, 26))
        sizePolicy1.setHeightForWidth(self.btn_add_note.sizePolicy().hasHeightForWidth())
        self.btn_add_note.setSizePolicy(sizePolicy1)
        self.btn_add_note.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.btn_add_note.setStyleSheet(u"QPushButton {\n"
"    background-color: #FF5722;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #F4511E;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #E64A19;\n"
"}\n"
"")
        self.btn_mdf = QPushButton(self.centralwidget)
        self.btn_mdf.setObjectName(u"btn_mdf")
        self.btn_mdf.setGeometry(QRect(530, 10, 88, 26))
        sizePolicy1.setHeightForWidth(self.btn_mdf.sizePolicy().hasHeightForWidth())
        self.btn_mdf.setSizePolicy(sizePolicy1)
        self.btn_mdf.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.btn_mdf.setStyleSheet(u"QPushButton {\n"
"    background-color: #9C27B0;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #8E24AA;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7B1FA2;\n"
"}")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(420, 50, 571, 571))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.browser_main = QTextBrowser(self.page)
        self.browser_main.setObjectName(u"browser_main")
        self.browser_main.setGeometry(QRect(0, 0, 571, 421))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(12)
        self.browser_main.setFont(font3)
        self.browser_cmd = QTextBrowser(self.page)
        self.browser_cmd.setObjectName(u"browser_cmd")
        self.browser_cmd.setGeometry(QRect(0, 430, 571, 141))
        self.browser_cmd.setStyleSheet(u"QTextBrowser {\n"
"    background-color: black;\n"
"    color: white;\n"
"    font-family: Consolas, monospace;\n"
"}")
        self.browser_cmd.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.browser_info = QTextBrowser(self.page_2)
        self.browser_info.setObjectName(u"browser_info")
        self.browser_info.setGeometry(QRect(0, 0, 571, 201))
        self.browser_info.setFont(font3)
        self.list_notes = QListWidget(self.page_2)
        self.list_notes.setObjectName(u"list_notes")
        self.list_notes.setGeometry(QRect(0, 310, 571, 261))
        self.browser_kwd = QTextBrowser(self.page_2)
        self.browser_kwd.setObjectName(u"browser_kwd")
        self.browser_kwd.setGeometry(QRect(0, 210, 571, 91))
        self.browser_kwd.setFont(font3)
        self.stackedWidget.addWidget(self.page_2)
        self.btn_download = QPushButton(self.centralwidget)
        self.btn_download.setObjectName(u"btn_download")
        self.btn_download.setGeometry(QRect(900, 10, 88, 26))
        sizePolicy1.setHeightForWidth(self.btn_download.sizePolicy().hasHeightForWidth())
        self.btn_download.setSizePolicy(sizePolicy1)
        self.btn_download.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.btn_download.setStyleSheet(u"QPushButton {\n"
"    background-color: #5f5f5f;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4f4f4f;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3f3f3f;\n"
"}\n"
"")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(30, 40, 961, 16))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(30, 109, 381, 515))
        self.tab_tree = QWidget()
        self.tab_tree.setObjectName(u"tab_tree")
        self.verticalLayout_2 = QVBoxLayout(self.tab_tree)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.tree_root = QTreeWidget(self.tab_tree)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_root.setHeaderItem(__qtreewidgetitem)
        self.tree_root.setObjectName(u"tree_root")
        self.tree_root.setHeaderHidden(True)
        self.tree_root.header().setVisible(False)

        self.verticalLayout_2.addWidget(self.tree_root)

        self.tabWidget.addTab(self.tab_tree, "")
        self.tab_search = QWidget()
        self.tab_search.setObjectName(u"tab_search")
        self.verticalLayout = QVBoxLayout(self.tab_search)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.list_searchs = QListWidget(self.tab_search)
        self.list_searchs.setObjectName(u"list_searchs")

        self.verticalLayout.addWidget(self.list_searchs)

        self.tabWidget.addTab(self.tab_search, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.list_articles = QListWidget(self.tab)
        self.list_articles.setObjectName(u"list_articles")

        self.verticalLayout_3.addWidget(self.list_articles)

        self.tabWidget.addTab(self.tab, "")
        self.btn_sync = QPushButton(self.centralwidget)
        self.btn_sync.setObjectName(u"btn_sync")
        self.btn_sync.setGeometry(QRect(840, 10, 25, 25))
        sizePolicy.setHeightForWidth(self.btn_sync.sizePolicy().hasHeightForWidth())
        self.btn_sync.setSizePolicy(sizePolicy)
        self.btn_sync.setStyleSheet(u"QPushButton {\n"
"    background-color: #E0E0E0;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #D3D3D3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #BEBEBE;\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/synchron_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_sync.setIcon(icon1)
        self.btn_sync_r = QPushButton(self.centralwidget)
        self.btn_sync_r.setObjectName(u"btn_sync_r")
        self.btn_sync_r.setGeometry(QRect(870, 10, 25, 25))
        sizePolicy.setHeightForWidth(self.btn_sync_r.sizePolicy().hasHeightForWidth())
        self.btn_sync_r.setSizePolicy(sizePolicy)
        self.btn_sync_r.setStyleSheet(u"QPushButton {\n"
"    background-color: #E0E0E0;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #D3D3D3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #BEBEBE;\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/synchron_red.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_sync_r.setIcon(icon2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.btn_search.raise_()
        self.textedit_search.raise_()
        self.btn_import.raise_()
        self.btn_importb.raise_()
        self.btn_addman.raise_()
        self.btn_add_key.raise_()
        self.btn_add_note.raise_()
        self.btn_mdf.raise_()
        self.stackedWidget.raise_()
        self.btn_download.raise_()
        self.line.raise_()
        self.tabWidget.raise_()
        self.btn_clear.raise_()
        self.btn_sync.raise_()
        self.btn_sync_r.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1023, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setMouseTracking(False)
        self.statusbar.setTabletTracking(True)
        self.statusbar.setAutoFillBackground(False)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_search.setText("")
        self.textedit_search.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Arial'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">input the text</p></body></html>", None))
        self.btn_import.setText(QCoreApplication.translate("MainWindow", u"Import Paper", None))
        self.btn_importb.setText(QCoreApplication.translate("MainWindow", u"Import Batch", None))
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.btn_addman.setText(QCoreApplication.translate("MainWindow", u"Add Manually", None))
        self.btn_add_key.setText(QCoreApplication.translate("MainWindow", u"Add Keywords", None))
        self.btn_add_note.setText(QCoreApplication.translate("MainWindow", u"Add Notes", None))
        self.btn_mdf.setText(QCoreApplication.translate("MainWindow", u"Modified", None))
        self.browser_cmd.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Consolas','monospace'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.btn_download.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_tree), QCoreApplication.translate("MainWindow", u"Tree View", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_search), QCoreApplication.translate("MainWindow", u"Search Page", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Repository", None))
        self.btn_sync.setText("")
        self.btn_sync_r.setText("")
    # retranslateUi

