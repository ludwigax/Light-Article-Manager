# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'atl_diag.ui'
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
    QHBoxLayout, QLabel, QLayout, QPlainTextEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from ui.modified import LPlainTextEdit

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(523, 359)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout_9 = QVBoxLayout(Dialog)
        self.verticalLayout_9.setSpacing(10)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(15, 15, 15, 15)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 493, 296))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.lb_title = QLabel(self.widget)
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

        self.verticalLayout_2.addWidget(self.lb_title)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.textedit_title = LPlainTextEdit(self.widget)
        self.textedit_title.setObjectName(u"textedit_title")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.textedit_title.sizePolicy().hasHeightForWidth())
        self.textedit_title.setSizePolicy(sizePolicy2)
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


        self.verticalLayout_8.addWidget(self.widget)

        self.widget_2 = QWidget(self.scrollAreaWidgetContents)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.lb_author = QLabel(self.widget_2)
        self.lb_author.setObjectName(u"lb_author")
        self.lb_author.setMinimumSize(QSize(60, 16))
        self.lb_author.setMaximumSize(QSize(60, 16))
        self.lb_author.setFont(font)
        self.lb_author.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_author.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.lb_author)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.textedit_author = LPlainTextEdit(self.widget_2)
        self.textedit_author.setObjectName(u"textedit_author")
        sizePolicy2.setHeightForWidth(self.textedit_author.sizePolicy().hasHeightForWidth())
        self.textedit_author.setSizePolicy(sizePolicy2)
        self.textedit_author.setMinimumSize(QSize(0, 30))
        self.textedit_author.setMaximumSize(QSize(16777215, 30))
        self.textedit_author.setFont(font1)
        self.textedit_author.setStyleSheet(u"QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_author.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textedit_author.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.horizontalLayout_3.addWidget(self.textedit_author)


        self.verticalLayout_8.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.scrollAreaWidgetContents)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy1.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy1)
        self.horizontalLayout_4 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.lb_journal = QLabel(self.widget_3)
        self.lb_journal.setObjectName(u"lb_journal")
        self.lb_journal.setMinimumSize(QSize(60, 16))
        self.lb_journal.setMaximumSize(QSize(60, 16))
        self.lb_journal.setFont(font)
        self.lb_journal.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_journal.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_4.addWidget(self.lb_journal)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.textedit_journal = LPlainTextEdit(self.widget_3)
        self.textedit_journal.setObjectName(u"textedit_journal")
        sizePolicy2.setHeightForWidth(self.textedit_journal.sizePolicy().hasHeightForWidth())
        self.textedit_journal.setSizePolicy(sizePolicy2)
        self.textedit_journal.setMinimumSize(QSize(0, 30))
        self.textedit_journal.setMaximumSize(QSize(16777215, 30))
        self.textedit_journal.setFont(font1)
        self.textedit_journal.setStyleSheet(u"QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_journal.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textedit_journal.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.horizontalLayout_4.addWidget(self.textedit_journal)


        self.verticalLayout_8.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.scrollAreaWidgetContents)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy1.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy1)
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 5, -1, -1)
        self.lb_year = QLabel(self.widget_4)
        self.lb_year.setObjectName(u"lb_year")
        self.lb_year.setMinimumSize(QSize(60, 16))
        self.lb_year.setMaximumSize(QSize(60, 16))
        self.lb_year.setFont(font)
        self.lb_year.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_year.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_5.addWidget(self.lb_year)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)

        self.textedit_year = LPlainTextEdit(self.widget_4)
        self.textedit_year.setObjectName(u"textedit_year")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.textedit_year.sizePolicy().hasHeightForWidth())
        self.textedit_year.setSizePolicy(sizePolicy3)
        self.textedit_year.setMinimumSize(QSize(0, 30))
        self.textedit_year.setMaximumSize(QSize(16777215, 30))
        self.textedit_year.setFont(font1)
        self.textedit_year.setStyleSheet(u"QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_year.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textedit_year.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.horizontalLayout_5.addWidget(self.textedit_year)


        self.verticalLayout_8.addWidget(self.widget_4)

        self.widget_5 = QWidget(self.scrollAreaWidgetContents)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy1.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy1)
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, 5, -1, -1)
        self.lb_doi = QLabel(self.widget_5)
        self.lb_doi.setObjectName(u"lb_doi")
        self.lb_doi.setMinimumSize(QSize(60, 16))
        self.lb_doi.setMaximumSize(QSize(60, 16))
        self.lb_doi.setFont(font)
        self.lb_doi.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_doi.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_6.addWidget(self.lb_doi)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)


        self.horizontalLayout_6.addLayout(self.verticalLayout_6)

        self.textedit_doi = LPlainTextEdit(self.widget_5)
        self.textedit_doi.setObjectName(u"textedit_doi")
        sizePolicy2.setHeightForWidth(self.textedit_doi.sizePolicy().hasHeightForWidth())
        self.textedit_doi.setSizePolicy(sizePolicy2)
        self.textedit_doi.setMinimumSize(QSize(0, 30))
        self.textedit_doi.setMaximumSize(QSize(16777215, 30))
        self.textedit_doi.setFont(font1)
        self.textedit_doi.setStyleSheet(u"QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")
        self.textedit_doi.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textedit_doi.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.horizontalLayout_6.addWidget(self.textedit_doi)


        self.verticalLayout_8.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.scrollAreaWidgetContents)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy1.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy1)
        self.horizontalLayout_7 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 5, -1, -1)
        self.lb_file = QLabel(self.widget_6)
        self.lb_file.setObjectName(u"lb_file")
        self.lb_file.setMinimumSize(QSize(60, 16))
        self.lb_file.setMaximumSize(QSize(60, 16))
        self.lb_file.setFont(font)
        self.lb_file.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_file.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_7.addWidget(self.lb_file)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_7.addItem(self.verticalSpacer_6)


        self.horizontalLayout_7.addLayout(self.verticalLayout_7)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 5, -1, -1)
        self.lb_filepath = QLabel(self.widget_6)
        self.lb_filepath.setObjectName(u"lb_filepath")
        self.lb_filepath.setFont(font1)
        self.lb_filepath.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lb_filepath.setStyleSheet(u"QLabel {\n"
"	color: blue;\n"
"}")
        self.lb_filepath.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.lb_filepath)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(8)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btn_add = QPushButton(self.widget_6)
        self.btn_add.setObjectName(u"btn_add")
        self.btn_add.setMinimumSize(QSize(70, 25))
        self.btn_add.setMaximumSize(QSize(70, 25))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(9)
        font2.setBold(False)
        self.btn_add.setFont(font2)
        self.btn_add.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_8.addWidget(self.btn_add)

        self.btn_clear = QPushButton(self.widget_6)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setMinimumSize(QSize(70, 25))
        self.btn_clear.setMaximumSize(QSize(70, 25))
        self.btn_clear.setFont(font2)
        self.btn_clear.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_8.addWidget(self.btn_clear)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_7.addLayout(self.verticalLayout)


        self.verticalLayout_8.addWidget(self.widget_6)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_7)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_9.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_9.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Default widget", None))
        self.lb_title.setText(QCoreApplication.translate("Dialog", u"Title", None))
        self.textedit_title.setPlainText("")
        self.lb_author.setText(QCoreApplication.translate("Dialog", u"Author", None))
        self.textedit_author.setPlainText("")
        self.lb_journal.setText(QCoreApplication.translate("Dialog", u"Journal", None))
        self.textedit_journal.setPlainText("")
        self.lb_year.setText(QCoreApplication.translate("Dialog", u"Year", None))
        self.textedit_year.setPlainText("")
        self.lb_doi.setText(QCoreApplication.translate("Dialog", u"DOI", None))
        self.textedit_doi.setPlainText("")
        self.lb_file.setText(QCoreApplication.translate("Dialog", u"File", None))
        self.lb_filepath.setText(QCoreApplication.translate("Dialog", u"None", None))
        self.btn_add.setText(QCoreApplication.translate("Dialog", u"Add Path", None))
        self.btn_clear.setText(QCoreApplication.translate("Dialog", u"Clear", None))
    # retranslateUi

