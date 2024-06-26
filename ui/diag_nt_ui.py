# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_note.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from ui.modified import LPlainTextEdit
# QtWidgets.QPlainTextEdit = LPlainTextEdit

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(525, 260)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 220, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 501, 211))
        self.scrollArea.setStyleSheet("QScrollArea {\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 484, 214))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lb_title = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lb_title.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_title.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_title.setFont(font)
        self.lb_title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_title.setObjectName("lb_title")
        self.verticalLayout.addWidget(self.lb_title)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.textedit_title = LPlainTextEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_title.sizePolicy().hasHeightForWidth())
        self.textedit_title.setSizePolicy(sizePolicy)
        self.textedit_title.setMinimumSize(QtCore.QSize(0, 30))
        self.textedit_title.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textedit_title.setFont(font)
        self.textedit_title.setStyleSheet("QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_title.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_title.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_title.setPlainText("")
        self.textedit_title.setObjectName("textedit_title")
        self.horizontalLayout.addWidget(self.textedit_title)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lb_note = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lb_note.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_note.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_note.setFont(font)
        self.lb_note.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_note.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_note.setObjectName("lb_note")
        self.verticalLayout_2.addWidget(self.lb_note)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.textedit_note = LPlainTextEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_note.sizePolicy().hasHeightForWidth())
        self.textedit_note.setSizePolicy(sizePolicy)
        self.textedit_note.setMinimumSize(QtCore.QSize(0, 30))
        self.textedit_note.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textedit_note.setFont(font)
        self.textedit_note.setStyleSheet("QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_note.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_note.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_note.setPlainText("")
        self.textedit_note.setObjectName("textedit_note")
        self.horizontalLayout_2.addWidget(self.textedit_note)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lb_date = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lb_date.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_date.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_date.setFont(font)
        self.lb_date.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_date.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_date.setObjectName("lb_date")
        self.verticalLayout_3.addWidget(self.lb_date)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.textedit_date = LPlainTextEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_date.sizePolicy().hasHeightForWidth())
        self.textedit_date.setSizePolicy(sizePolicy)
        self.textedit_date.setMinimumSize(QtCore.QSize(0, 30))
        self.textedit_date.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textedit_date.setFont(font)
        self.textedit_date.setStyleSheet("QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_date.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_date.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_date.setPlainText("")
        self.textedit_date.setObjectName("textedit_date")
        self.horizontalLayout_3.addWidget(self.textedit_date)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lb_content = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lb_content.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_content.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_content.setFont(font)
        self.lb_content.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_content.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_content.setObjectName("lb_content")
        self.verticalLayout_4.addWidget(self.lb_content)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btn_add = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_add.setMinimumSize(QtCore.QSize(24, 24))
        self.btn_add.setMaximumSize(QtCore.QSize(24, 24))
        self.btn_add.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout_6.addWidget(self.btn_add)
        self.btn_rm = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_rm.setMinimumSize(QtCore.QSize(24, 24))
        self.btn_rm.setMaximumSize(QtCore.QSize(24, 24))
        self.btn_rm.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_rm.setIcon(icon1)
        self.btn_rm.setObjectName("btn_rm")
        self.verticalLayout_6.addWidget(self.btn_rm)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.list_content = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_content.sizePolicy().hasHeightForWidth())
        self.list_content.setSizePolicy(sizePolicy)
        self.list_content.setMinimumSize(QtCore.QSize(0, 80))
        self.list_content.setStyleSheet("QListWidget {\n"
"    background: transparent;\n"
"    border: none;\n"
"}")
        self.list_content.setObjectName("list_content")
        self.horizontalLayout_4.addWidget(self.list_content)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lb_title.setText(_translate("Dialog", "Title"))
        self.lb_note.setText(_translate("Dialog", "Note"))
        self.lb_date.setText(_translate("Dialog", "Date"))
        self.lb_content.setText(_translate("Dialog", "Content"))
import ui.res_rc
