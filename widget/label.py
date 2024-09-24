from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QDragEnterEvent

import json

import utils.format as fmt


class KVLabel(QWidget):
    def __init__(self, key, value, status_color):
        super().__init__()

        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        self.key_label = QLabel(key)
        self.key_label.setFrameShape(QFrame.Panel)
        self.key_label.setFrameShadow(QFrame.Sunken)
        self.key_label.setLineWidth(2)
        self.key_label.setAlignment(Qt.AlignCenter)
        self.key_label.setStyleSheet("""
            font-weight: bold;
            font-size: 12px;
            color: #013e5d;
            background-color: none;
        """)

        self.value_label = QLabel(value)
        self.value_label.setFrameShape(QFrame.Panel)
        self.value_label.setFrameShadow(QFrame.Sunken)
        self.value_label.setLineWidth(2)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")

        layout.addWidget(self.key_label)
        layout.addWidget(self.value_label)
        self.setLayout(layout)

    def setTexts(self, key, value, status_color):
        self.key_label.setText(key)
        self.value_label.setText(value)
        self.value_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")


class MetaLabel(QLabel):
    def __init__(self, metadata=None, text=None):
        if metadata and text is None:
            text = fmt.format_metadata(metadata)
        super().__init__(text)
        self._metadata = metadata

    def setMetaData(self, metadata=None, text=None):
        self._metadata = metadata
        if metadata and text is None:
            text = fmt.format_metadata(metadata)
        self.setText(text)


class CountLabel(QLabel):
    def __init__(self):
        super().__init__()
        self._metadatas = []
        self.setText(f"Total: {len(self._metadatas)}")

    def addMetaData(self, metadatas):
        if not isinstance(metadatas, list):
            metadatas = [metadatas]
        self._metadatas.extend(metadatas)
        self.setText(f"Total: {len(self._metadatas)}")

    def clearMetaData(self):
        self._metadatas.clear()
        self.setText(f"Total: {len(self._metadatas)}")
