import os
import sys
from typing import List, Tuple

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog,\
    QMessageBox, QDialog, QTextBrowser, QListWidget, QTextEdit, QTreeWidgetItem, QInputDialog,\
    QToolBar, QDockWidget, QSizePolicy
from PySide6.QtCore import Qt, Signal, QByteArray, QSignalBlocker
from PySide6.QtGui import QAction

import PySide6QtAds as QtAds

from PySide6.QtWidgets import QTabWidget, QVBoxLayout

from ui import Ui_MainWindow2
from widget.dialog import LArticleDialog, LKeywordDialog, LNoteDialog, LGroupDialog
from widget.widget import LSearchItem, LNoteItem, LAddItem, LArticleItem, LFolderItem, LCheckItem, \
    LFolderAddItem
import widget.action as act
from widget.search import DelayedSearchWidget
from widget.text import EditableTextEdit
from widget.zone import ModuleViewZone, MainBrowserZone, NoteViewZone, NoteEditZone, PDFViewerZone, \
    OnlineSearchZone

from crawler import DownloadWorker

from database import Article, Keyword, Note
import database

from sylva import ArticleData, NoteData, AnnotationData, FolderData
from sylva import Sylva, UserDict

import utils
import utils.format as fmt
import utils.opn as opn
from utils.opn import to_data

from mvc.module import NestedModule, NonNestedModule
from mvc.notem import NoteModule

from tools.pdf import extract_annotations
import tools.ref as ref

import markdown2
import datetime

from func import global_session

import pickle as pkl

class LMainWindow(QMainWindow, Ui_MainWindow2):
    render_signal = Signal(int)
    render_note_signal = Signal(int)
    delete_note_signal = Signal(int)
    open_pdf_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ludwig Article Manager")
        self.focus_id = None
        self.download_id = None
        # self.log = [] # TODO

        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.OpaqueSplitterResize, True)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.XmlCompressionEnabled, False)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.FocusHighlighting, True)
        QtAds.CDockManager.setAutoHideConfigFlags(QtAds.CDockManager.DefaultAutoHideConfig)
        self.dock_manager = QtAds.CDockManager(self)

        self.mvm = NonNestedModule(self, columns=None)
        self.nvm = NestedModule(self, columns=None)
        self.notem = NoteModule(self)
        self.browser_m = QTextBrowser(self)
        self.textedit_nt_tl = EditableTextEdit(self)
        self.textedit_nt_cn = EditableTextEdit(self)

        self.is_notelock = [1, 1]
        self.pdf_area = None
        self.pdf_set = set()

        # define the dock view
        self.zone_moduleview = ModuleViewZone(self, self)
        self.zone_mainbrowser = MainBrowserZone(self, self)
        self.zone_noteview = NoteViewZone(self, self)
        self.zone_noteedit = NoteEditZone(self, self)
        self.zone_onlinesearch = OnlineSearchZone(self, self)

        # init the necessary data
        self.zone_moduleview.init_data()
        self.zone_noteedit.init_data(None)

        dock1 = QtAds.CDockWidget("Main View", self)
        dock1.setWidget(self.zone_moduleview)
        area1 = self.dock_manager.setCentralWidget(dock1)
        area1.setAllowedAreas(QtAds.DockWidgetArea.OuterDockAreas)

        dock3 = QtAds.CDockWidget("Note View", self)
        dock3.setWidget(self.zone_noteview)
        area3 = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.BottomDockWidgetArea, dock3, area1)

        dock2 = QtAds.CDockWidget("Main Browser", self)
        dock2.setWidget(self.zone_mainbrowser)
        area2 = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.RightDockWidgetArea, dock2, area1)

        dock4 = QtAds.CDockWidget("Note Browser", self)
        dock4.setWidget(self.zone_noteedit)
        area4 = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.RightDockWidgetArea, dock4, area3)

        dock5 = QtAds.CDockWidget("Online Search", self)
        dock5.setWidget(self.zone_onlinesearch)
        area5 = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.LeftDockWidgetArea, dock5)

        self.dock_widgets = {
            "module": dock1,
            "main": dock2,
            "note": dock3,
            "note_edit": dock4,
            "online_search": dock5,
        }

        self._setupMenuAction()
        self._setupSlots()
        self._setupBrowserAnchor()

        self.loadPerspective()

    def _setupMenuAction(self):
        self.actionImport_article.triggered.connect(self.onImportClicked)
        self.actionImport_batch.triggered.connect(self.onImportBatchClicked)
        self.actionImport_manually.triggered.connect(self.onManualClicked)
        self.actionSave_layout.triggered.connect(self.onSaveLayoutClicked)
        # self.actionSave_layout.triggered.connect(self.onOnlineSearch) # just for test
        # Another action TODO
        # self.actionLoad_Library
        # self.actionDump_Library
        # self.actionMicrosoft_Modern

    def _setupSlots(self):
        self.render_signal.connect(self.showArticleMain)
        # temp
        self.render_note_signal.connect(self.showNote_temp)
        self.delete_note_signal.connect(self.clearNoteOnDelete)
        self.open_pdf_signal.connect(self.onOpenArticlePDF)

        # widget slot
        self.textedit_nt_tl.editingChanged.connect(lambda x: self.onEditSwitching(x, 0))
        self.textedit_nt_cn.editingChanged.connect(lambda x: self.onEditSwitching(x, 1))
        self.zone_onlinesearch.import_signal.connect(self.onOnlineSearchImport)

    def _setupBrowserAnchor(self):
        def anchor_fcn(path):
            if act.openAritcleFile(path):
                self.showArticleMain(self.focus_id)
        self.browser_m.anchorClicked.connect(anchor_fcn)   

    # --------------------------------------------------------------------------------
    # mainwindow GUI functions
    # browser
    def setFocusArticle(self, article_id: int = None):
        self.focus_id = article_id

    def renderBrowser(self, content: str): # DELETE this FUNCTION
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

    def onSaveLayoutClicked(self):
        self.savePerspective()

    def onOpenArticlePDF(self, article_id):
        import os.path as osp
        # test utils
        article = opn.get_article(article_id)
        if not article:
            return
        
        pdf_path = article.local_path
        if not pdf_path:
            return
        if article_id in self.pdf_set:
            return
        
        self.pdf_viewer = PDFViewerZone(self, self)
        self.pdf_viewer.init_data(osp.join("papers", pdf_path))

        dock5 = QtAds.CDockWidget("PDF Viewer", self)
        dock5.setWidget(self.pdf_viewer)
        dock5.setFeature(QtAds.CDockWidget.DockWidgetDeleteOnClose, True)
        dock5.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
        dock5.setMinimumWidth(850)
        
        dock5.closed.connect(lambda: self.onCloseArticlePDF(article_id))
        if self.pdf_area:
            self.pdf_area = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.CenterDockWidgetArea, dock5, self.pdf_area)
        else:
            self.pdf_area = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.RightDockWidgetArea, dock5)

        self.pdf_set.add(article_id)

    def onCloseArticlePDF(self, article_id):
        self.pdf_set.remove(article_id)
        if not self.pdf_set:
            self.pdf_area = None

    def onOnlineSearchImport(self, result: dict):
        data = {
            "title": result['title'],
            "author": " and ".join(result['authors']),
            "journal": result['journal'],
            "year": result['published_year'],
            "doi": result['doi'],
            "add_time": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        data = ArticleData(**data)
        self.importArticle(data)

    def onEditSwitching(self, flag, order):
        self.is_notelock[order] = flag
        if self.zone_noteedit.note_id is None:
            return
        
        if self.is_notelock[0] and self.is_notelock[1]:
            self.dock_widgets["note_edit"].setWindowTitle("Note Browser")
        else:
            self.dock_widgets["note_edit"].setWindowTitle("Note Browser *")

        if not flag:
            return
        title = self.textedit_nt_tl.toPlainText()
        content = self.textedit_nt_cn.toHtml()
        note = opn.get_note(self.zone_noteedit.note_id)
        data = to_data(note)
        data.title = title
        data.note = content
        data.changed_time = opn.get_time()
        opn.reset_note(data, note)
        if self.zone_noteview.article_id == note.article_id:
            self.zone_noteview.clear_data()
            self.zone_noteview.init_data(note.article_id)

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
            self.mvm.append_item(article.id, data)
        return True

    def showArticleMain(self, article: Article | int):
        print(f"clicked {article}")
        if isinstance(article, int):
            article = opn.get_article(article)
        self.zone_mainbrowser.init_data(article.id)
        self.zone_noteview.clear_data()
        self.zone_noteview.init_data(article.id)
        self.setFocusArticle(article.id)

    def showNote_temp(self, note_id):
        print(f"clicked {note_id}")
        self.zone_noteedit.init_data(note_id)

    def clearNoteOnDelete(self, note_id):
        if self.zone_noteedit.note_id == note_id:
            self.zone_noteedit.init_data(None)

    def savePerspective(self):
        with open("layout.xml", "wb") as f:
            f.write(self.dock_manager.saveState())

    def loadPerspective(self):
        with open("layout.xml", "rb") as f:
            self.dock_manager.restoreState(f.read())

    def closeEvent(self, event):
        self.dock_manager.deleteLater()
        super().closeEvent(event)
