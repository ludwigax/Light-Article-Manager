# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'note_diag.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLayout, QListWidget,
    QListWidgetItem, QPlainTextEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import ui.res_rc

from ui.modified import LPlainTextEdit

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(525, 262)
        self.verticalLayout_7 = QVBoxLayout(Dialog)
        self.verticalLayout_7.setSpacing(10)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(15, 15, 15, 15)
        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea {\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 495, 199))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, 5, -1, -1)
        self.lb_title = QLabel(self.scrollAreaWidgetContents)
        self.lb_title.setObjectName(u"lb_title")
        self.lb_title.setMinimumSize(QSize(60, 16))
        self.lb_title.setMaximumSize(QSize(60, 16))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_title.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.lb_title)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.textedit_title = LPlainTextEdit(self.scrollAreaWidgetContents)
        self.textedit_title.setObjectName(u"textedit_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_title.sizePolicy().hasHeightForWidth())
        self.textedit_title.setSizePolicy(sizePolicy)
        self.textedit_title.setMinimumSize(QSize(0, 30))
        self.textedit_title.setMaximumSize(QSize(16777215, 30))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(10)
        self.textedit_title.setFont(font1)
        self.textedit_title.setStyleSheet(u"QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_title.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textedit_title.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.horizontalLayout.addWidget(self.textedit_title)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.lb_note = QLabel(self.scrollAreaWidgetContents)
        self.lb_note.setObjectName(u"lb_note")
        self.lb_note.setMinimumSize(QSize(60, 16))
        self.lb_note.setMaximumSize(QSize(60, 16))
        self.lb_note.setFont(font)
        self.lb_note.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_note.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_2.addWidget(self.lb_note)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.textedit_note = LPlainTextEdit(self.scrollAreaWidgetContents)
        self.textedit_note.setObjectName(u"textedit_note")
        sizePolicy.setHeightForWidth(self.textedit_note.sizePolicy().hasHeightForWidth())
        self.textedit_note.setSizePolicy(sizePolicy)
        self.textedit_note.setMinimumSize(QSize(0, 30))
        self.textedit_note.setMaximumSize(QSize(16777215, 30))
        self.textedit_note.setFont(font1)
        self.textedit_note.setStyleSheet(u"QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_note.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textedit_note.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.horizontalLayout_2.addWidget(self.textedit_note)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.lb_content = QLabel(self.scrollAreaWidgetContents)
        self.lb_content.setObjectName(u"lb_content")
        self.lb_content.setMinimumSize(QSize(60, 16))
        self.lb_content.setMaximumSize(QSize(60, 16))
        self.lb_content.setFont(font)
        self.lb_content.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_content.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_4.addWidget(self.lb_content)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.btn_add = QPushButton(self.scrollAreaWidgetContents)
        self.btn_add.setObjectName(u"btn_add")
        self.btn_add.setMinimumSize(QSize(24, 24))
        self.btn_add.setMaximumSize(QSize(24, 24))
        icon = QIcon()
        icon.addFile(u":/icons/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_add.setIcon(icon)

        self.verticalLayout_6.addWidget(self.btn_add)

        self.btn_rm = QPushButton(self.scrollAreaWidgetContents)
        self.btn_rm.setObjectName(u"btn_rm")
        self.btn_rm.setMinimumSize(QSize(24, 24))
        self.btn_rm.setMaximumSize(QSize(24, 24))
        icon1 = QIcon()
        icon1.addFile(u":/icons/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_rm.setIcon(icon1)

        self.verticalLayout_6.addWidget(self.btn_rm)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)


        self.horizontalLayout_4.addLayout(self.verticalLayout_6)

        self.list_content = QListWidget(self.scrollAreaWidgetContents)
        self.list_content.setObjectName(u"list_content")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.list_content.sizePolicy().hasHeightForWidth())
        self.list_content.setSizePolicy(sizePolicy1)
        self.list_content.setMinimumSize(QSize(0, 80))
        self.list_content.setStyleSheet(u"QListWidget {\n"
"	background: transparent;\n"
"	border: none;\n"
"}")

        self.horizontalLayout_4.addWidget(self.list_content)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_7.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_7.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lb_title.setText(QCoreApplication.translate("Dialog", u"Title", None))
        self.textedit_title.setPlainText("")
        self.lb_note.setText(QCoreApplication.translate("Dialog", u"Note", None))
        self.textedit_note.setPlainText("")
        self.lb_content.setText(QCoreApplication.translate("Dialog", u"Content", None))
        self.btn_add.setText("")
        self.btn_rm.setText("")
    # retranslateUi

