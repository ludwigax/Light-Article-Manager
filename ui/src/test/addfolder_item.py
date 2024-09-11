# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addfolder_item.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(478, 28)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.btn_add = QPushButton(Form)
        self.btn_add.setObjectName(u"btn_add")
        self.btn_add.setMinimumSize(QSize(0, 24))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(True)
        self.btn_add.setFont(font)
        self.btn_add.setStyleSheet(u"QPushButton {\n"
"    background-color: #deffde;\n"
"    border: none;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #cdffcd;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #c4ffc4;\n"
"}")

        self.horizontalLayout.addWidget(self.btn_add)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_add.setText(QCoreApplication.translate("Form", u"Add New Folder", None))
    # retranslateUi

