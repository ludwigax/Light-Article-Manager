import os
import sys
from typing import List, Tuple

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog,\
    QMessageBox, QDialog, QTextBrowser, QListWidget, QTextEdit, QTreeWidgetItem, QInputDialog,\
    QToolBar, QAction
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QTabWidget, QVBoxLayout

from ui import Ui_MainWindow2
from widget.dialog import LArticleDialog, LKeywordDialog, LNoteDialog, LGroupDialog
from widget.widget import LSearchItem, LNoteItem, LAddItem, LArticleItem, LFolderItem, LCheckItem, \
    LFolderAddItem
import widget.action as act
from widget.search import SearchWidget

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

        self._setupMenuAction()
        self._setupLeftWidget()
        self._setupRightWidget()
        self._setupSlots()
        self._setupBrowserAnchor()

        # temp functions
        self.win_1 = None
        self.win_2 = None
        self._setupDockNoteList_temp()
        self._setupDockNoteBrowser_temp()

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
        self.browser.anchorClicked.connect(anchor_fcn)

    def _setupLeftWidget(self):
        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        
        articles = opn.get_all_articles()

        self.mvm = NonNestedModule(self, columns=None)
        self.nvm = NestedModule(self, columns=None)

        search_widget = SearchWidget()
        search_widget.search_signal.connect(self.mvm._sort_by_search)
        search_widget.search_signal.connect(self.nvm._sort_by_search)

        for article in articles:
            self.mvm.add_item(article.id, to_profile(to_data(article)))
        
        archi = Archi()
        archi.load()
        for kv in archi.data:
            item = self.nvm.add_item(-1, True, ProfileData(kv['name'], '', '', '', '', ''))
            for idx in kv['data']:
                article = opn.get_article(idx)
                self.nvm.add_item(idx, False, to_profile(to_data(article)), item)

        tab1_layout = QVBoxLayout()
        tab1_layout.setContentsMargins(0, 0, 0, 0)
        tab1_layout.setSpacing(3)
        tab1_layout.addWidget(self.mvm.tree_view)

        tab1.setLayout(tab1_layout)
        
        tab2_layout = QVBoxLayout()
        tab2_layout.setContentsMargins(0, 0, 0, 0)
        tab2_layout.setSpacing(3)
        tab2_layout.addWidget(self.nvm.tree_view)
        tab2.setLayout(tab2_layout)
        
        tab_widget.addTab(tab1, "Flat View")
        tab_widget.addTab(tab2, "Folder View")
        
        layout = QVBoxLayout()
        layout.addWidget(search_widget)
        layout.addWidget(tab_widget)
        self.widgetL.setLayout(layout)
        return
    
    def _setupRightWidget(self):
        browse_widget = QWidget()

        toolbar = QToolBar("Toolbar", browse_widget)
        actionAddnote = QAction("Add note", browse_widget)
        actionAddnote.triggered.connect(self.temp_add_note)
        toolbar.addAction(actionAddnote)

        self.browser = QTextBrowser(self)
        
        browse_layout = QVBoxLayout()
        browse_layout.setContentsMargins(0, 0, 0, 0)
        browse_layout.setSpacing(3)
        browse_layout.addWidget(toolbar)
        browse_layout.addWidget(self.browser)
        browse_widget.setLayout(browse_layout)

        layout = QVBoxLayout()
        layout.addWidget(browse_widget)
        self.widgetR.setLayout(layout)
        return
    
    def _setupDockNoteList_temp(self):
        self.win_1 = QDialog(self)
        self.notem = NoteModule(self)
        layout = QVBoxLayout()

        layout.addWidget(self.notem.tree_view)

        self.win_1.setWindowTitle("Note List")
        self.win_1.setLayout(layout)
        self.win_1.setModal(False)
        self.win_1.show()

    def _setupDockNoteBrowser_temp(self):
        self.win_2 = QDialog(self)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        
        browser1 = QTextBrowser(self.win_2)
        browser2 = QTextBrowser(self.win_2)

        layout.addWidget(browser1, stretch=2)
        layout.addWidget(browser2, stretch=8)

        self.win_2.setWindowTitle("Note Browser")
        self.win_2.setLayout(layout)
        self.win_2.setModal(False)
        self.win_2.show()

        def on_win_2_close(event):
            self.win_2 = None
            event.accept()

        self.win_2.closeEvent = on_win_2_close
        
    
    def temp_add_note(self):
        if not self.focus_id:
            # self.print(fmt.RED_BOLD("No valid article selected"))
            return
        diag = LNoteDialog(self, 'Add New Note')
        if diag.exec_() == QDialog.Rejected:
            return
        data = diag.get_data()
        note = opn.create_note(data)
        opn.add_note(note, opn.get_article(self.focus_id))

        self.showArticleMain(self.focus_id)

    def showNote_temp(self, note_id):
        note = opn.get_note(note_id)
        content = fmt.get_notes_html([note])
        content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
        if self.win_2 is None:
            self._setupDockNoteBrowser_temp()
        self.win_2.findChildren(QTextBrowser)[1].setHtml(content)

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
        article = act.getArticle(article)
        content = fmt.get_article_html(article)
        content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
        self.setFocusArticle(article.id)
        self.renderBrowser(content)

        # temp functions
        self.notem.focus_id = article.id
        self.notem.model.removeRows(0, self.notem.model.rowCount())
        notes = opn.get_article_notes(article)
        for note in notes:
            self.notem.add_item(note.id, to_profile(to_data(note)))