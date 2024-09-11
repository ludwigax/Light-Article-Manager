# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'folder_item.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QStackedWidget, QWidget)
import res_rc
import res_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(477, 28)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.lb_icon = QLabel(Form)
        self.lb_icon.setObjectName(u"lb_icon")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lb_icon.sizePolicy().hasHeightForWidth())
        self.lb_icon.setSizePolicy(sizePolicy1)
        self.lb_icon.setMinimumSize(QSize(24, 24))
        self.lb_icon.setMaximumSize(QSize(24, 24))
        self.lb_icon.setPixmap(QPixmap(u":/icons/open-folder.png"))
        self.lb_icon.setScaledContents(False)
        self.lb_icon.setMargin(0)

        self.horizontalLayout.addWidget(self.lb_icon)

        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(True)
        self.stackedWidget.setFont(font)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_3 = QHBoxLayout(self.page)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lb_folder = QLabel(self.page)
        self.lb_folder.setObjectName(u"lb_folder")
        self.lb_folder.setFont(font)

        self.horizontalLayout_3.addWidget(self.lb_folder)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_2 = QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.edit_folder = QLineEdit(self.page_2)
        self.edit_folder.setObjectName(u"edit_folder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.edit_folder.sizePolicy().hasHeightForWidth())
        self.edit_folder.setSizePolicy(sizePolicy2)
        self.edit_folder.setFont(font)
        self.edit_folder.setStyleSheet(u"QLineEdit {\n"
"    border: none;\n"
"}")

        self.horizontalLayout_2.addWidget(self.edit_folder)

        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)

        self.btn_add = QPushButton(Form)
        self.btn_add.setObjectName(u"btn_add")
        sizePolicy1.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy1)
        self.btn_add.setMinimumSize(QSize(24, 24))
        self.btn_add.setMaximumSize(QSize(24, 24))
        self.btn_add.setAutoFillBackground(False)
        self.btn_add.setStyleSheet(u"QPushButton {\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u":/icons/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btn_add)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lb_icon.setText("")
        self.lb_folder.setText("")
        self.btn_add.setText("")
    # retranslateUi

