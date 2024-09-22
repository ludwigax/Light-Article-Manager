import os
import sys
import shutil
from typing import List, Tuple

import markdown2
import datetime

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QListWidgetItem, \
    QMessageBox, QDialog, QInputDialog, QLineEdit
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt
from ui import Ui_ArticleDialog, Ui_KeywordDialog, Ui_NoteDialog, Ui_GroupDialog

import utils.opn
import utils.format as fmt
import utils.opn as opn
from func import global_session

from database import Article, Keyword, Note
import database
from sylva import ArticleData, NoteData, AnnotationData

class LArticleDialog(QDialog, Ui_ArticleDialog):
    def __init__(self, parent=None, widget_title=None):
        super().__init__(parent)
        self.setupUi(self)
        if widget_title:
            self.setWindowTitle(widget_title)
        self.local_path = ""

        self.btn_add.clicked.connect(self.AddLocalPath)
        self.btn_clear.clicked.connect(self.RmLocalPath)
        self.textedit_title.setTextChangedSlot()
        self.textedit_author.setTextChangedSlot()
        self.textedit_journal.setTextChangedSlot()
        self.textedit_year.setTextChangedSlot()
        self.textedit_doi.setTextChangedSlot()

    def get_data(self):
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        data = {
            'title': self.textedit_title.toPlainText(),
            'author': self.textedit_author.toPlainText(),
            'journal': self.textedit_journal.toPlainText(),
            'year': self.textedit_year.toPlainText(),
            'doi': self.textedit_doi.toPlainText(),
            'local_path': self.local_path,
            'add_time': time,
        }
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip() if v.strip() else None
        if data['title'] is None:
            return None
        return ArticleData(**data)
    
    def set_data(self, article: Article):
        self.textedit_title.setPlainText(article.title)
        self.textedit_author.setPlainText(article.author)
        self.textedit_journal.setPlainText(article.journal)
        self.textedit_year.setPlainText(article.year)
        self.textedit_doi.setPlainText(article.doi)
        self.local_path = article.local_path
        if os.path.exists(str(opn.get_absolute_path(article.local_path))):
            self.lb_filepath.setText(str(article.local_path))
        else:
            self.lb_filepath.setText("The File May Not Exist!")

    def AddLocalPath(self):
        if file_path := QFileDialog.getOpenFileName(self, 'Open file', '', fmt.PDF_FILTER)[0]:
            self.local_path = opn.get_related_path(file_path)
            self.lb_filepath.setText(self.local_path)
            shutil.copyfile(file_path, opn.get_absolute_path(self.local_path))

    def RmLocalPath(self):
        self.local_path = None
        self.lb_filepath.setText("None")

class LKeywordDialog(QDialog, Ui_KeywordDialog):
    def __init__(self, parent=None, widget_title=None):
        super().__init__(parent)
        self.setupUi(self)
        if widget_title:
            self.setWindowTitle(widget_title)

    def get_data(self) -> List[str]: # the strip operation is not implemented here 
        return self.textedit_kwd.toPlainText().strip().split('\n')
    
    def set_data(self, info: List[Keyword]):
        info = [keyword.word for keyword in info]
        self.textedit_kwd.setPlainText('\n'.join(info))

class LNoteDialog(QDialog, Ui_NoteDialog):
    def __init__(self, parent=None, widget_title=None):
        super().__init__(parent)
        self.setupUi(self)
        if widget_title:
            self.setWindowTitle(widget_title)

        self.btn_add.clicked.connect(self.AddCite)
        self.btn_rm.clicked.connect(self.RemoveCite)
        self.textedit_title.setTextChangedSlot()
        self.textedit_note.setTextChangedSlot()
        self.quote = []

    def get_data(self):
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        data = {
            'title': self.textedit_title.toPlainText(),
            'note': self.textedit_note.toPlainText(),
            'add_time': time,
            'quote': [],
        }
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip() if v.strip() else None
        data['quote'] = self.quote
        return NoteData(**data)
    
    def set_data(self, note: Note):
        self.textedit_title.setPlainText(note.title)
        self.textedit_note.setPlainText(note.note)
        for content in note.quote:
            self.quote.append(content)
            self.list_content.addItem(content)
    
    def AddCite(self):
        if content := QInputDialog.getText(self, 'Add related content', 'content')[0]:
            self.quote.append(content)
            self.list_content.addItem(content)
        
    def RemoveCite(self):
        if item := self.list_content.currentItem():
            self.quote.pop(self.list_content.row(item))
            self.list_content.takeItem(self.list_content.row(item))

class LGroupDialog(QDialog, Ui_GroupDialog):
    def __init__(self, parent=None, widget_title=None):
        super().__init__(parent)
        self.setupUi(self)
        if widget_title:
            self.setWindowTitle(widget_title)

    def add_item(self, widget: QWidget):
        item = QListWidgetItem(self.list_group)
        item.setSizeHint(widget.sizeHint())
        self.list_group.addItem(item)
        self.list_group.setItemWidget(item, widget)

    def get_data(self) -> List[int]:
        article_ids = []
        for idx in range(self.list_group.count()):
            item = self.list_group.item(idx)
            widget = self.list_group.itemWidget(item)
            if widget.GetCheckState():
                article_ids.append(widget.article_id)
        return article_ids
    
import mvc.base
from mvc.model import BinestedItem
from PySide6.QtWidgets import QVBoxLayout, QDialogButtonBox
from utils.opn import to_data
class CheckStateDialog(QDialog):
    def __init__(self, parent=None, title=None, columns=None):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.resize(500, 350)

        layout = QVBoxLayout(self)

        self.module = mvc.base.BaseModule(self, columns=['Title', 'Add Time', 'Rank'])
        layout.addWidget(self.module.tree_view)

        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.init_data()
        self.module.set_slots()

    def init_data(self):
        articles = utils.opn.get_all_articles()
        for article in articles:
            self.module.append_item(to_data(article))
        for row in range(self.module.model.rowCount()):
            item: BinestedItem = self.module.model.item(row)
            item.setCheckable(True)

    def get_data(self):
        id_list = []
        for row in range(self.module.model.rowCount()):
            item: BinestedItem = self.module.model.item(row)
            if item.checkState() == Qt.Checked:
                id_list.append(item.id)

        return id_list



# quickly dialog function -- for testing
def new_article_dialog(clf, data: Article = None):
    dialog = LArticleDialog(clf, 'Add New Article')
    if dialog.exec_() == QDialog.Rejected:
        return None
    return dialog.get_data()

def modify_article_dialog(clf, article: Article):
    dialog = LArticleDialog(clf, 'Modify Article')
    dialog.set_data(article)
    if dialog.exec_() == QDialog.Rejected:
        return None
    return dialog.get_data()

def delete_article_dialog(clf):
    if QMessageBox.question(clf, 'Delete', 'Ensure the deletion',
                            QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
        return True
    else:
        return False
    
def new_article_sylva_dialog(clf):
    diag = CheckStateDialog(clf.parent(), 'Add article to folder')
    if diag.exec_() == QDialog.Rejected:
        return None
    return diag.get_data()

def rename_folder_sylva_dialog(clf):
    new_title, ok_pressed = QInputDialog.getText(clf, "Input", "Changed Name:", QLineEdit.Normal, "")
    return new_title if ok_pressed else None

def delete_note_dialog(clf):
    if QMessageBox.question(clf, 'Delete', 'Ensure the deletion',
                            QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
        return True
    else:
        return False