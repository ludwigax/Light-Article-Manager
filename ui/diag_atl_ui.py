# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Ludwig\Python Code\pyarticle_prj\ui\src\add_diag.ui'
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
        Dialog.resize(553, 368)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 330, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 511, 301))
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 511, 301))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lb_title = QtWidgets.QLabel(self.widget)
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
        self.verticalLayout_2.addWidget(self.lb_title)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.textedit_title = LPlainTextEdit(self.widget) # ludwig modified
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
        self.verticalLayout_8.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lb_author = QtWidgets.QLabel(self.widget_2)
        self.lb_author.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_author.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_author.setFont(font)
        self.lb_author.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_author.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_author.setObjectName("lb_author")
        self.verticalLayout_3.addWidget(self.lb_author)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.textedit_author = LPlainTextEdit(self.widget_2) # ludwig modified
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_author.sizePolicy().hasHeightForWidth())
        self.textedit_author.setSizePolicy(sizePolicy)
        self.textedit_author.setMinimumSize(QtCore.QSize(0, 30))
        self.textedit_author.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textedit_author.setFont(font)
        self.textedit_author.setStyleSheet("QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_author.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_author.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_author.setPlainText("")
        self.textedit_author.setObjectName("textedit_author")
        self.horizontalLayout_3.addWidget(self.textedit_author)
        self.verticalLayout_8.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lb_journal = QtWidgets.QLabel(self.widget_3)
        self.lb_journal.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_journal.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_journal.setFont(font)
        self.lb_journal.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_journal.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_journal.setObjectName("lb_journal")
        self.verticalLayout_4.addWidget(self.lb_journal)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.textedit_journal = LPlainTextEdit(self.widget_3) # ludwig modified
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_journal.sizePolicy().hasHeightForWidth())
        self.textedit_journal.setSizePolicy(sizePolicy)
        self.textedit_journal.setMinimumSize(QtCore.QSize(0, 30))
        self.textedit_journal.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textedit_journal.setFont(font)
        self.textedit_journal.setStyleSheet("QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_journal.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_journal.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_journal.setPlainText("")
        self.textedit_journal.setObjectName("textedit_journal")
        self.horizontalLayout_4.addWidget(self.textedit_journal)
        self.verticalLayout_8.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lb_year = QtWidgets.QLabel(self.widget_4)
        self.lb_year.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_year.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_year.setFont(font)
        self.lb_year.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_year.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_year.setObjectName("lb_year")
        self.verticalLayout_5.addWidget(self.lb_year)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_5.addItem(spacerItem3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.textedit_year = LPlainTextEdit(self.widget_4) # ludwig modified
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_year.sizePolicy().hasHeightForWidth())
        self.textedit_year.setSizePolicy(sizePolicy)
        self.textedit_year.setMinimumSize(QtCore.QSize(0, 30))
        self.textedit_year.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textedit_year.setFont(font)
        self.textedit_year.setStyleSheet("QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_year.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_year.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_year.setPlainText("")
        self.textedit_year.setObjectName("textedit_year")
        self.horizontalLayout_5.addWidget(self.textedit_year)
        self.verticalLayout_8.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lb_doi = QtWidgets.QLabel(self.widget_5)
        self.lb_doi.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_doi.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_doi.setFont(font)
        self.lb_doi.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_doi.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_doi.setObjectName("lb_doi")
        self.verticalLayout_6.addWidget(self.lb_doi)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_6.addItem(spacerItem4)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.textedit_doi = LPlainTextEdit(self.widget_5) # ludwig modified
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_doi.sizePolicy().hasHeightForWidth())
        self.textedit_doi.setSizePolicy(sizePolicy)
        self.textedit_doi.setMinimumSize(QtCore.QSize(0, 30))
        self.textedit_doi.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textedit_doi.setFont(font)
        self.textedit_doi.setStyleSheet("QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_doi.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_doi.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textedit_doi.setPlainText("")
        self.textedit_doi.setObjectName("textedit_doi")
        self.horizontalLayout_6.addWidget(self.textedit_doi)
        self.verticalLayout_8.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_7.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lb_file = QtWidgets.QLabel(self.widget_6)
        self.lb_file.setMinimumSize(QtCore.QSize(60, 16))
        self.lb_file.setMaximumSize(QtCore.QSize(60, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lb_file.setFont(font)
        self.lb_file.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_file.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lb_file.setObjectName("lb_file")
        self.verticalLayout_7.addWidget(self.lb_file)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_7.addItem(spacerItem5)
        self.horizontalLayout_7.addLayout(self.verticalLayout_7)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lb_filepath = QtWidgets.QLabel(self.widget_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lb_filepath.setFont(font)
        self.lb_filepath.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lb_filepath.setStyleSheet("QLabel {\n"
"    color: blue;\n"
"}")
        self.lb_filepath.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lb_filepath.setObjectName("lb_filepath")
        self.verticalLayout.addWidget(self.lb_filepath)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(8)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.btn_add = QtWidgets.QPushButton(self.widget_6)
        self.btn_add.setMinimumSize(QtCore.QSize(70, 25))
        self.btn_add.setMaximumSize(QtCore.QSize(70, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.btn_add.setFont(font)
        self.btn_add.setStyleSheet("QPushButton {\n"
"    background-color: #FF6347;\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #FF4500;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #CD5C5C;\n"
"}")
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_8.addWidget(self.btn_add)
        self.btn_clear = QtWidgets.QPushButton(self.widget_6)
        self.btn_clear.setMinimumSize(QtCore.QSize(70, 25))
        self.btn_clear.setMaximumSize(QtCore.QSize(70, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.btn_clear.setFont(font)
        self.btn_clear.setStyleSheet("QPushButton {\n"
"    background-color: #FF6347;\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #FF4500;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #CD5C5C;\n"
"}")
        self.btn_clear.setObjectName("btn_clear")
        self.horizontalLayout_8.addWidget(self.btn_clear)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.verticalLayout_8.addWidget(self.widget_6)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem7)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Default widget"))
        self.lb_title.setText(_translate("Dialog", "Title"))
        self.lb_author.setText(_translate("Dialog", "Author"))
        self.lb_journal.setText(_translate("Dialog", "Journal"))
        self.lb_year.setText(_translate("Dialog", "Year"))
        self.lb_doi.setText(_translate("Dialog", "DOI"))
        self.lb_file.setText(_translate("Dialog", "File"))
        self.lb_filepath.setText(_translate("Dialog", "None"))
        self.btn_add.setText(_translate("Dialog", "Add Path"))
        self.btn_clear.setText(_translate("Dialog", "Clear"))