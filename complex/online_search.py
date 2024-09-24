from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, \
    QPushButton

from widget.search import SearchWidget
from widget.emitter import emitter
from widget.button import StyleButton

from utils.thread import TaskQueue
from tools.web import parse, webfuncs

import setting
from setting import ACTIVE_ADVANCED_SEARCH_ENGINE


class OnlineSearchZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._metadata = None
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

    def set_taskqueue(self, task_queue: TaskQueue):
        self.task_queue = task_queue

    def _start_worker(self, func, args, callback):
        if self.is_working:
            return
        self.is_working = True
        self.task_queue.add_task(func, args, [callback, self.error_display])
        
    def google_search(self, text):
        if not text:
            return
        self._start_worker(webfuncs.google_scholar_get, (text,), self.google_results_display)

    def crossref_search(self, item):
        title = item.text().split(' - ')[0]
        self._start_worker(webfuncs.crossref_get, (title, None), self.crossref_results_display)

    def google_results_display(self, response):
        self.is_working = False
        results = parse.google_scholar_parse(response, limit = 20)

        self.list_widget.clear()
        for result in results:
            item = QListWidgetItem(f"{result['title']} - {result['page_url']}")
            self.list_widget.addItem(item)

    def crossref_results_display(self, response):
        self.is_working = False
        metadatas = parse.crossref_parse(response)
        metadata = metadatas[0] if metadatas else None

        formatted_string = f"""<p>----- <span style="color: green;">Article Metadata</span> -----</p>
<p><span style="color: blue;">Title</span>: {metadata['title']}</p>
<p><span style="color: blue;">Abstract</span>: {metadata['abstract']}</p>
<p><span style="color: blue;">Authors</span>: {metadata['authors']}</p>
<p><span style="color: blue;">Published Year</span>: {metadata['year']}</p>
<p><span style="color: blue;">Journal</span>: {metadata['journal']}</p>
<p><span style="color: blue;">DOI</span>: {metadata['doi']}</p>
<p><span style="color: blue;">Keywords</span>: {metadata['keywords']}</p>
<p>------------------------</p>
"""
        self.result_label.setText(formatted_string)

        self._metadata = metadata
        self.import_button.setEnabled(True)

    def error_display(self, error):
        self.is_working = False
        self.result_label.setText(f"<p><span style='color: red;'>Error</span>: {error}</p>")

    def import_selection(self):
        if not self._metadata:
            self.import_button.setEnabled(False)
            return
        
        emitter.import_online.emit(self._metadata)
        self.import_button.setEnabled(False)
        self._metadata = None




