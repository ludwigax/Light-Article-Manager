from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QToolBar, \
    QTextBrowser
from PySide6.QtGui import QAction

from mvc.module import NestedModule, NonNestedModule
from mvc.notem import NoteModule

from widget.search import SearchWidget, DelayedSearchWidget
from widget.button import PDFDropButton, StyleButton
from widget.text import EditableTextEdit
from widget.emitter import emitter

import utils.opn as opn
from utils.opn import to_data
import utils.format as fmt
import utils.combo as cb

import tools.web as web

from sylva import Sylva, UserDict, FolderData
from func import global_sylva

class ModuleViewZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.tab_widget = QTabWidget(self)
        tab1 = QWidget()
        tab2 = QWidget()

        self.mvm = NonNestedModule(self, columns=None)
        self.nvm = NestedModule(self, columns=None)

        self.search_widget = DelayedSearchWidget(self)
        self.search_widget.search_signal.connect(self.mvm._sort_by_search)
        self.search_widget.search_signal.connect(self.nvm._sort_by_search)

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

        self.tab_widget.addTab(tab1, "Flat View")
        self.tab_widget.addTab(tab2, "Folder View")

        layout = QVBoxLayout()
        layout.addWidget(self.search_widget)
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.set_slots()

    def set_slots(self):
        def refresh_mvm():
            self._clear_mvm()
            self._init_mvm()

        def refresh_nvm():
            self._clear_nvm()
            self._init_nvm()

        emitter.render_main_viewer.connect(self.init_data)
        emitter.clear_main_viewer.connect(self.clear_data)
        emitter.refresh_mvm.connect(refresh_mvm)
        emitter.refresh_nvm.connect(refresh_nvm)

    def init_data(self):
        self._init_mvm()
        self._init_nvm()

    def clear_data(self):
        self._clear_mvm()
        self._clear_nvm()

    def _init_mvm(self):
        articles = opn.get_all_articles()
        for article in articles:
            self.mvm.append_item(to_data(article))

    def _init_nvm(self):
        sylva = global_sylva()
        for kv in sylva.data:
            data = FolderData(kv['id'], kv['name'])
            self.nvm.append_item(1, data, None)
            index = self.nvm.model.index(self.nvm.model.rowCount() - 1, 0)
            for article_id in kv['data']:
                article = opn.get_article(article_id)
                if not article:
                    continue
                self.nvm.append_item(0, to_data(article), index)

    def _clear_mvm(self):
        self.mvm.model.removeRows(0, self.mvm.model.rowCount())

    def _clear_nvm(self):
        self.nvm.model.removeRows(0, self.nvm.model.rowCount())


class MainBrowserZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.toolbar = QToolBar("Toolbar", self)
        self.add_note_button = StyleButton(self, "PURPLE")
        self.add_note_button.setText("New Note")
        self.add_note_button.clicked.connect(self.action_add_note)

        self.drag_button = PDFDropButton(self)
        self.drag_button.init_data(None, None)

        self.sync_button = StyleButton(self, "RED")
        self.sync_button.setText("Sync Data")
        self.sync_button.clicked.connect(self._sync_all)

        self.toolbar.addWidget(self.add_note_button)
        self.toolbar.addWidget(self.drag_button)
        self.toolbar.addWidget(self.sync_button)

        self.browser = QTextBrowser(self)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.set_slots()

        self.article_id = None

    def set_slots(self):
        def open_pdf(path):
            opn.open_file(path)
            self.init_data(None)

        emitter.render_main_browser.connect(self.init_data)
        emitter.clear_main_browser.connect(self.clear_data)

        self.browser.anchorClicked.connect(open_pdf)
    
    def init_data(self, article_id):
        if not article_id:
            article_id = self.article_id
        article = opn.get_article(article_id)
        if article is None:
            if self.article_id is not None:
                self.clear_data()
            return
        
        self.article_id = article_id
        content = fmt.get_article_html(article, article_only=True) # TODO note html error
        content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
        self.browser.setHtml(content)
        self.drag_button.init_data(opn.get_absolute_path(article.local_path), article_id)

    def clear_data(self):
        self.article_id = None
        self.browser.clear()
        self.drag_button.clear_data()

    def action_add_note(self):
        emitter.refresh_note_viewer.emit(self.article_id)
        cb.new_note_passive(None, self.article_id)

    def _sync_all(self):
        pass

class NoteViewZone(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.notem = NoteModule(self)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        layout.addWidget(self.notem.tree_view)
        self.setLayout(layout)

        self.set_slots()

        self.article_id = None

    def set_slots(self):
        emitter.render_note_viewer.connect(self.init_data)
        emitter.clear_note_viewer.connect(self.clear_data)
        emitter.refresh_note_viewer.connect(self.refresh)

    def init_data(self, article_id):
        article = opn.get_article(article_id)
        if article is None:
            if self.article_id is not None:
                self.clear_data()
            return
        
        self.article_id = article_id
        self.notem.focus_id = article_id
        notes = opn.get_article_notes(article)
        for note in notes:
            self.notem.append_item(to_data(note))

    def clear_data(self):
        self.article_id = None
        self.notem.focus_id = None
        self.notem.model.removeRows(0, self.notem.model.rowCount())

    def refresh(self, article_id):
        if article_id is None:
            article_id = self.article_id
        if article_id == self.article_id:
            self.clear_data()
            self.init_data(article_id)


class NoteEditZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.textedit_tl = EditableTextEdit(self)
        self.textedit_cn = EditableTextEdit(self)
        self.textedit_tl.setStyleSheet("font-size: 24px; font-weight: bold; border: none;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        layout.addWidget(self.textedit_tl, stretch=1)
        layout.addWidget(self.textedit_cn, stretch=8)
        self.setLayout(layout)
        self.note_id = None
        self.clear_data()

        self.set_slots()

    def set_slots(self):
        emitter.render_note_editor.connect(self.init_data)
        emitter.clear_note_editor.connect(self.clear_data)

        self.textedit_tl.editingChanged.connect(lambda x: self.editSwitching(x, "tl"))
        self.textedit_cn.editingChanged.connect(lambda x: self.editSwitching(x, "cn"))

    def init_data(self, note_id): # TODO, give it title
        note = opn.get_note(note_id)
        if note is None:
            if self.note_id is not None:
                self.clear_data()
            return
        
        self.enabled()
        self.note_id = note_id
        self.textedit_tl.setText(note.title)
        self.textedit_cn.setHtml(note.note)

    def clear_data(self):
        self.note_id = None
        self.textedit_tl.clear()
        self.textedit_cn.clear()
        self.disabled()

    def enabled(self):
        self.textedit_tl.setEnabled(True)
        self.textedit_cn.setEnabled(True)
        self.textedit_tl.setPlaceholderText("Enter Title Here")

    def disabled(self):
        self.textedit_tl.setEnabled(False)
        self.textedit_cn.setEnabled(False)
        self.textedit_tl.setPlaceholderText("")

    def editSwitching(self, flag, who):
        emitter.change_editor_mode.emit(
            self.textedit_tl.is_locked and self.textedit_cn.is_locked
        )
        if not flag:
            return
        note = opn.get_note(self.note_id)
        data = to_data(note)
        if who == "tl":
            title = self.textedit_tl.toPlainText()
            data.title = title
        elif who == "cn":
            content = self.textedit_cn.toHtml()
            data.content = content
        data.changed_time = opn.get_time()
        opn.reset_note(data, note)
        emitter.refresh_note_viewer.emit(note.article_id)


# pdfviewer
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument

class PDFViewerZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pdfviewer = QPdfView(self)
        self.pdfviewer.setPageMode(QPdfView.MultiPage)

        self.pdfdoc = QPdfDocument()
        self.pdfviewer.setDocument(self.pdfdoc)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        layout.addWidget(self.pdfviewer)
        self.setLayout(layout)

    def init_data(self, pdf_path):
        self.pdfdoc.load(pdf_path)
