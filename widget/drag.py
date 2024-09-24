from PySide6.QtWidgets import QLabel, QListWidgetItem, QListWidget, QApplication
from PySide6.QtCore import Qt, QMimeData, QPoint
from PySide6.QtGui import QDrag, QDragEnterEvent

from widget.label import MetaLabel, CountLabel

import json


class DragLabel(MetaLabel):
    def __init__(self, drop_in = True, drag_out = True):
        super().__init__(None, "<p>-- Search Results --</p>")
        self.setAcceptDrops(drop_in)
        self.drop_in = drop_in
        self.drag_out = drag_out

    def mousePressEvent(self, event):
        if self.drag_out and event.button() == Qt.LeftButton:
            if not self._metadata:
                return
            mime_data = QMimeData()
            bytes = json.dumps(self._metadata).encode()
            mime_data.setData("application/octet-stream", bytes)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.CopyAction | Qt.MoveAction)

    def dragEnterEvent(self, event):
        if self.drop_in and event.mimeData().hasFormat("application/octet-stream"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.drop_in and event.mimeData().hasFormat("application/octet-stream"):
            label_data = event.mimeData().data("application/octet-stream")
            self.setMetaData(json.loads(label_data.data().decode()))
            event.acceptProposedAction()


class DragCountLabel(CountLabel):
    def __init__(self, drop_in = True, drag_out = False):
        super().__init__()
        self.setAcceptDrops(drop_in)
        self.drop_in = drop_in

    def dragEnterEvent(self, event):
        if self.drop_in and event.mimeData().hasFormat("application/octet-stream"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.drop_in and event.mimeData().hasFormat("application/octet-stream"):
            label_data = event.mimeData().data("application/octet-stream")
            self.addMetaData(json.loads(label_data.data().decode()))
            event.acceptProposedAction()


class MetaItem(QListWidgetItem):
    def __init__(self, metadata):
        super().__init__(metadata.get("title"))
        self._metadata = metadata

    def setMetaData(self, metadata):
        self._metadata = metadata
        return super().setText(self._metadata.get("title"))

    def metadata(self):
        return self._metadata


class DragListWidget(QListWidget):
    def __init__(self, drop_in=True, drag_out=True):
        super().__init__()
        self.dragging = True
        self.start_point = QPoint()
        self.drag_out = drag_out
        self.drop_in = drop_in
        self.setAcceptDrops(drop_in)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event):
        if self.drop_in and event.mimeData().hasFormat("application/octet-stream"):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if self.drop_in and event.mimeData().hasFormat("application/octet-stream"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/octet-stream"):
            item_data = event.mimeData().data("application/octet-stream")
            meta_data = json.loads(item_data.data().decode())
            drop_index = self.indexAt(QPoint(event.position().x(), event.position().y()))
            if drop_index.isValid():
                self.insertItem(drop_index.row(), MetaItem(meta_data))
            else:
                self.addItem(MetaItem(meta_data))
            event.acceptProposedAction()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.position().toPoint()
            item: MetaItem = self.itemAt(self.start_point)
            if item:
                self.dragging = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.dragging:
            super().mouseMoveEvent(event)
        distance = (event.position().toPoint() - self.start_point).manhattanLength()
        if distance >= QApplication.startDragDistance():
            item: MetaItem = self.itemAt(self.start_point)
            mime_data = QMimeData()
            mime_data.setData("application/octet-stream", json.dumps(item.metadata()).encode())
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            if drag.exec(Qt.MoveAction) == Qt.MoveAction:
                self.takeItem(self.row(item))
            self.dragging = False

    def mouseReleaseEvent(self, event):
        self.dragging = False
        super().mouseReleaseEvent(event)

