# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_item.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QPushButton,
    QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout,
    QWidget)
import res_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(474, 74)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(0, 74))
        Form.setMaximumSize(QSize(16777215, 74))
        Form.setWindowOpacity(1.000000000000000)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.browser = QTextBrowser(Form)
        self.browser.setObjectName(u"browser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.browser.sizePolicy().hasHeightForWidth())
        self.browser.setSizePolicy(sizePolicy1)
        self.browser.setMinimumSize(QSize(0, 70))
        self.browser.setMaximumSize(QSize(16777215, 70))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        self.browser.setFont(font)
        self.browser.setStyleSheet(u"QTextBrowser {\n"
"    border: 2px solid #32CD32;\n"
"    background-color: white;\n"
"}")

        self.horizontalLayout.addWidget(self.browser)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_del = QPushButton(Form)
        self.btn_del.setObjectName(u"btn_del")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_del.sizePolicy().hasHeightForWidth())
        self.btn_del.setSizePolicy(sizePolicy2)
        self.btn_del.setMinimumSize(QSize(32, 32))
        self.btn_del.setMaximumSize(QSize(32, 32))
        self.btn_del.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.btn_del.setStyleSheet(u"QPushButton {\n"
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
        icon.addFile(u":/icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/icons/delete_on.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.btn_del.setIcon(icon)
        self.btn_del.setIconSize(QSize(20, 20))

        self.verticalLayout.addWidget(self.btn_del)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_del.setText("")
    # retranslateUi

