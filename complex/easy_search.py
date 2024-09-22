from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, \
    QPushButton, QListWidget, QListWidgetItem

from widget.search import SearchWidget


class EasySearchZone(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.results = []
        self.idx = -1

        layout = QVBoxLayout()

        self.search_widget = SearchWidget()
        self.status_label = QLabel()
        self.status_label.setText("Status: No Task")

        self.list_widget = QListWidget()
        self.list_widget.setFrameShape(QFrame.Panel)
        self.list_widget.setFrameShadow(QFrame.Sunken)
        self.list_widget.setLineWidth(2)
        self.result_label = QLabel()
        self.result_label.setText("Search Results")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setFrameShape(QFrame.Panel)
        self.result_label.setFrameShadow(QFrame.Sunken)
        self.result_label.setLineWidth(2)

        navi_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        navi_layout.addWidget(self.prev_button)
        navi_layout.addWidget(self.next_button)

        layout.addWidget(self.search_widget)
        layout.addWidget(self.status_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.result_label)
        layout.addLayout(navi_layout)

        # layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    
    def set_slots(self):
        def render_item(item):
            idx = self.list_widget.row(item)
            self.render_label(idx)
        
        self.prev_button.clicked.connect(self.prev_button)
        self.next_button.clicked.connect(self.next_button)
        self.list_widget.itemClicked.connect(render_item) # TODO

    def set_search_results(self, results): #  TODO
        if not results:
            results = []
        self.init_data(results)
        self.idx = 0 if results else -1
        self.render_label(self.idx)

    def init_data(self, results):
        if (not results) and self.results:
            self.clear_data()
            return
        
        if not results:
            return
        self.results = results
        for res in self.results:
            item = QListWidgetItem(res["title"])
            self.list_widget.addItem(item)

    def clear_data(self):
        self.results = []
        for item in reversed(self.list_widget.item()):
            self.list_widget.removeItemWidget(item)

    def render_label(self, idx):
        if not 0 <= idx <= len(self.results):
            return
        self.result_label.setText(self.results[idx]["title"])

    def render_status(self, status):
        self.status_label.setText(f"{status}")

    def clear_label(self):
        self.idx = -1
        self.result_label.clear()

    def prev_item(self):
        if self.idx == -1:
            return
        
        if not 0 < self.idx <= len(self.results):
            return
        self.idx -= 1
        self.render_label(self.idx)

    def next_item(self):
        if self.idx == -1:
            return
        
        if not 0 <= self.idx < len(self.results):
            return
        self.idx += 1
        self.render_label(self.idx)