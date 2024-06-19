from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

import ui.res_rc

class SearchWidget(QWidget):
    search_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.initUI()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_search)

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText('Type to search...')
        self.search_box.textChanged.connect(self.on_text_change)
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

    def on_text_change(self):
        self.timer.start(500)  # 500ms delay

    def on_search(self):
        self.timer.stop()
        search_text = self.search_box.text()
        if not search_text:
            return
        print(f'Searching for: {search_text}')
        self.search_signal.emit(search_text)