from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QToolBar, QAction, \
    QTextBrowser

from mvc.module import NestedModule, NonNestedModule
from mvc.notem import NoteModule

from widget.search import SearchWidget

from utils import opn
from utils.opn import to_profile, to_data
import utils.format as fmt

from archi import Archi, ProfileData

from mvc.funcs import on_new_note

class ModuleViewZone(QWidget):
    def __init__(self, parent=None, clf=None):
        super().__init__(parent)
        
        self.tab_widget = QTabWidget(self)
        tab1 = QWidget()
        tab2 = QWidget()

        self.mvm: NonNestedModule = clf.mvm
        self.nvm: NestedModule = clf.nvm

        self.search_widget = SearchWidget(self)
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
            self.mvm.add_item(article.id, to_profile(to_data(article)))
        
        archi = Archi()
        archi.load()
        for kv in archi.data:
            item = self.nvm.add_item(-1, True, ProfileData(kv['name'], '', '', '', '', ''))
            for idx in kv['data']:
                article = opn.get_article(idx)
                self.nvm.add_item(idx, False, to_profile(to_data(article)), item)

    def clear_data(self):
        self.mvm.model.removeRows(0, self.mvm.model.rowCount())
        self.nvm.model.removeRows(0, self.nvm.model.rowCount())


class MainBrowserZone(QWidget):
    def __init__(self, parent=None, clf=None):
        super().__init__(parent)
        
        self.toolbar = QToolBar("Toolbar", self)
        actionAddnote = QAction("Add note", self)
        actionAddnote.triggered.connect(self._add_note)
        self.toolbar.addAction(actionAddnote)

        self.browser: QTextBrowser = clf.browser_m

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.article_id = None
    
    def init_data(self, article_id):
        self.article_id = article_id
        article = opn.get_article(article_id)
        content = fmt.get_article_html(article)
        content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
        self.browser.setHtml(content)

    def clear_data(self):
        self.article_id = None
        self.browser.clear()

    def _add_note(self):
        if self.article_id:
            on_new_note(self.article_id)

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
        self.article_id = article_id
        notes = opn.get_article_notes(opn.get_article(article_id))
        for note in notes:
            self.notem.add_item(note.id, to_profile(to_data(note)))

    def clear_data(self):
        self.article_id = None
        self.notem.model.removeRows(0, self.notem.model.rowCount())

class NoteBrowserZone(QWidget):
    def __init__(self, parent=None, clf=None):
        super().__init__(parent)

        self.browser_tl: QTextBrowser = clf.browser_nt_1
        self.browser_nt: QTextBrowser = clf.browser_nt_2

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        layout.addWidget(self.browser_tl, stretch=1)
        layout.addWidget(self.browser_nt, stretch=8)
        self.setLayout(layout)
        self.note_id = None

    def init_data(self, note_id): # TODO, give it title
        self.note_id = note_id
        note = opn.get_note(note_id)
        content = fmt.get_notes_html([note])
        content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
        self.browser_nt.setHtml(content)

    def clear_data(self):
        self.note_id = None
        self.browser_nt.clear()