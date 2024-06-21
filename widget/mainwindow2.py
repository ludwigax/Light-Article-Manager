import os
import sys
from typing import List, Tuple

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog,\
    QMessageBox, QDialog, QTextBrowser, QListWidget, QTextEdit, QTreeWidgetItem, QInputDialog,\
    QToolBar, QAction, QDockWidget
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QTabWidget, QVBoxLayout

from ui import Ui_MainWindow2
from widget.dialog import LArticleDialog, LKeywordDialog, LNoteDialog, LGroupDialog
from widget.widget import LSearchItem, LNoteItem, LAddItem, LArticleItem, LFolderItem, LCheckItem, \
    LFolderAddItem
import widget.action as act
from widget.search import SearchWidget
from widget.zone import ModuleViewZone, MainBrowserZone, NoteViewZone, NoteBrowserZone 

from crawler import DownloadWorker

from database import Article, Keyword, Note
import database

from archi import ArticleData, NoteData, AnnotationData
from archi import Archi, ProfileData

import utils
import utils.format as fmt
import utils.opn as opn
from utils.opn import to_data, to_profile

from mvc.module import NestedModule, NonNestedModule
from mvc.notem import NoteModule

from tools.pdf import extract_annotations
import tools.ref as ref

import markdown2
import datetime

from func import global_session

class LMainWindow(QMainWindow, Ui_MainWindow2):
    render_signal = pyqtSignal(int)
    render_note_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ludwig Article Manager")
        self.focus_id = None
        self.download_id = None
        # self.log = [] # TODO

        self.mvm = NonNestedModule(self, columns=None)
        self.nvm = NestedModule(self, columns=None)
        self.notem = NoteModule(self)
        self.browser_m = QTextBrowser(self)
        self.browser_nt_1 = QTextBrowser(self)
        self.browser_nt_2 = QTextBrowser(self)

        self._setupMenuAction()
        self._setupSlots()
        self._setupBrowserAnchor()

        # define the dock view
        self.widget_1 = ModuleViewZone(self, self)
        self.widget_2 = MainBrowserZone(self, self)
        self.widget_3 = NoteViewZone(self, self)
        self.widget_4 = NoteBrowserZone(self, self)

        # init the necessary data
        self.widget_1.init_data()

        dock1 = QDockWidget("Module View", self)
        dock1.setWidget(self.widget_1)
        self.addDockWidget(Qt.TopDockWidgetArea, dock1)

        dock2 = QDockWidget("Main Browser", self)
        dock2.setWidget(self.widget_2)
        self.addDockWidget(Qt.TopDockWidgetArea, dock2)

        dock3 = QDockWidget("Note View", self)
        dock3.setWidget(self.widget_3)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock3)

        dock4 = QDockWidget("Note Browser", self)
        dock4.setWidget(self.widget_4)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock4)

    def _setupMenuAction(self):
        self.actionImport_article.triggered.connect(self.onImportClicked)
        self.actionImport_batch.triggered.connect(self.onImportBatchClicked)
        self.actionImport_manually.triggered.connect(self.onManualClicked)
        # Another action TODO
        # self.actionLoad_Library
        # self.actionDump_Library
        # self.actionMicrosoft_Modern

    def _setupSlots(self):
        self.render_signal.connect(self.showArticleMain)
        # temp
        self.render_note_signal.connect(self.showNote_temp)

    def _setupBrowserAnchor(self):
        def anchor_fcn(path):
            if act.openAritcleFile(path):
                self.showArticleMain(self.focus_id)
        self.browser_m.anchorClicked.connect(anchor_fcn)   

    def showNote_temp(self, note_id):
        self.widget_4.init_data(note_id)

    # --------------------------------------------------------------------------------
    # mainwindow GUI functions
    # browser
    def setFocusArticle(self, article_id: int = None):
        self.focus_id = article_id

    def renderBrowser(self, content: str):
        self.browser.setHtml(content)

    def clearBrowser(self):
        self.browser.clear()

    # --------------------------------------------------------------------------------
    # slot functions
    def onImportClicked(self):
        if not (file_path := QFileDialog.getOpenFileName(self, 'Open file', '', fmt.BIB_FILTER)[0]):
            return
        data = ref.REF_PARSER.extract(file_path)
        if not data:
            return
        self.importArticle(data)

    def onImportBatchClicked(self):
        if not (file_paths := QFileDialog.getOpenFileNames(self, 'Open folder', '', fmt.BIB_FILTER)[0]):
            return
        for file_path in file_paths:
            data = ref.REF_PARSER.extract(file_path)
            if not data:
                continue
            self.importArticle(data)
    
    def onManualClicked(self):
        dialog = LArticleDialog(self, 'Add manually')
        if dialog.exec_() == QDialog.Rejected:
            return
        data = dialog.get_data()
        if not data.title:
            return
        self.importArticle(data)

    # --------------------------------------------------------------------------------
    # combo functions
    def importArticle(self, datas: ArticleData | List[ArticleData]):
        if isinstance(datas, ArticleData):
            datas = [datas]
        for data in datas:
            if data.local_path is not None and not act.checkPath(fmt.absolute_path(data.local_path)):
                data.local_path = None
            article = opn.create_article(data)
            opn.add_article(article)
            self.mvm.add_item(article.id, to_profile(data))
        return True

    def showArticleMain(self, article: Article | int):
        print(f"clicked {article}")
        if isinstance(article, int):
            article = opn.get_article(article)
        self.widget_2.init_data(article.id)
        self.widget_3.clear_data()
        self.widget_3.init_data(article.id)
        self.setFocusArticle(article.id)
