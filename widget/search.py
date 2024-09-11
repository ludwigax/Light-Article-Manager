from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QIcon, QPixmap

import ui.res_rc

class SearchWidget(QWidget):
    search_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText('Type to search...')
        self.search_box.returnPressed.connect(self.on_search)
        layout.addWidget(self.search_box)

        self.search_button = QPushButton(self)
        self.search_button.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/search.png"), QIcon.Normal, QIcon.Off)
        self.search_button.setIcon(icon)
        self.search_button.clicked.connect(self.on_search)
        self.search_button.setFixedSize(24, 24)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def on_search(self):
        search_text = self.search_box.text()
        if not search_text:
            self.search_signal.emit('')
            return
        print(f'Searching for: {search_text}')
        self.search_signal.emit(search_text)

class DelayedSearchWidget(SearchWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.search_box.textChanged.connect(self.on_text_change)
        self.timer.timeout.connect(self.on_search)

    def on_text_change(self):
        self.timer.start(500)  # 500ms delay

    def on_search(self):
        self.timer.stop()
        super().on_search()
