import sys
from typing import List, Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QListWidgetItem, \
    QMessageBox, QDialog, QInputDialog

from ui import Ui_AddItem, Ui_InfoItem, Ui_KeywordItem, Ui_ArticleItem, Ui_FolderItem, Ui_CheckItem, Ui_FolderAddItem

from database import Article
import database
import utils
import widget.action as act
from widget.menu import folder_right_click_menu

import markdown2
import datetime

from func import global_session
import utils.opn

class LSearchItem(QWidget, Ui_InfoItem):
    def __init__(self, id: int, text: str=None):
        super().__init__()
        self.setupUi(self)
        self.article_id = id
        if text:
            self.browser.setMarkdown(text)

        self.btn_del.clicked.connect(self.DeleteItem)
        self.browser.setHook(mousePress_hook=self.GetItemDetail, mousePress_state=False)

    def SetItemText(self, text: str):
        text = markdown2.markdown(text)
        self.browser.setHtml(text)

    def GetItemDetail(self, handle, params):
        self.window().showArticleMain(self.article_id)

    def DeleteItem(self):
        if QMessageBox.question(self, 'Delete', 'Are you sure to delete this item?', QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            act.deleteArticle(self.article_id) # TODO function have problem
            self.window().removeListItem(self, "searchs")
            self.window().showArticleMain(self.article_id)

class LArticleItem(QWidget, Ui_ArticleItem):
    def __init__(self, id: int, text: str=None, node_id=None):
        super().__init__()
        self.setupUi(self)
        self.article_id = id
        
        if text:
            self.SetItemText(text)

        if not node_id is None:
            self.node_id = node_id
            self.btn_del.clicked.connect(self.RemoveNode)
        else:
            self.btn_del.clicked.connect(self.DeleteItem)
        self.lb_title.setHook(mousePress_hook=self.GetItemDetail, mousePress_state=False)

    def SetItemText(self, text: str):
        self.lb_title.setFullText(text)
        self.lb_title.updateElidedText()

    def GetItemDetail(self, handle, params):
        self.lb_title.updateElidedText()
        self.window().showArticleMain(self.article_id)

    def RemoveNode(self):
        act.deleteArticleNode(self.node_id)
        act.removeTreeWidgetItem(self, self.window().tree_root)

    def DeleteItem(self):
        if QMessageBox.question(self, 'Delete', 'Are you sure to delete this item?', QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.article_id == self.window().focus_id:
                self.window().focus_id = None
                self.window().clearArticleMain()
            self.window().removeListItem(self, "articles")
            act.deleteArticleCascade(self.article_id)
            self.window().showViewList()

class LCheckItem(QWidget, Ui_CheckItem):
    def __init__(self, id: int, text: str=None):
        super().__init__()
        self.setupUi(self)
        self.article_id = id
        if text:
            self.SetItemText(text)

    def SetItemText(self, text: str):
        self.lb_title.setFullText(text)
        self.lb_title.updateElidedText()

    def GetCheckState(self):
        return self.btn_check.isChecked()
    
class LFolderAddItem(QWidget, Ui_FolderAddItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_add.clicked.connect(self.AddFolder)

    def AddFolder(self):
        self.window().onFolderAddClicked()

class LFolderItem(QWidget, Ui_FolderItem):
    def __init__(self, id: int, text: str=None):
        super().__init__()
        self.setupUi(self)
        self.node_id = id
        self.lb_folder.setHook(mouseDoubleClick_hook=self.SetEditMode, mouseDoubleClick_state=None)
        self.edit_folder.setHook(focusOut_hook=self.FinishEditMode, focusOut_state=False)
        self.edit_folder.editingFinished.connect(self.FinishEditMode)
        self.lb_icon.setHook(mousePress_hook=self.SetExpand, mousePress_state=None)
        self.btn_add.clicked.connect(self.AddFolderArticle)
        
        if text:
            self.SetItemText(text)

    def mousePressEvent(self, a0: QMouseEvent) -> None: # this function do not use hook, maybe change in future
        if a0.button() == Qt.RightButton:
            return self.callFolderMenu(self, (a0,))
        return super().mousePressEvent(a0)

    def callFolderMenu(self, handle, params):
        folder_right_click_menu(self, params[0].pos())

    def SetItemText(self, text: str):
        self.lb_folder.setText(text)
        self.edit_folder.setText(text)

    def SetExpand(self, handle, params):
        if params[0].button() == Qt.LeftButton:
            tree_widget = self.window().tree_root
            # item = tree_widget.itemAt(params[0].pos()) # this could cause error as the pos is strange
            item = tree_widget.itemAt(self.pos())
            if not item:
                return 0
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
            return 1
        return 0

    def SetEditMode(self, handle, params):
        if params[0].button() == Qt.LeftButton:
            self.stackedWidget.setCurrentIndex(1)
            self.edit_folder.setFocus()
            return 1
        return 0 # not override the right click event

    def FinishEditMode(self, handle=None, params=()):
        self.stackedWidget.setCurrentIndex(0)
        new_text = self.edit_folder.text()
        if new_text != self.lb_folder.text():
            act.resetNode(new_text, self.node_id)
            self.SetItemText(new_text)

    def AddFolderArticle(self, handle=None, params=()):
        self.window().onFolderArticleAddClicked(self, self.node_id)

    def RemoveNode(self):
        self.window().onFolderDeleteClicked(self)

class LNoteItem(QWidget, Ui_InfoItem):
    def __init__(self, note_id: int, text: str=None):
        super().__init__()
        self.setupUi(self)
        self.note_id = note_id

        self.btn_del.clicked.connect(self.DeleteItem)
        self.browser.setHook(mouseDoubleClick_hook=self.SetItemNote, mouseDoubleClick_state=True)

    def SetItemText(self, text: str):
        text = markdown2.markdown(text)
        self.browser.setHtml(text)

    def SetItemNote(self, handle, params):
        self.window().onNoteModifierItemClicked(self.note_id)

    def DeleteItem(self):
        if QMessageBox.question(self, 'Delete', 'Are you sure to delete this item?', QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            utils.opn.delete_note(global_session(), self.note_id)
            self.window().removeListItem(self, "notes")

class LAddItem(QWidget, Ui_AddItem):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.browser.setHook(mousePress_hook=self.AddItemNote, mousePress_state=True)

    def AddItemNote(self, handle, params):
        self.window().onNoteModifierAddClicked()

class LKeywordItem(QWidget, Ui_KeywordItem):
    r"""
    This class is used in a LineEdit when users use tab 
     to transfer former text to a keyword item for searching
    """
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.label.setText(text)
        
        self.pushButton.clicked.connect(self.DeleteItem)

    def DeleteItem(self):
        # TODO
        self.deleteLater()
