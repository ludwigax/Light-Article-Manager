import os
import sys
from typing import List, Tuple

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog,\
    QMessageBox, QDialog, QTextBrowser, QListWidget, QTextEdit, QTreeWidgetItem, QInputDialog,\
    QToolBar, QSizePolicy
from PySide6.QtCore import Qt, Signal, QByteArray, QSignalBlocker, QSize
from PySide6.QtGui import QAction, QIcon

import PySide6QtAds as QtAds

from PySide6.QtWidgets import QTabWidget, QVBoxLayout

from ui import Ui_MainWindow2
import utils.thread
from widget.dialog import new_article_dialog
from widget.search import DelayedSearchWidget
from widget.text import EditableTextEdit
from complex.zone import ModuleViewZone, MainBrowserZone, NoteViewZone, NoteEditZone, PDFViewerZone
from complex.online_search import OnlineSearchZone
from complex.advanced_search import AdvancedSearchZone
from complex.semantic_search import SemanticSearchZone
from complex.test_llama import TestLLamaZone

from crawler import DownloadWorker

from database import Article, Keyword, Note
import database

from sylva import ArticleData, NoteData, AnnotationData, FolderData
from sylva import Sylva, UserDict

import utils
import utils.format as fmt
import utils.opn as opn
from utils.opn import to_data
import utils.combo as cb

from mvc.module import NestedModule, NonNestedModule
from mvc.notem import NoteModule

from tools.pdf.pdf import extract_annotations
import tools.ref as ref

import markdown2
import datetime

from func import global_session

import pickle as pkl

from widget.emitter import emitter

class LMainWindow(QMainWindow, Ui_MainWindow2):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ludwig Article Manager")
        self.focus_id = None
        self.download_id = None
        # self.log = [] # TODO

        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        action = QAction(QIcon(":icons/sync.png"), "Sync All", self)
        self.toolbar.addAction(action)
        self.toolbar.addAction(QAction(QIcon(":icons/rebuild.png"), "Build Vector", self))
        self.toolbar.addAction(QAction(QIcon(":icons/reindex.png"), "Reindex", self))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.OpaqueSplitterResize, True)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.XmlCompressionEnabled, False)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.FocusHighlighting, True)
        QtAds.CDockManager.setAutoHideConfigFlags(QtAds.CDockManager.DefaultAutoHideConfig)
        self.dock_manager = QtAds.CDockManager(self)

        self.is_notelock = [1, 1]
        self.pdf_area = None
        self.pdf_set = set()

        # define the dock view
        self.zone_moduleview = ModuleViewZone(self)
        self.zone_mainbrowser = MainBrowserZone(self)
        self.zone_noteview = NoteViewZone(self)
        self.zone_noteedit = NoteEditZone(self)
        self.zone_onlinesearch = OnlineSearchZone(self)
        self.zone_advancedsearch = AdvancedSearchZone(self)
        self.zone_semanticsearch = SemanticSearchZone(self)

        self.zone_testllama = TestLLamaZone(self)

        self.task_queue = utils.thread.TaskQueue(1)
        self.zone_onlinesearch.set_taskqueue(self.task_queue)
        self.zone_advancedsearch.set_taskqueue(self.task_queue)
        self.zone_advancedsearch.action_test_internet()

        from setting import SEARCH_ENGINE_PREFER
        self.zone_advancedsearch.button_group.buttons()[SEARCH_ENGINE_PREFER].setChecked(True)
        self.zone_advancedsearch.search_engine = SEARCH_ENGINE_PREFER

        self.widgets = {
            "mvm": self.zone_moduleview.mvm,
            "nvm": self.zone_moduleview.nvm,
            "notem": self.zone_noteview.notem,
            "browser": self.zone_mainbrowser.browser,
            "nttl": self.zone_noteedit.textedit_tl,
            "ntcn": self.zone_noteedit.textedit_cn,
        }

        # init the necessary data
        emitter.render_main_viewer.emit()
        emitter.clear_note_editor.emit()

        dock1 = QtAds.CDockWidget("Main View", self)
        dock1.setWidget(self.zone_moduleview)
        area1 = self.dock_manager.setCentralWidget(dock1)
        area1.setAllowedAreas(QtAds.DockWidgetArea.OuterDockAreas)

        dock3 = QtAds.CDockWidget("Note View", self)
        dock3.setWidget(self.zone_noteview)
        dock3.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
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

        dock6 = QtAds.CDockWidget("Advanced Search", self)
        dock6.setWidget(self.zone_advancedsearch)
        area6 = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.LeftDockWidgetArea, dock6)

        dock7 = QtAds.CDockWidget("Semantic Search", self)
        dock7.setWidget(self.zone_semanticsearch)
        area7 = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.LeftDockWidgetArea, dock7)

        dock8 = QtAds.CDockWidget("Test LLama", self)
        dock8.setWidget(self.zone_testllama)
        area8 = self.dock_manager.addDockWidget(QtAds.DockWidgetArea.RightDockWidgetArea, dock8)

        self.dock_widgets = {
            "module": dock1,
            "main": dock2,
            "note": dock3,
            "note_edit": dock4,
            "online_search": dock5,
            "advanced_search": dock6,
            "semantic_search": dock7,
            "test_llama": dock8,
        }

        self._setupMenuAction()
        self._setupSlots()
        self._always_test()

        self.loadPerspective()

    def _setupMenuAction(self):
        self.actionImport_article.triggered.connect(self.onImportClicked)
        self.actionImport_batch.triggered.connect(self.onImportBatchClicked)
        self.actionImport_manually.triggered.connect(self.onManualClicked)
        self.actionSave_layout.triggered.connect(self.onSaveLayoutClicked)

        self.menuRecover_layout.addAction(self.dock_widgets["main"].toggleViewAction())
        self.menuRecover_layout.addAction(self.dock_widgets["note"].toggleViewAction())
        self.menuRecover_layout.addAction(self.dock_widgets["note_edit"].toggleViewAction())
        self.menuRecover_layout.addAction(self.dock_widgets["online_search"].toggleViewAction())
        self.menuRecover_layout.addAction(self.dock_widgets["advanced_search"].toggleViewAction())
        self.menuRecover_layout.addAction(self.dock_widgets["semantic_search"].toggleViewAction())
        self.menuRecover_layout.addAction(self.dock_widgets["test_llama"].toggleViewAction())

        # self.actionNote_Browser.triggered.connect
        # self.actionNote_View.triggered.connect
        # self.actionAdvanced_Search.triggered.connect
        # self.actionOnline_Search.triggered.connect
        # self.actionSave_layout.triggered.connect(self.onOnlineSearch) # just for test
        # Another action TODO
        # self.actionLoad_Library
        # self.actionDump_Library
        # self.actionMicrosoft_Modern

    def _setupSlots(self):
        emitter.open_pdf_internal.connect(self.onOpenArticlePDF)
        emitter.change_editor_mode.connect(self.changeEditMode)
        emitter.import_internet.connect(self.onOnlineSearchImport)
        # self.zone_onlinesearch.import_signal.connect(self.onOnlineSearchImport) TODO

    def _always_test(self):
        pass
        # import time
        # tic = time.time()
        # self.zone_advancedsearch.set_accounts(["fuckyour mother", None])
        # self.zone_advancedsearch.set_accounts([None, "well good"])
        # print(time.time() - tic)


    # --------------------------------------------------------------------------------
    # mainwindow GUI functions
    # browser
    def setFocusArticle(self, article_id: int = None):
        self.focus_id = article_id

    # --------------------------------------------------------------------------------
    # slot functions
    def onImportClicked(self):
        if not (file_path := QFileDialog.getOpenFileName(self, 'Open file', '', fmt.BIB_FILTER)[0]):
            return
        data = ref.REF_PARSER.extract(file_path)
        if data:
            self.importArticle(data)
        

    def onImportBatchClicked(self):
        if not (file_paths := QFileDialog.getOpenFileNames(self, 'Open folder', '', fmt.BIB_FILTER)[0]):
            return
        for file_path in file_paths:
            data = ref.REF_PARSER.extract(file_path)
            if data:
                self.importArticle(data)
    
    def onManualClicked(self):
        data = new_article_dialog(self)
        if data:
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
        
        self.pdf_viewer = PDFViewerZone(self)
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
        result["add_time"] = opn.get_time()
        self.importArticle(ArticleData(**result))


    # --------------------------------------------------------------------------------
    # combo functions
    def importArticle(self, datas: ArticleData | List[ArticleData]):
        if isinstance(datas, ArticleData):
            datas = [datas]
        for data in datas:
            if data.local_path is not None and not opn.check_path(opn.get_absolute_path(data.local_path)):
                data.local_path = None
            cb.new_article(None, -1, data)
        return True
    
    def changeEditMode(self, flag):
        if flag:
            self.dock_widgets["note_edit"].setWindowTitle("Note Browser")
        else:
            self.dock_widgets["note_edit"].setWindowTitle("Note Browser *")

    def savePerspective(self):
        with open("./cache/layout.xml", "wb") as f:
            f.write(self.dock_manager.saveState())

    def loadPerspective(self):
        with open("./cache/layout.xml", "rb") as f:
            self.dock_manager.restoreState(f.read())

    def closeEvent(self, event):
        # self.savePerspective()
        self.dock_manager.deleteLater()
        super().closeEvent(event)
