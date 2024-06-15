import os
import sys
import shutil
from typing import List, Tuple

import markdown2
import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QListWidgetItem, \
    QMessageBox, QDialog, QInputDialog
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import Qt
from ui import Ui_ArticleDialog, Ui_KeywordDialog, Ui_NoteDialog, Ui_GroupDialog

import utils.opn
import utils.format
from func import global_session
from widget.action import setTextEditFit

from database import Article, Keyword, Note
import database
from archi import ArticleData, NoteData, AnnotationData

class LArticleDialog(QDialog, Ui_ArticleDialog):
    def __init__(self, parent=None, widget_title=None):
        super().__init__(parent)
        self.setupUi(self)
        if widget_title:
            self.setWindowTitle(widget_title)
        self.local_path = ""

        self.btn_add.clicked.connect(self.AddLocalPath)
        self.btn_clear.clicked.connect(self.RmLocalPath)
        self.textedit_title.setHook(keyPress_hook=setTextEditFit, keyPress_state=False)
        self.textedit_author.setHook(keyPress_hook=setTextEditFit, keyPress_state=False)
        self.textedit_journal.setHook(keyPress_hook=setTextEditFit, keyPress_state=False)
        self.textedit_year.setHook(keyPress_hook=setTextEditFit, keyPress_state=False)
        self.textedit_doi.setHook(keyPress_hook=setTextEditFit, keyPress_state=False)

    def get_data(self):
        data = {
            'title': self.textedit_title.toPlainText(),
            'author': self.textedit_author.toPlainText(),
            'journal': self.textedit_journal.toPlainText(),
            'year': self.textedit_year.toPlainText(),
            'doi': self.textedit_doi.toPlainText(),
            'local_path': self.local_path,
            'add_time': datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip() if v.strip() else None
        return ArticleData(**data)
    
    def set_data(self, article: Article):
        self.textedit_title.setPlainText(article.title)
        self.textedit_author.setPlainText(article.author)
        self.textedit_journal.setPlainText(article.journal)
        self.textedit_year.setPlainText(article.year)
        self.textedit_doi.setPlainText(article.doi)
        self.local_path = article.local_path
        if os.path.exists(str(utils.format.absolute_path(article.local_path))):
            self.lb_filepath.setText(str(article.local_path))
        else:
            self.lb_filepath.setText("The File May Not Exist!")

    def AddLocalPath(self):
        if file_path := QFileDialog.getOpenFileName(self, 'Open file', '', utils.format.PDF_FILTER)[0]:
            self.local_path = utils.format.related_path(file_path)
            self.lb_filepath.setText(self.local_path)
            shutil.copyfile(file_path, utils.format.absolute_path(self.local_path))

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
        self.textedit_note.setHook(keyPress_hook=setTextEditFit, keyPress_state=False)
        self.textedit_quote.setHook(keyPress_hook=setTextEditFit, keyPress_state=False)
        self.related_content = []

    def get_data(self): # TODO
        data = {
            'note': self.textedit_note.toPlainText(),
            'date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'related_content': self.textedit_quote.toPlainText(),
        }
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip() if v.strip() else None
        data['related_content'] = []
        return NoteData(**data)
    
    def set_data(self, note: Note):
        self.textedit_note.setPlainText(note.note)
        self.textedit_quote.setPlainText(str(note.related_content))
    
    def AddCite(self):
        if doi := QInputDialog.getText(self, 'Add related cite', 'doi')[0]:
            info = {"doi": doi, "local_path": None, "article_id": None}
            if article := utils.opn.search_doi_article(doi):
                info['article_id'] = article.id
                info['local_path'] = article.local_path
            self.related_content.append(info)
            self.list_cite.addItem(doi)
        
    def RemoveCite(self):
        if item := self.list_cite.currentItem():
            self.related_content.pop(self.list_cite.row(item))
            self.list_cite.takeItem(self.list_cite.row(item))

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
from PyQt5.QtWidgets import QVBoxLayout, QDialogButtonBox
from utils.opn import to_data, to_profile
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
            row = self.module.package_item(article.id, data = to_profile(to_data(article)))
            row[0].setCheckable(True)
            self.module.model.appendRow(row)

    def get_data(self):
        id_list = []
        for row in range(self.module.model.rowCount()):
            
            item: BinestedItem = self.module.model.item(row)
            if item.checkState() == Qt.Checked:
                id_list.append(item.article_id)

        return id_list

