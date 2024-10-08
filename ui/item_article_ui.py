# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'article_item.ui'
#
# Created by: PySide6 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets

from ui.modified import LLabel
# QtWidgets.QLabel = LLabel

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(478, 28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lb_icon = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_icon.sizePolicy().hasHeightForWidth())
        self.lb_icon.setSizePolicy(sizePolicy)
        self.lb_icon.setMinimumSize(QtCore.QSize(24, 24))
        self.lb_icon.setMaximumSize(QtCore.QSize(24, 24))
        self.lb_icon.setText("")
        self.lb_icon.setPixmap(QtGui.QPixmap(":/icons/google-docs.png"))
        self.lb_icon.setScaledContents(False)
        self.lb_icon.setObjectName("lb_icon")
        self.horizontalLayout.addWidget(self.lb_icon)
        self.lb_title = LLabel(Form) # ludwig modified
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_title.setFont(font)
        self.lb_title.setText("")
        self.lb_title.setObjectName("lb_title")
        self.horizontalLayout.addWidget(self.lb_title)
        self.btn_del = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_del.sizePolicy().hasHeightForWidth())
        self.btn_del.setSizePolicy(sizePolicy)
        self.btn_del.setMinimumSize(QtCore.QSize(24, 24))
        self.btn_del.setMaximumSize(QtCore.QSize(24, 24))
        self.btn_del.setStyleSheet("QPushButton {\n"
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
        self.btn_del.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_del.setIcon(icon)
        self.btn_del.setIconSize(QtCore.QSize(24, 24))
        self.btn_del.setObjectName("btn_del")
        self.horizontalLayout.addWidget(self.btn_del)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
import ui.res_rc
