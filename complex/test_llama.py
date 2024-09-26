from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, \
    QLabel, QListWidgetItem

from widget.search import SearchWidget

from utils.thread import SocketThread, TempThread

class TestLLamaZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Thread")
        self.exit_button = QPushButton("Exit Thread")
        self.search_widget = SearchWidget()
        self.list_widget = QListWidget()

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.exit_button)

        layout.addLayout(button_layout)
        layout.addWidget(self.search_widget)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_thread)
        self.exit_button.clicked.connect(self.exit_thread)

        self.worker = None
        self.slave_worker = None

    def start_thread(self):
        self.clear_text()
        self.init_text()

        self.worker = SocketThread()
        
        self.worker.start()
        self.search_widget.search_signal.connect(self.search)
        self.start_button.setEnabled(False)

    def exit_thread(self):
        if self.worker:
            self.worker.stop()
            self.worker = None
            self.search_widget.search_signal.disconnect(self.search)
            self.start_button.setEnabled(True)

    def search(self, text):
        if not text:
            return
        if self.worker:
            self.add_text("User: " + text)
            self.add_text("Assistant: " + "")
            self.slave_worker = TempThread(self.worker.conn, text)
            self.slave_worker.stream_signal.connect(self.update_text)
            self.slave_worker.start()
        if text == "exit":
            self.slave_worker.wait()
            self.exit_thread()

    def init_text(self):
        import json
        messages_path = "./tools/emb/messages.json"
        with open(messages_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
        for data in messages:
            self.add_text(f'{data["role"]}: {data["content"]}')

    def clear_text(self):
        self.list_widget.clear()

    def add_text(self, text):
        label = QLabel(text)
        label.setFixedWidth(300)
        label.setWordWrap(True)
        item = QListWidgetItem()
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, label)

    def update_text(self, text):
        if text == "[END]":
            self.slave_worker.quit()
            self.slave_worker = None
            return
        if text:
            item = self.list_widget.item(self.list_widget.count() - 1)
            label: QLabel = self.list_widget.itemWidget(item)
            label.setText(label.text() + text)
            label.adjustSize()