from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QToolBar, \
    QTextBrowser, QListWidget, QListWidgetItem, QLabel, QPushButton
from PySide6.QtGui import QAction

from mvc.module import NestedModule, NonNestedModule
from mvc.notem import NoteModule

from widget.search import SearchWidget, DelayedSearchWidget
from widget.button import PDFDropButton, StyleButton
from widget.text import EditableTextEdit

from utils import opn
from utils.opn import to_data
import utils.format as fmt

import tools.web as web

from sylva import Sylva, UserDict, FolderData

from mvc.funcs import on_new_note_passive

class ModuleViewZone(QWidget):
    def __init__(self, parent=None, clf=None):
        super().__init__(parent)
        
        self.tab_widget = QTabWidget(self)
        tab1 = QWidget()
        tab2 = QWidget()

        self.mvm: NonNestedModule = clf.mvm
        self.nvm: NestedModule = clf.nvm

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
    
    def init_data(self):
        articles = opn.get_all_articles()

        for article in articles:
            self.mvm.append_item(article.id, to_data(article))
        
        sylva = Sylva()
        sylva.load()
        for kv in sylva.data:
            item = self.nvm.append_item(-1, True, FolderData(kv['name']))
            for idx in kv['data']:
                article = opn.get_article(idx)
                if not article:
                    continue
                self.nvm.append_item(idx, False, to_data(article), item)

    def clear_data(self):
        self.mvm.model.removeRows(0, self.mvm.model.rowCount())
        self.nvm.model.removeRows(0, self.nvm.model.rowCount())


class MainBrowserZone(QWidget):
    def __init__(self, parent=None, clf=None):
        super().__init__(parent)
        
        self.toolbar = QToolBar("Toolbar", self)
        self.add_note_button = StyleButton(self, "PURPLE")
        self.add_note_button.setText("Add Note")
        self.add_note_button.clicked.connect(self._add_note)
        self.toolbar.addWidget(self.add_note_button)

        self.drag_button = PDFDropButton(self)
        self.drag_button.init_data(None, None)
        self.toolbar.addWidget(self.drag_button)

        self.browser: QTextBrowser = clf.browser_m

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.article_id = None
    
    def init_data(self, article_id):
        if article_id is None:
            return
        self.article_id = article_id
        article = opn.get_article(article_id)
        content = fmt.get_article_html(article, article_only=True) # TODO note html error
        content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
        self.browser.setHtml(content)

        self.drag_button.init_data(fmt.absolute_path(article.local_path), article_id)

    def clear_data(self):
        self.article_id = None
        self.browser.clear()

    def _add_note(self): # TODO transfer this function in mainwindow2
        if self.article_id:
            note_id, data, flag = on_new_note_passive(self.window().zone_noteview.notem, self.article_id)
            if not flag:
                return
            self.window().zone_noteview.init_data(self.article_id) # note view zone

class NoteViewZone(QWidget):
    def __init__(self, parent = None, clf = None):
        super().__init__(parent)
        self.notem: NoteModule = clf.notem

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        layout.addWidget(self.notem.tree_view)
        self.setLayout(layout)

        self.article_id = None

    def init_data(self, article_id):
        if article_id is None:
            return
        self.article_id = article_id
        self.notem.focus_id = article_id
        notes = opn.get_article_notes(opn.get_article(article_id))
        for note in notes:
            self.notem.append_item(note.id, to_data(note))

    def clear_data(self):
        self.article_id = None
        self.notem.focus_id = None
        self.notem.model.removeRows(0, self.notem.model.rowCount())

class NoteEditZone(QWidget):
    def __init__(self, parent=None, clf=None):
        super().__init__(parent)

        self.textedit_tl: EditableTextEdit = clf.textedit_nt_tl
        self.textedit_cn: EditableTextEdit = clf.textedit_nt_cn
        self.textedit_tl.setStyleSheet("font-size: 24px; font-weight: bold; border: none;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        layout.addWidget(self.textedit_tl, stretch=1)
        layout.addWidget(self.textedit_cn, stretch=8)
        self.setLayout(layout)
        self.note_id = None

    def init_data(self, note_id): # TODO, give it title
        if note_id is None:
            self.clear_data()
            return
        self.enabled()
        self.note_id = note_id
        note = opn.get_note(note_id)
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


# pdfviewer
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument

class PDFViewerZone(QWidget):
    def __init__(self, parent=None, clf=None):
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


class NetworkThread(QThread):
    finished_signal = Signal(object)
    error_signal = Signal(str)

    def __init__(self, func, params=()):
        super().__init__()
        self.func = func
        self.params = params

    def run(self):
        try:
            response = self.func(*self.params)
            self.finished_signal.emit(response)
        except Exception as e:
            self.error_signal.emit(str(e))

class OnlineSearchZone(QWidget):
    import_signal = Signal(dict)

    def __init__(self, parent=None, clf=None):
        super().__init__(parent)

        self._metadata = None
        self.worker = None
        self.is_working = False
    
        layout = QVBoxLayout()

        self.search_widget = SearchWidget(self)
        layout.addWidget(self.search_widget)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.list_widget)

        self.result_label = QLabel(self)
        self.result_label.setText("""<p><span style="color: green;">Meta Data</span> results will be displayed <span style="color: red;">here</span>.</p>""")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        self.import_button = QPushButton("Import this reference", self)
        self.import_button.setEnabled(False)
        layout.addWidget(self.import_button)

        self.setLayout(layout)
        self._setupSlots()

    def _setupSlots(self):
        self.search_widget.search_signal.connect(self.google_search)
        self.list_widget.itemClicked.connect(self.crossref_search)
        self.import_button.clicked.connect(self.import_selection)

    def _start_worker(self, func, args, on_finished):
        if self.worker:
            self.worker.terminate()

        self.worker = NetworkThread(func, args)
        self.worker.finished_signal.connect(on_finished)
        self.worker.finished_signal.connect(self.worker.deleteLater)
        self.worker.error_signal.connect(self.display_error)
        self.is_working = True
        self.worker.start()
        
    def google_search(self, text):
        if not text or self.is_working:
            return
        
        self._start_worker(web.google_scholar_get, (text,), self.display_google_results)

    def crossref_search(self, item):
        if self.is_working:
            return

        title, doi = item.text().split(" - ")
        self._start_worker(web.crossref_get, (title, None), self.display_crossref_results)

    def display_google_results(self, response):
        self.is_working = False
        results = web.parse_google_scholar_results(response)

        self.list_widget.clear()
        for result in results:
            item = QListWidgetItem(f"{result['title']} - {result['doi']}")
            self.list_widget.addItem(item)

    def display_crossref_results(self, response):
        self.is_working = False
        metadata = web.parse_crossref_results(response)

        metadata['title'] = web.remove_formatting(metadata['title'])
        metadata['abstract'] = web.remove_formatting(metadata['abstract'])

        formatted_string = f"""<p>----- <span style="color: green;">Article Metadata</span> -----</p>
<p><span style="color: blue;">Title</span>: {metadata['title']}</p>
<p><span style="color: blue;">Abstract</span>: {metadata['abstract']}</p>
<p><span style="color: blue;">Authors</span>: {', '.join(metadata['authors'])}</p>
<p><span style="color: blue;">Published Year</span>: {metadata['published_year']}</p>
<p><span style="color: blue;">Journal</span>: {metadata['journal']}</p>
<p><span style="color: blue;">DOI</span>: {metadata['doi']}</p>
<p><span style="color: blue;">Keywords</span>: {metadata['keywords']}</p>
<p>------------------------</p>
"""
        self.result_label.setText(formatted_string)

        self._metadata = metadata
        self.import_button.setEnabled(True)

    def display_error(self, error):
        self.is_working = False
        self.result_label.setText(f"<p><span style='color: red;'>Error</span>: {error}</p>")

    def import_selection(self):
        if not self._metadata:
            self.import_button.setEnabled(False)
            return
        
        self.import_signal.emit(self._metadata)
        self.import_button.setEnabled(False)
        self._metadata = None
        
