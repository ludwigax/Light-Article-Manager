# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'check_item.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QSizePolicy, QWidget)
import res_rc
import res_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(478, 28)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.btn_check = QCheckBox(Form)
        self.btn_check.setObjectName(u"btn_check")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_check.sizePolicy().hasHeightForWidth())
        self.btn_check.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.btn_check)

        self.lb_icon = QLabel(Form)
        self.lb_icon.setObjectName(u"lb_icon")
        sizePolicy1.setHeightForWidth(self.lb_icon.sizePolicy().hasHeightForWidth())
        self.lb_icon.setSizePolicy(sizePolicy1)
        self.lb_icon.setMinimumSize(QSize(24, 24))
        self.lb_icon.setMaximumSize(QSize(24, 24))
        self.lb_icon.setPixmap(QPixmap(u":/icons/google-docs.png"))
        self.lb_icon.setScaledContents(False)
        self.lb_icon.setMargin(0)

        self.horizontalLayout.addWidget(self.lb_icon)

        self.lb_title = QLabel(Form)
        self.lb_title.setObjectName(u"lb_title")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(True)
        self.lb_title.setFont(font)

        self.horizontalLayout.addWidget(self.lb_title)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_check.setText("")
        self.lb_icon.setText("")
        self.lb_title.setText("")
    # retranslateUi

