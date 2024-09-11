# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'kwd_diag.ui'
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
    QLabel, QPlainTextEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 278)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.lb_key = QLabel(Dialog)
        self.lb_key.setObjectName(u"lb_key")

        self.verticalLayout.addWidget(self.lb_key)

        self.textedit_kwd = QPlainTextEdit(Dialog)
        self.textedit_kwd.setObjectName(u"textedit_kwd")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        self.textedit_kwd.setFont(font)
        self.textedit_kwd.setStyleSheet(u"QPlainTextEdit {\n"
"    border: 1px solid#e6e6e6;\n"
"    background-color: white;\n"
"}")

        self.verticalLayout.addWidget(self.textedit_kwd)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Keywords", None))
        self.lb_key.setText(QCoreApplication.translate("Dialog", u"Add Keywords Line by Line", None))
    # retranslateUi

